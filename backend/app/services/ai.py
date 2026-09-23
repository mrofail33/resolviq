import json
import re
from abc import ABC, abstractmethod
from datetime import date
from decimal import Decimal

from app.core.config import Settings, get_settings
from app.models.case import CaseCategory
from app.schemas.case import StructuredCaseAnalysis


class AIClient(ABC):
    @abstractmethod
    def analyze_documents(self, category: CaseCategory, text: str) -> StructuredCaseAnalysis:
        raise NotImplementedError

    @abstractmethod
    def generate_draft(self, category: CaseCategory, analysis: StructuredCaseAnalysis) -> str:
        raise NotImplementedError


class MockAIClient(AIClient):
    def analyze_documents(self, category: CaseCategory, text: str) -> StructuredCaseAnalysis:
        company = _first_company(text) or _default_company(category)
        amount = _first_amount(text)
        dates = _dates(text)
        reason = _reason(category)
        evidence = _evidence(text)
        missing = _missing_info(category, text)
        summary = (
            f"The user appears to have a {category.value} case involving {company}. "
            f"The available documents describe a dispute about {reason.lower()}."
        )
        return StructuredCaseAnalysis(
            summary=summary,
            company=company,
            disputed_amount=amount,
            important_dates=dates,
            dispute_reason=reason,
            evidence=evidence,
            missing_information=missing,
        )

    def generate_draft(self, category: CaseCategory, analysis: StructuredCaseAnalysis) -> str:
        amount = f" ${analysis.disputed_amount}" if analysis.disputed_amount else ""
        evidence = "\n".join(f"- {item}" for item in analysis.evidence) or "- Uploaded documents"
        missing_note = ""
        if analysis.missing_information:
            missing_note = (
                "\n\nI can provide any missing information you reasonably need, including "
                + ", ".join(analysis.missing_information)
                + "."
            )
        return (
            f"Subject: Request to resolve my {category.value} claim\n\n"
            f"To {analysis.company},\n\n"
            f"I am writing to request a fair resolution of my {category.value} claim{amount}. "
            f"{analysis.summary}\n\n"
            f"My reason for disputing the decision is: {analysis.dispute_reason}\n\n"
            f"Evidence I am relying on:\n{evidence}\n"
            f"{missing_note}\n\n"
            "Please review this matter and respond with the next steps or a written explanation "
            "of your decision.\n\n"
            "Sincerely,\nDemo User"
        )


class OpenAIClient(AIClient):
    def __init__(self, settings: Settings):
        self.settings = settings

    def analyze_documents(self, category: CaseCategory, text: str) -> StructuredCaseAnalysis:
        try:
            from openai import OpenAI

            client = OpenAI(api_key=self.settings.openai_api_key)
            prompt = (
                "Extract a consumer dispute case as JSON with keys: summary, company, "
                "disputed_amount, important_dates [{label,date}], dispute_reason, evidence, "
                "missing_information. Use only the document text. Category: "
                f"{category.value}\n\nDocument text:\n{text[:10000]}"
            )
            response = client.responses.create(
                model=self.settings.openai_model,
                input=prompt,
                text={"format": {"type": "json_object"}},
            )
            return StructuredCaseAnalysis.model_validate(json.loads(response.output_text))
        except Exception:
            return MockAIClient().analyze_documents(category, text)

    def generate_draft(self, category: CaseCategory, analysis: StructuredCaseAnalysis) -> str:
        return MockAIClient().generate_draft(category, analysis)


def get_ai_client() -> AIClient:
    settings = get_settings()
    if settings.ai_provider == "openai" and settings.openai_api_key:
        return OpenAIClient(settings)
    return MockAIClient()


def _first_company(text: str) -> str | None:
    patterns = [
        r"(?:from|company|merchant|airline|manufacturer)[:\s]+([A-Z][A-Za-z0-9 &-]{2,40})(?:[.,\n]|$)",
        r"\b([A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+){0,2})\s+(?:denied|refused|rejected)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip(" .")
    return None


def _default_company(category: CaseCategory) -> str:
    return {
        CaseCategory.refund: "the merchant",
        CaseCategory.warranty: "the manufacturer",
        CaseCategory.travel: "the travel provider",
    }[category]


def _first_amount(text: str) -> Decimal | None:
    match = re.search(r"\$\s?([0-9]+(?:\.[0-9]{1,2})?)", text)
    return Decimal(match.group(1)) if match else None


def _dates(text: str) -> list[dict[str, date]]:
    results: list[dict[str, date]] = []
    for raw in re.findall(r"\b(20[0-9]{2}-[0-9]{2}-[0-9]{2})\b", text):
        results.append({"label": "Mentioned date", "date": date.fromisoformat(raw)})
    return results[:3]


def _reason(category: CaseCategory) -> str:
    return {
        CaseCategory.refund: "The company refused or delayed a requested refund.",
        CaseCategory.warranty: "The warranty claim was denied despite available purchase evidence.",
        CaseCategory.travel: "The travel provider has not reimbursed the customer for a covered issue.",
    }[category]


def _evidence(text: str) -> list[str]:
    evidence = []
    lowered = text.lower()
    for label in ["receipt", "denial", "email", "warranty", "itinerary", "baggage"]:
        if label in lowered:
            evidence.append(label.title())
    return evidence or ["Uploaded document text"]


def _missing_info(category: CaseCategory, text: str) -> list[str]:
    lowered = text.lower()
    missing = []
    if "$" not in text:
        missing.append("disputed amount")
    if "receipt" not in lowered:
        missing.append("receipt or proof of purchase")
    if category == CaseCategory.travel and "itinerary" not in lowered:
        missing.append("travel itinerary")
    return missing
