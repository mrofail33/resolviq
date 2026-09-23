from app.schemas.case import StructuredCaseAnalysis
from pydantic import ValidationError


def test_create_case(client):
    response = client.post("/cases", json={"title": "Refund denied by store", "category": "refund"})
    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Refund denied by store"
    assert body["category"] == "refund"
    assert body["status"] == "draft"


def test_invalid_category_rejected(client):
    response = client.post("/cases", json={"title": "Medical appeal", "category": "medical"})
    assert response.status_code == 422


def test_structured_ai_validation_rejects_short_summary():
    try:
        StructuredCaseAnalysis.model_validate(
            {
                "summary": "Too short",
                "company": "Store",
                "disputed_amount": 20,
                "important_dates": [],
                "dispute_reason": "Refund was refused",
                "evidence": ["receipt"],
                "missing_information": [],
            }
        )
    except ValidationError as exc:
        assert "summary" in str(exc)
    else:
        raise AssertionError("Expected validation error")


def test_document_case_workflow(client):
    created = client.post("/cases", json={"title": "BrightMart refund", "category": "refund"})
    case_id = created.json()["id"]

    upload = client.post(
        f"/cases/{case_id}/documents",
        files={
            "file": (
                "refund.txt",
                b"Receipt from BrightMart. Purchase date: 2026-07-02. Amount: $300. Email denial refused refund.",
                "text/plain",
            )
        },
    )
    assert upload.status_code == 200
    body = upload.json()
    assert body["company"] == "BrightMart"
    assert body["disputed_amount"] == "300.00"
    assert "Receipt" in body["evidence"]
    assert body["generated_draft"].startswith("Subject:")
