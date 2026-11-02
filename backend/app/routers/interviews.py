import base64
import uuid

import jwt
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from starlette.concurrency import run_in_threadpool

from app.core.deps import get_current_user
from app.core.errors import AppError
from app.core.ratelimit import hit
from app.core.security import decode_access_token
from app.db import SessionLocal, get_db
from app.models import InterviewSession, User
from app.schemas.common import InterviewAnswerIn, InterviewStartIn, InterviewTurnOut, ReportOut
from app.services import interviews as svc
from app.services import reports
from app.services.speech import get_speech

router = APIRouter(tags=["interviews"])
MAX_AUDIO_BYTES = 10 * 1024 * 1024


def _turn(t) -> dict:
    return {"seq": t.seq, "speaker": t.speaker, "stage": t.stage, "text": t.text, "is_followup": t.is_followup,
            "audio_url": t.audio_url}


@router.post("/interviews", status_code=201)
def start(body: InterviewStartIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Start an interview (deducts a credit). The response includes the first interviewer question."""
    hit(f"interview_start:{user.id}", 5, 60)
    s = svc.start(db, user, role_id=body.role_id, level=body.level, language=body.language, mode=body.mode,
                  job_description=body.job_description, resume_text=body.resume_text,
                  use_profile_resume=body.use_profile_resume)
    return svc.state(db, user, s.id)


@router.get("/interviews/{session_id}")
def get_interview(session_id: uuid.UUID, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return svc.state(db, user, session_id)


@router.post("/interviews/{session_id}/answer", response_model=InterviewTurnOut)
@router.post("/interviews/{session_id}/turns", response_model=InterviewTurnOut, include_in_schema=False)
def answer(session_id: uuid.UUID, body: InterviewAnswerIn, user: User = Depends(get_current_user),
           db: Session = Depends(get_db)):
    """Text-mode REST alternative to the WebSocket: send an answer, get the next question."""
    hit(f"interview_turn:{user.id}", 30, 60)
    out = svc.answer(db, user, session_id, body.text, body.duration_sec)
    return {"done": out["done"], "turn": _turn(out["turn"]), "report_id": out["report_id"]}


@router.post("/interviews/{session_id}/resume")
def resume(session_id: uuid.UUID, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Reconnect after a disconnect (allowed once, within 10 minutes)."""
    svc.resume(db, user, session_id)
    return svc.state(db, user, session_id)


@router.post("/interviews/{session_id}/end")
def end(session_id: uuid.UUID, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """End the interview and trigger the evaluation report."""
    r = svc.end(db, user, session_id)
    return {"interview_id": session_id, "report_id": r.id if r else None, "report_status": r.status if r else None}


@router.get("/interviews/{session_id}/report", response_model=ReportOut)
def interview_report(session_id: uuid.UUID, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    r = svc.report_for_session(db, user, session_id)
    reports.mark_viewed(db, user, r)
    return reports.serialize(r)


# ---- WebSocket ------------------------------------------------------------------------------------------------------
def _ws_user(token: str) -> uuid.UUID:
    try:
        return uuid.UUID(decode_access_token(token)["sub"])
    except (jwt.PyJWTError, KeyError, ValueError):
        raise AppError(401, "invalid_token", "Invalid or expired token")


def _ws_connect(user_id: uuid.UUID, session_id: uuid.UUID) -> dict:
    with SessionLocal() as db:
        user = db.get(User, user_id)
        if user is None or user.status != "active":
            raise AppError(401, "invalid_token", "Account not available")
        s = db.get(InterviewSession, session_id)
        if s is None or s.user_id != user.id:
            raise AppError(404, "not_found", "Interview not found")
        if s.status == "active":
            svc.resume(db, user, session_id)
        return svc.state(db, user, session_id)


def _ws_answer(user_id, session_id, text: str, duration: float | None) -> dict:
    with SessionLocal() as db:
        user = db.get(User, user_id)
        out = svc.answer(db, user, session_id, text, duration)
        return {"done": out["done"], "turn": _turn(out["turn"]), "report_id": str(out["report_id"]) if out["report_id"] else None}


def _ws_end(user_id, session_id) -> str | None:
    with SessionLocal() as db:
        r = svc.end(db, db.get(User, user_id), session_id)
        return str(r.id) if r else None


def _ws_disconnected(session_id) -> None:
    with SessionLocal() as db:
        svc.mark_disconnected(db, session_id)


def _jsonable(d):
    import json

    return json.loads(json.dumps(d, default=str))


@router.websocket("/interviews/{session_id}/stream")
async def stream(websocket: WebSocket, session_id: uuid.UUID, token: str | None = None):
    """Real-time interview channel (text and audio). See docs/API.md "Interview WebSocket protocol"."""
    await websocket.accept()
    try:
        user_id = _ws_user(token or "")
        state = await run_in_threadpool(_ws_connect, user_id, session_id)
    except AppError as e:
        await websocket.send_json({"type": "error", "code": e.code, "message": e.message})
        await websocket.close(code=4401 if e.status_code == 401 else 4404 if e.status_code == 404 else 4409)
        return
    await websocket.send_json({"type": "state", "interview": _jsonable(state)})
    if state["status"] != "active":
        await websocket.close(code=1000)
        return

    speech, audio, mode = get_speech(), bytearray(), state["mode"]
    try:
        while True:
            msg = await websocket.receive_json()
            kind = msg.get("type")
            try:
                if kind == "ping":
                    await websocket.send_json({"type": "pong"})
                    continue
                if kind == "audio_chunk":
                    audio.extend(base64.b64decode(msg.get("data", "")))
                    if len(audio) > MAX_AUDIO_BYTES:
                        audio.clear()
                        raise AppError(413, "audio_too_large", "Answer audio is too long")
                    continue
                if kind == "end":
                    report_id = await run_in_threadpool(_ws_end, user_id, session_id)
                    await websocket.send_json({"type": "ended", "report_id": report_id})
                    await websocket.close(code=1000)
                    return
                if kind == "audio_end":
                    text = await run_in_threadpool(speech.transcribe, bytes(audio), state["language"], msg.get("mime"))
                    audio.clear()
                    await websocket.send_json({"type": "transcript", "text": text})
                elif kind == "answer":
                    text = msg.get("text", "")
                else:
                    raise AppError(422, "unknown_message", f"Unknown message type {kind}")
                out = await run_in_threadpool(_ws_answer, user_id, session_id, text, msg.get("duration_sec"))
                reply = {"type": "question", "turn": out["turn"]}
                if mode == "voice":
                    tts = await run_in_threadpool(speech.synthesize, out["turn"]["text"], state["language"])
                    reply["audio"] = None if tts is None else base64.b64encode(tts).decode()
                    reply["tts"] = "server" if tts else "client"  # client speaks the text with on-device TTS
                await websocket.send_json(reply)
                if out["done"]:
                    await websocket.send_json({"type": "ended", "report_id": out["report_id"]})
                    await websocket.close(code=1000)
                    return
            except AppError as e:
                await websocket.send_json({"type": "error", "code": e.code, "message": e.message})
                if e.code == "interview_ended":
                    await websocket.close(code=4409)
                    return
    except WebSocketDisconnect:
        await run_in_threadpool(_ws_disconnected, session_id)
