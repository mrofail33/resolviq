# Interview Proof

Safe interview claim:

> I built a React and FastAPI app that turns uploaded refund, warranty, or travel documents into organized cases with extracted text, structured AI-style analysis, generated claim drafts, PostgreSQL persistence, and a dashboard workflow.

## What the repo proves

- React dashboard for creating, selecting, and viewing cases.
- FastAPI backend with case, document, status, and deadline endpoints.
- Text/PDF extraction before analysis.
- Pydantic validation for structured analysis output.
- Known-answer extraction evaluation in `backend/evaluation/case_extraction_eval.json`.
- SQLAlchemy models for users, cases, documents, deadlines, evidence, missing info, and important dates.
- Mock AI mode by default so the app is demoable without paid API access.
- Optional OpenAI mode behind `AI_PROVIDER=openai`.
- Optional demo API-key auth boundary through `DEMO_API_KEY`, `X-API-Key`, and `X-Demo-User`.
- Backend workflow tests in `backend/tests/`.
- CI that runs backend tests and frontend build checks.

## Mock AI vs real AI

Default mode is `AI_PROVIDER=mock`. That is intentional for demos and tests. It proves the app workflow without depending on a paid API key.

Real provider mode exists through the OpenAI client abstraction, but should be described as optional integration, not the core proof.

## Final AI and full-stack flows

```text
Document -> LLM/mock LLM -> structured JSON -> validation -> PostgreSQL
```

```text
User -> React -> demo authentication -> FastAPI -> PostgreSQL -> LLM/mock LLM
```

## What not to claim yet

- Production claims management system.
- Production authentication or multi-tenant security.
- Production AI reliability.
- Background jobs or advanced document processing.

## Simple next upgrade

Add login and user-owned cases, then add Alembic migrations for database changes.
