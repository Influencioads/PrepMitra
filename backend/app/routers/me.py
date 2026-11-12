from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db import get_db
from app.models import User
from app.schemas.me import ConsentIn, MeOut, MeUpdateIn, ProfileOut
from app.services import profile as svc

router = APIRouter(prefix="/me", tags=["me"])


def _me_out(db: Session, user: User) -> MeOut:
    p = user.profile
    missing = svc.missing_fields(db, user)
    return MeOut(
        id=user.id, phone=user.phone, email=user.email, name=user.name, dob=user.dob, state=user.state,
        preferred_language=user.preferred_language,
        is_admin=user.admin is not None, admin_role=user.admin.role if user.admin else None,
        profile=ProfileOut(
            education=p.education, stream=p.stream, target_exam_ids=p.target_exam_ids or [],
            target_role_ids=p.target_role_ids or [], experience_years=p.experience_years,
            has_resume=bool(p.resume_path),
        ),
        consents=svc.current_consents(db, user.id),
        profile_complete=not missing,
        missing_fields=missing,
    )


@router.get("", response_model=MeOut)
def get_me(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return _me_out(db, user)


@router.patch("", response_model=MeOut)
def patch_me(body: MeUpdateIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    svc.update_me(db, user, body.model_dump(exclude_unset=True))
    return _me_out(db, user)


@router.delete("", status_code=204)
def delete_me(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    svc.delete_account(db, user)


@router.post("/consents")
def post_consents(body: ConsentIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return svc.record_consents(db, user, body.model_dump())


@router.delete("/consents/{consent_type}", status_code=204)
def withdraw(consent_type: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    svc.withdraw_consent(db, user, consent_type)


@router.get("/export")
def export(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return svc.export_data(db, user)


@router.post("/resume", response_model=MeOut)
async def upload_resume(file: UploadFile = File(...), user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    data = await file.read(svc.get_settings().max_resume_bytes + 1)
    svc.save_resume(db, user, file.filename or "", data)
    return _me_out(db, user)


@router.delete("/resume", response_model=MeOut)
def remove_resume(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    svc.delete_resume(db, user)
    return _me_out(db, user)


uploads = APIRouter(prefix="/uploads", tags=["me"])


@uploads.post("/resume")
async def upload_resume_for_interview(file: UploadFile = File(...), user: User = Depends(get_current_user),
                                      db: Session = Depends(get_db)):
    """PDF/DOCX up to 5 MB. Stored privately, text extracted for the AI interviewer. Phone numbers and emails are
    removed before any text is sent to the AI; `preview` shows exactly that cleaned text."""
    from app.ai.safety import strip_pii

    data = await file.read(svc.get_settings().max_resume_bytes + 1)
    svc.save_resume(db, user, file.filename or "", data)
    text = user.profile.resume_text or ""
    return {"has_resume": True, "filename": file.filename, "characters": len(text),
            "preview": strip_pii(text)[:600], "pii_removed_before_ai": True}
