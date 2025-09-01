from __future__ import annotations
import os
from dataclasses import dataclass
from typing import List, Optional


def _getenv(name: str, default: Optional[str] = None) -> Optional[str]:
    v = os.getenv(name)
    return v if v not in (None, "") else default


def _getenv_int(name: str, default: int) -> int:
    v = os.getenv(name)
    try:
        return int(v) if v is not None and v != "" else int(default)
    except Exception:
        return int(default)


def _getenv_bool(name: str, default: bool) -> bool:
    v = os.getenv(name)
    if v is None or v == "":
        return default
    return str(v).strip().lower() in {"1", "true", "yes", "on"}


def _getenv_csv(name: str) -> Optional[List[str]]:
    v = os.getenv(name)
    if not v:
        return None
    return [part.strip() for part in v.split(",") if part.strip()]


@dataclass
class Settings:
    # General
    timezone: str = _getenv("TIMEZONE", "UTC") or "UTC"
    days_ahead: int = _getenv_int("DAYS_AHEAD", 60)
    include_types: Optional[List[str]] = _getenv_csv("INCLUDE_TYPES")  # e.g., CF, ICPC
    exclude_keywords: Optional[List[str]] = _getenv_csv("EXCLUDE_KEYWORDS")  # e.g., Practice
    dry_run: bool = _getenv_bool("DRY_RUN", False)

    # Google Calendar (optional; used only if upserting to GCal)
    calendar_id: str = _getenv("GOOGLE_CALENDAR_ID", "primary") or "primary"
    reminder_minutes: int = _getenv_int("REMINDER_MINUTES", 30)


settings = Settings()
