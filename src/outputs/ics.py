from __future__ import annotations
from datetime import datetime
from typing import Iterable

from ..models import Contest


def _format_dt(dt: datetime) -> str:
    # iCalendar requires UTC in Zulu format for floating UTC; we'll use UTC timestamps
    return dt.strftime("%Y%m%dT%H%M%SZ")


def contests_to_ics(contests: Iterable[Contest], calendar_name: str = "Competitive Programming Contests") -> str:
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//contest-scraper//EN",
        f"X-WR-CALNAME:{calendar_name}",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
    ]

    for c in contests:
        uid = f"cf-{c.id}@contest-scraper"
        lines.extend([
            "BEGIN:VEVENT",
            f"UID:{uid}",
            f"SUMMARY:Codeforces: {c.name}",
            f"DTSTART:{_format_dt(c.start_time_utc)}",
            f"DTEND:{_format_dt(c.end_time_utc)}",
            f"DESCRIPTION:{c.url}\\nType: {c.type}",
            f"URL:{c.url}",
            f"DTSTAMP:{_format_dt(c.start_time_utc)}",
            "END:VEVENT",
        ])

    lines.append("END:VCALENDAR")
    return "\r\n".join(lines) + "\r\n"
