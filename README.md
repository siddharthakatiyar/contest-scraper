# Contest Scraper → ICS feed

Generates an iCalendar (.ics) feed for upcoming Codeforces contests. A GitHub Actions workflow runs twice daily and publishes to GitHub Pages, so anyone can subscribe in Google Calendar (or any calendar app) without credentials.

## What you get
- Codeforces API (no scraping)
- Upcoming contests only, within a configurable window (default 60 days)
- Clean ICS feed at `https://<your-user>.github.io/<repo>/codeforces.ics`
- Works for anyone; just subscribe the URL in your calendar app

## Quick start (as a template)
1. Use this repo as a template (GitHub → Use this template).
2. Enable GitHub Pages: Settings → Pages → Branch: `gh-pages`.
3. The scheduled workflow is already set to run twice daily. You can also trigger it manually (Actions → Run workflow).
4. After it runs, visit your Pages site (e.g., `https://<you>.github.io/contest-scraper/`). Copy the `codeforces.ics` URL and add it to your calendar:
   - Google Calendar → Settings → Add calendar → From URL

## Configuration
Environment variables (optional; set in Actions → Variables):
- `TIMEZONE` (default: UTC)
- `DAYS_AHEAD` (default: 60)
- `INCLUDE_TYPES` (CSV, e.g., `CF,ICPC`)
- `EXCLUDE_KEYWORDS` (CSV, e.g., `Practice`)

## Local dev
- Python 3.10+
- Install deps: `pip install -r requirements.txt`
- Run: `python -m src.main`
- Output: `dist/codeforces.ics` and a simple `dist/index.html`

## Roadmap
- Add AtCoder, CodeChef, LeetCode, etc.
- Optional: direct Google Calendar sync (OAuth) for users who want instant updates (not just subscribed ICS refresh cadence).

## Similar services
- CLIST (clist.by) provides contest listings and ICS feeds. This repo is a minimal OSS alternative focused on transparency and customizability.

## License
MIT
