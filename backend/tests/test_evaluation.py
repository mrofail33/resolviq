import json
from decimal import Decimal
from pathlib import Path

from app.models.case import CaseCategory
from app.services.ai import MockAIClient


def test_mock_ai_extracts_known_eval_fields():
    dataset = json.loads(Path("evaluation/case_extraction_eval.json").read_text(encoding="utf-8"))
    client = MockAIClient()
    total_checks = 0
    passed_checks = 0

    for item in dataset:
        analysis = client.analyze_documents(CaseCategory(item["category"]), item["text"])
        expected = item["expected"]
        checks = [
            analysis.company == expected["company"],
            analysis.disputed_amount == Decimal(expected["amount"]),
            item["category"] == expected["claim_type"],
            expected["reason_contains"] in analysis.dispute_reason.lower(),
        ]
        total_checks += len(checks)
        passed_checks += sum(checks)

    assert passed_checks / total_checks >= 0.8
