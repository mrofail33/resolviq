# Structured Extraction Evaluation

Safe interview claim:

> I added a small known-answer evaluation set for document extraction and test it against the structured JSON output.

## Final AI flow

```text
Document -> LLM/mock LLM -> structured JSON -> Pydantic validation -> PostgreSQL
```

## What the evaluation checks

The dataset lives at `backend/evaluation/case_extraction_eval.json`.

Each known document checks:

- company
- disputed amount
- claim type
- claim reason

The test is `backend/tests/test_evaluation.py`. It runs in CI and verifies that the extraction flow returns the expected structured fields.

## What not to claim yet

- Do not claim production model evaluation.
- Do not claim large-scale benchmark coverage.
- Do not claim RAG or vector search.

## Simple next upgrade

Add 20-30 more realistic documents and report per-field accuracy for company, amount, date, claim type, and reason.
