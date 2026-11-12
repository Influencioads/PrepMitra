from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.languages import LANGUAGES
from app.db import get_db
from app.services import catalog, payments
from app.services.attempts import ANTI_CHEAT_EVENTS
from app.services.catalog import CATEGORIES
from app.services.profile import CONSENT_TYPES, POLICY_VERSION
from app.schemas.me import EDUCATION_LEVELS

router = APIRouter(tags=["catalog"])


@router.get("/exams")
def list_exams(category: str | None = None, q: str | None = Query(default=None, max_length=80),
               language: str | None = None, limit: int = Query(default=50, ge=1, le=100),
               offset: int = Query(default=0, ge=0), db: Session = Depends(get_db)):
    """Published exams. Filter by category, search by name, filter by available language."""
    return catalog.list_exams(db, category=category, q=q, language=language, limit=limit, offset=offset) | {
        "limit": limit, "offset": offset}


@router.get("/exams/{exam_ref}")
def exam_detail(exam_ref: str, db: Session = Depends(get_db)):
    """Exam detail by id or slug: pattern, sections, duration, marks, negative marking, price, sample question."""
    return catalog.exam_detail(db, exam_ref)


@router.get("/interview-roles")
def interview_roles(q: str | None = None, db: Session = Depends(get_db)):
    return {"items": catalog.list_roles(db, q)}


@router.get("/interview-roles/{role_ref}")
def interview_role(role_ref: str, db: Session = Depends(get_db)):
    return catalog.role_detail(db, role_ref)


@router.get("/plans")
def plans(db: Session = Depends(get_db)):
    return {"items": payments.list_plans(db), "currency": "INR", "gst_inclusive": True}


@router.get("/meta")
def meta():
    """Static enums for web and mobile forms, so clients never hard-code them."""
    return {
        "languages": [{"code": k, **v} for k, v in LANGUAGES.items()],
        "exam_categories": [{"key": k, "label": v} for k, v in CATEGORIES.items()],
        "education_levels": list(EDUCATION_LEVELS),
        "interview_levels": ["fresher", "1-3", "3-5"],
        "consent_types": list(CONSENT_TYPES), "policy_version": POLICY_VERSION,
        "anti_cheat_event_types": sorted(ANTI_CHEAT_EVENTS),
        "question_report_reasons": ["wrong_answer", "unclear", "bad_translation", "other"],
        "client_platforms": ["web", "android", "ios"],
    }


POLICIES = {
    "privacy": "Privacy policy (DPDP Act 2023). DRAFT - to be reviewed by an Indian lawyer before launch. "
               "We collect your phone, profile, answers and interview transcripts to run mock tests and write your "
               "reports. Data is hosted in India. You can download or delete your data from your profile at any time. "
               "Recruiter sharing is off unless you turn it on, and you can withdraw it anytime.",
    "terms": "Terms of use. DRAFT - to be reviewed by an Indian lawyer before launch. The service is for users aged 18 "
             "and above. Mock tests are based on public exam patterns and are not affiliated with any exam body.",
    "refund": "Refund and cancellation policy. DRAFT. A credit is used only when you start an attempt. If an attempt "
              "fails for technical reasons, or the report is not ready within 10 minutes, the credit is restored "
              "automatically. You can cancel auto-renewal anytime; the plan stays active until expiry.",
    "ai-notice": "AI-generated content notice. Questions, explanations, reports and interview feedback are generated "
                 "by AI and checked by automated verification and sample expert review. Report any wrong question "
                 "with the Report button.",
}


@router.get("/policies/{kind}")
def policy(kind: str):
    from app.core.errors import not_found

    if kind not in POLICIES:
        raise not_found("Policy")
    return {"kind": kind, "version": POLICY_VERSION, "status": "draft", "text": POLICIES[kind]}
