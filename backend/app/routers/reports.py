import uuid

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.core.ratelimit import limit
from app.db import get_db
from app.models import User
from app.schemas.common import RatingIn, ReportOut
from app.services import reports as svc

router = APIRouter(tags=["reports"])


@router.get("/reports/{report_id}", response_model=ReportOut)
def get_report(report_id: uuid.UUID, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    r = svc.own_report(db, user, report_id)
    svc.mark_viewed(db, user, r)
    return svc.serialize(r)


@router.post("/reports/{report_id}/rating", response_model=ReportOut)
def rate(report_id: uuid.UUID, body: RatingIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return svc.serialize(svc.rate(db, user, report_id, body.rating, body.comment))


@router.post("/reports/{report_id}/share", response_model=ReportOut)
def share(report_id: uuid.UUID, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Creates (or extends) a public share link valid for 30 days."""
    return svc.serialize(svc.share(db, user, report_id))


@router.delete("/reports/{report_id}/share", status_code=204)
def unshare(report_id: uuid.UUID, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    svc.unshare(db, user, report_id)


@router.post("/reports/{report_id}/retry", response_model=ReportOut)
def retry(report_id: uuid.UUID, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return svc.serialize(svc.retry(db, user, report_id))


@router.get("/reports/{report_id}/pdf", response_class=Response)
def report_pdf(report_id: uuid.UUID, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    data = svc.pdf_bytes(db, svc.own_report(db, user, report_id))
    return Response(data, media_type="application/pdf",
                    headers={"Content-Disposition": f'attachment; filename="report-{report_id}.pdf"'})


@router.get("/shared/reports/{token}", dependencies=[Depends(limit("shared", 60))])
def shared(token: str, db: Session = Depends(get_db)):
    """Public, unauthenticated view of a shared report (no personal data)."""
    return svc.public_view(db, svc.by_share_token(db, token))


@router.get("/shared/reports/{token}/pdf", response_class=Response, dependencies=[Depends(limit("shared", 60))])
def shared_pdf(token: str, db: Session = Depends(get_db)):
    data = svc.pdf_bytes(db, svc.by_share_token(db, token))
    return Response(data, media_type="application/pdf", headers={"Content-Disposition": 'inline; filename="report.pdf"'})
