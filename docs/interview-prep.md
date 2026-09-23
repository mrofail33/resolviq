# Resolviq Interview Prep

## 30-second explanation

Resolviq is a full-stack AI application I built that turns unstructured consumer documents into organized dispute cases and helps users generate and track claims for issues like refunds, warranties, and travel.

## Simple architecture

The frontend is a React dashboard where users create cases, upload documents, review extracted details, edit a generated claim draft, update status, and track deadlines.

The backend is a FastAPI application. It receives case and document requests, extracts text from uploads, calls an AI service abstraction, validates the returned structure with Pydantic, and stores everything in a relational database.

PostgreSQL stores users, cases, uploaded documents, deadlines, evidence, missing information, and important dates. SQLAlchemy defines the models.

## Data flow

1. User creates a case in React.
2. React sends the title and category to FastAPI.
3. FastAPI stores the case in PostgreSQL.
4. User uploads a TXT or PDF document.
5. Backend extracts readable text.
6. AI service analyzes the text.
7. Pydantic validates the AI response.
8. Backend stores extracted fields and generates a draft.
9. React refreshes the dashboard with the organized case.

## Important files

- `backend/app/main.py`: creates the FastAPI app and registers routes.
- `backend/app/api/cases.py`: case, upload, status, and deadline endpoints.
- `backend/app/models/case.py`: database tables.
- `backend/app/schemas/case.py`: request, response, and AI validation schemas.
- `backend/app/services/ai.py`: mock AI and OpenAI-ready abstraction.
- `backend/app/services/pdf.py`: PDF and text extraction.
- `backend/tests/test_cases.py`: automated workflow tests.
- `frontend/src/App.tsx`: main dashboard state and workflow.
- `frontend/src/components/CaseDetail.tsx`: organized case view, upload, draft, and deadlines.

## What AI helped with

AI helped scaffold and organize the project quickly, suggest clean naming, generate starter tests, and create a professional dashboard layout.

## What the developer should understand

The developer should be able to explain:

- How React sends requests to FastAPI.
- Why only three categories are accepted.
- How SQLAlchemy maps Python classes to database tables.
- How uploaded files become extracted text.
- Why Pydantic validation matters when using AI output.
- How mock AI mode makes the project demoable without an API key.
- What each test proves.

## Common interviewer questions

### Why use Pydantic after the AI response?

AI output can be inconsistent. Pydantic forces the response into a predictable structure before the app stores or displays it. If fields are missing or malformed, the backend can reject or fall back safely.

### Why include mock AI mode?

It makes the project reliable for demos, tests, and local development. The app still shows the AI workflow without depending on paid API access or network availability.

### Why PostgreSQL?

The app has relational data: users have cases, cases have documents and deadlines, and extracted fields belong to cases. PostgreSQL is a practical production-style database for that structure.

### What would you improve next?

I would add real authentication, persistent draft editing, better document parsing for emails and images, richer deadline reminders, and Alembic migrations for production database changes.

### How is this more than a ChatGPT wrapper?

The AI is only one service inside a full application. Resolviq handles uploads, text extraction, validation, storage, case organization, status tracking, deadlines, and a dashboard workflow.

## Resume bullet options

- Built Resolviq, a React/FastAPI application that converts consumer dispute documents into organized refund, warranty, and travel claim cases.
- Implemented document upload, PDF/text extraction, structured AI analysis, Pydantic validation, PostgreSQL persistence, and generated dispute drafts.
- Added mock AI fallback and automated tests covering case creation, invalid input, structured validation, and document analysis workflow.
