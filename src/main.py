from __future__ import annotations
from datetime import datetime, timedelta, timezone
import os

from .config import settings
from .providers.codeforces import fetch_upcoming
from .outputs.ics import contests_to_ics
from .models import Contest


def filter_contests(now_utc: datetime, contests: list[Contest]) -> list[Contest]:
    res: list[Contest] = []
    for c in contests:
        if c.start_time_utc < now_utc:
            continue
        if (c.start_time_utc - now_utc) > timedelta(days=settings.days_ahead):
            continue
        if settings.include_types and c.type not in settings.include_types:
            continue
        if settings.exclude_keywords and any(k.lower() in c.name.lower() for k in settings.exclude_keywords):
            continue
        res.append(c)
    return res


def write_ics(path: str, contents: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(contents)


def _get_base_url() -> str | None:
    # Prefer explicit BASE_URL, otherwise try to infer from GitHub Actions envs
    base = os.getenv("BASE_URL")
    if base:
        return base.rstrip("/")
    owner = os.getenv("GITHUB_REPOSITORY_OWNER")
    repo_full = os.getenv("GITHUB_REPOSITORY")  # e.g. owner/repo
    if owner and repo_full and "/" in repo_full:
        repo = repo_full.split("/", 1)[1]
        return f"https://{owner}.github.io/{repo}"
    return None


def write_index(path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    base_url = _get_base_url()
    if base_url:
        ics_url = f"{base_url}/codeforces.ics"
    else:
        ics_url = "https://<your-user>.github.io/<repo>/codeforces.ics"
    html = """
<!doctype html>
<html>
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width,initial-scale=1" />
        <title>Contest ICS Feeds</title>
        <style>body{font-family:system-ui,Segoe UI,Arial,sans-serif;margin:40px;max-width:760px}code{padding:.2em .4em;background:#f5f5f5;border-radius:4px}</style>
    </head>
    <body>
        <h1>Contest ICS Feeds</h1>
    <p>Subscribe this URL in your calendar app:</p>
    <p><code>{ICS_URL}</code></p>
    <p><a href="{ICS_URL}">Open codeforces.ics</a></p>
        <p>Tip: In Google Calendar, use <b>Settings &gt; Add calendar &gt; From URL</b>.</p>
    </body>
 </html>
""".strip()
    html = html.replace("{ICS_URL}", ics_url)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)


def main():
    now_utc = datetime.now(timezone.utc)
    contests = fetch_upcoming()
    contests = filter_contests(now_utc, contests)

    ics = contests_to_ics(contests)

    out_dir = os.getenv("OUTPUT_DIR", "dist")
    out_file = os.path.join(out_dir, "codeforces.ics")
    write_ics(out_file, ics)
    write_index(os.path.join(out_dir, "index.html"))

    print(f"Wrote {len(contests)} contests to {out_file}")


if __name__ == "__main__":
    main()
