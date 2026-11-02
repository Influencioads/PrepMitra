import uuid

from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.core.ratelimit import hit
from app.db import get_db
from app.models import User
from app.schemas.common import AnswersIn, AnswersOut, AttemptStartIn, EventsIn, QuestionReportIn, ReportOut
from app.services import attempts as svc
from app.services import questions, reports

router = APIRouter(tags=["exams"])


@router.post("/attempts", status_code=201)
def start(body: AttemptStartIn, response: Response, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Start an exam: deducts a credit (or uses the one-time free trial), assigns an unseen paper, starts the
    server timer. If an attempt for this exam is already in progress it is returned instead (HTTP 200, resumed=true)."""
    hit(f"attempt_start:{user.id}", 10, 60)
    attempt, resumed = svc.start_attempt(db, user, body.exam_id, body.language)
    if resumed:
        response.status_code = 200
    return svc.attempt_state(db, user, attempt.id) | {"resumed": resumed}


@router.get("/attempts")
def my_attempts(limit: int = Query(default=20, ge=1, le=100), offset: int = Query(default=0, ge=0),
                user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    items, total = svc.list_attempts(db, user, limit, offset)
    return {"items": items, "total": total, "limit": limit, "offset": offset}


@router.get("/attempts/{attempt_id}")
def get_attempt(attempt_id: uuid.UUID, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Resume: questions (chosen language + English toggle), saved answers and the server's remaining time."""
    return svc.attempt_state(db, user, attempt_id)


@router.get("/attempts/{attempt_id}/paper")
def get_paper(attempt_id: uuid.UUID, lang: str | None = None, user: User = Depends(get_current_user),
              db: Session = Depends(get_db)):
    """API Plan name for the paper: questions without answers, server end time, saved answers. `?lang=hi` for Hindi."""
    return svc.attempt_state(db, user, attempt_id, lang)


@router.put("/attempts/{attempt_id}/answers", response_model=AnswersOut)
def autosave(attempt_id: uuid.UUID, body: AnswersIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    hit(f"autosave:{user.id}", 240, 60)
    return svc.save_answers(db, user, attempt_id, body.to_items())


@router.post("/attempts/{attempt_id}/events")
def events(attempt_id: uuid.UUID, body: EventsIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return svc.log_events(db, user, attempt_id, [e.model_dump() for e in body.events])


@router.post("/attempts/{attempt_id}/submit")
def submit(attempt_id: uuid.UUID, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Submit (idempotent). Scores immediately; the AI report is generated in the background."""
    a = svc.submit(db, user, attempt_id)
    r = reports.report_for_attempt(db, user, a.id)
    return {"attempt_id": a.id, "status": a.status, "score": a.score, "max_score": a.max_score,
            "percentile": a.percentile, "report_id": r.id, "report_status": r.status}


@router.get("/attempts/{attempt_id}/report", response_model=ReportOut)
def attempt_report(attempt_id: uuid.UUID, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """AI report. Poll while status is "processing" (or wait for the result_ready push)."""
    r = reports.report_for_attempt(db, user, attempt_id)
    reports.mark_viewed(db, user, r)
    return reports.serialize(r)


@router.get("/attempts/{attempt_id}/review")
def review(attempt_id: uuid.UUID, language: str | None = None, user: User = Depends(get_current_user),
           db: Session = Depends(get_db)):
    """Question-by-question review with correct answers and explanations (after submission)."""
    return svc.review(db, user, attempt_id, language)


@router.post("/questions/{question_id}/flags", status_code=201)
@router.post("/questions/{question_id}/reports", status_code=201, include_in_schema=False)
def report_question(question_id: uuid.UUID, body: QuestionReportIn, user: User = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    hit(f"qreport:{user.id}", 30, 3600)
    r = questions.report_question(db, user, question_id, body.reason, body.details, body.language, body.attempt_id)
    return {"id": r.id, "status": r.status}
