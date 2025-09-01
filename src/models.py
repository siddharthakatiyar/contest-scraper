from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class Contest:
    id: int
    name: str
    type: str
    platform: str
    url: str
    start_time_utc: datetime
    duration: timedelta

    @property
    def end_time_utc(self) -> datetime:
        return self.start_time_utc + self.duration
