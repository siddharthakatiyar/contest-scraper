from __future__ import annotations
import requests
from datetime import datetime, timedelta, timezone
from typing import List

from ..models import Contest

API_URL = "https://codeforces.com/api/contest.list?gym=false"


def fetch_upcoming() -> List[Contest]:
    r = requests.get(API_URL, timeout=20)
    r.raise_for_status()
    data = r.json()
    if data.get("status") != "OK":
        raise RuntimeError(f"Codeforces API error: {data}")

    contests: List[Contest] = []
    for item in data.get("result", []):
        if item.get("phase") != "BEFORE":
            continue
        cid = int(item["id"])  # has startTimeSeconds
        start_ts = int(item["startTimeSeconds"])  # UTC epoch
        duration_s = int(item.get("durationSeconds", 0))
        contests.append(
            Contest(
                id=cid,
                name=str(item.get("name", "Codeforces Contest")),
                type=str(item.get("type", "CF")),
                platform="codeforces",
                url=f"https://codeforces.com/contest/{cid}",
                start_time_utc=datetime.fromtimestamp(start_ts, tz=timezone.utc),
                duration=timedelta(seconds=duration_s if duration_s > 0 else 7200),
            )
        )
    return contests
