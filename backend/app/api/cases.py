from pathlib import Path
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.session import get_db
from app.models.case import (
    Case,
    Deadline,
    Document,
    EvidenceItem,
    ImportantDate,
    MissingInformation,
    User,
)
from app.schemas.case import CaseCreate, CaseRead, CaseStatusUpdate, DeadlineCreate, DeadlineRead
from app.schemas.case import StructuredDate
from app.services.ai import get_ai_client
from app.services.pdf import extract_text_from_upload

router = APIRouter(prefix="/cases", tags=["cases"])


@router.get("", response_model=list[CaseRead])
def list_cases(db: Session = Depends(get_db)) -> list[CaseRead]:
    cases = db.scalars(select(Case).order_by(Case.created_at.desc())).all()
    return [_case_to_read(db, case) for case in cases]


@router.post("", response_model=CaseRead, status_code=status.HTTP_201_CREATED)
def create_case(payload: CaseCreate, db: Session = Depends(get_db)) -> CaseRead:
    user = db.scalar(select(User).where(User.email == payload.user_email))
    if user is None:
        user = User(email=payload.user_email, full_name=payload.user_full_name)
        db.add(user)
        db.flush()

    case = Case(user_id=user.id, title=payload.title, category=payload.category)
    db.add(case)
    db.commit()
    db.refresh(case)
    return _case_to_read(db, case)


@router.get("/{case_id}", response_model=CaseRead)
def get_case(case_id: int, db: Session = Depends(get_db)) -> CaseRead:
    case = db.get(Case, case_id)
    if case is None:
        raise HTTPException(status_code=404, detail="Case not found")
    return _case_to_read(db, case)


@router.patch("/{case_id}/status", response_model=CaseRead)
def update_case_status(case_id: int, payload: CaseStatusUpdate, db: Session = Depends(get_db)) -> CaseRead:
    case = db.get(Case, case_id)
    if case is None:
        raise HTTPException(status_code=404, detail="Case not found")
    case.status = payload.status
    db.commit()
    db.refresh(case)
    return _case_to_read(db, case)


@router.post("/{case_id}/documents", response_model=CaseRead)
async def upload_document(
    case_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> CaseRead:
    case = db.get(Case, case_id)
    if case is None:
        raise HTTPException(status_code=404, detail="Case not found")

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Uploaded document is empty")

    try:
        extracted_text = extract_text_from_upload(file.filename or "upload.txt", content)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    settings = get_settings()
    Path(settings.upload_dir).mkdir(parents=True, exist_ok=True)
    safe_name = Path(file.filename or "upload.txt").name
    Path(settings.upload_dir, f"case-{case_id}-{safe_name}").write_bytes(content)

    document = Document(
        case_id=case.id,
        filename=safe_name,
        content_type=file.content_type or "application/octet-stream",
        extracted_text=extracted_text,
    )
    db.add(document)

    analysis = get_ai_client().analyze_documents(case.category, extracted_text)
    case.summary = analysis.summary
    case.company = analysis.company
    case.disputed_amount = analysis.disputed_amount
    case.dispute_reason = analysis.dispute_reason
    case.generated_draft = get_ai_client().generate_draft(case.category, analysis)

    _replace_analysis_rows(db, case.id, analysis)
    db.commit()
    db.refresh(case)
    return _case_to_read(db, case)


@router.post("/{case_id}/deadlines", response_model=DeadlineRead, status_code=status.HTTP_201_CREATED)
def create_deadline(case_id: int, payload: DeadlineCreate, db: Session = Depends(get_db)) -> DeadlineRead:
    case = db.get(Case, case_id)
    if case is None:
        raise HTTPException(status_code=404, detail="Case not found")
    deadline = Deadline(case_id=case.id, label=payload.label, due_date=payload.due_date)
    db.add(deadline)
    db.commit()
    db.refresh(deadline)
    return DeadlineRead.model_validate(deadline)


def _replace_analysis_rows(db: Session, case_id: int, analysis) -> None:
    for model in (EvidenceItem, MissingInformation, ImportantDate):
        for row in db.scalars(select(model).where(model.case_id == case_id)).all():
            db.delete(row)

    for item in analysis.evidence:
        db.add(EvidenceItem(case_id=case_id, label=item))
    for item in analysis.missing_information:
        db.add(MissingInformation(case_id=case_id, label=item))
    for item in analysis.important_dates:
        db.add(ImportantDate(case_id=case_id, label=item.label, date_value=item.date))


def _case_to_read(db: Session, case: Case) -> CaseRead:
    data = CaseRead.model_validate(case)
    data.evidence = [
        item.label for item in db.scalars(select(EvidenceItem).where(EvidenceItem.case_id == case.id)).all()
    ]
    data.missing_information = [
        item.label
        for item in db.scalars(select(MissingInformation).where(MissingInformation.case_id == case.id)).all()
    ]
    data.important_dates = [
        StructuredDate(label=item.label, date=item.date_value)
        for item in db.scalars(select(ImportantDate).where(ImportantDate.case_id == case.id)).all()
    ]
    return data
