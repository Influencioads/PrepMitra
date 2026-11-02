"""Swappable external providers (SMS, file storage). Dev implementations need no credentials."""

import logging
import uuid
from pathlib import Path
from typing import Protocol

from app.config import get_settings

log = logging.getLogger(__name__)


class SmsProvider(Protocol):
    def send_otp(self, phone: str, code: str) -> None: ...


class DevSmsProvider:
    """Sends nothing. In development the OTP is returned in the API response instead (never logged)."""

    def send_otp(self, phone: str, code: str) -> None:
        log.info("dev sms: OTP issued for phone ending %s", phone[-4:])


def get_sms_provider() -> SmsProvider:
    # A DLT-registered Indian SMS provider plugs in here once credentials exist.
    return DevSmsProvider()


class LocalStorage:
    """Stores files under STORAGE_DIR. Swap for S3 (ap-south-1) in production."""

    def __init__(self, root: str | None = None):
        self.root = Path(root or get_settings().storage_dir)

    def save(self, folder: str, data: bytes, suffix: str) -> str:
        rel = Path(folder) / f"{uuid.uuid4().hex}{suffix}"
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return rel.as_posix()

    def read(self, rel: str) -> bytes:
        return (self.root / rel).read_bytes()

    def delete(self, rel: str) -> None:
        (self.root / rel).unlink(missing_ok=True)

    def abspath(self, rel: str) -> Path:
        return self.root / rel


def get_storage() -> LocalStorage:
    return LocalStorage()
