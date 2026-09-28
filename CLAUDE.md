# Niche Scout

Keyword opportunity finder for e-commerce products. Given a seed keyword or category,
the app pulls related search terms, estimates demand and competition for each, and
scores them so a seller can spot low-competition / decent-demand niches.

Read `docs/plan.md` before starting any work session. Read `docs/state.md` to see
what is already built and what is next. Update `docs/state.md` at the end of every
session, not just when a feature is finished.

## Stack

- Backend: Python 3.11, FastAPI, SQLite (via SQLAlchemy)
- Data collection: `httpx` against autocomplete/suggestion endpoints + a keyword-metrics
  provider (see `docs/data-sources.md` for which one and why)
- Scoring: plain Python in `backend/scoring.py`, no ML model v1
- Frontend: React + Vite, plain fetch calls to the backend, Recharts for the opportunity
  scatter plot
- Tests: pytest for backend, Vitest for frontend

## Commands

- Backend dev server: `make backend` (runs `uvicorn backend.main:app --reload`)
- Frontend dev server: `make frontend` (runs `npm run dev` inside `frontend/`)
- Run backend tests: `make test` (runs `pytest -q`)
- Lint: `make lint` (runs `ruff check backend` and `npm run lint` in `frontend/`)
- Seed local DB with sample data: `make seed`

## Conventions

- All keyword scores are 0-100 integers, never floats in the API response.
- Backend routes live under `backend/routes/`, one file per resource (`keywords.py`,
  `niches.py`). Do not put route logic in `main.py`.
- Every data provider (autocomplete scraper, metrics API) implements the
  `KeywordProvider` protocol in `backend/providers/base.py`. Never call a provider's
  raw client from a route; always go through `backend/services/keyword_service.py`.
- Frontend components are function components with hooks, no class components.
- Money and percentages are formatted in the frontend, never in the backend response.
- No secrets in code. All provider API keys come from environment variables listed in
  `.env.example`.

## Gotchas

- The free-tier autocomplete scraper is rate-limited to ~1 request/second. The
  `KeywordProvider` implementations must queue and throttle themselves; do not add
  retry loops in the route handlers.
- SQLite does not enforce foreign keys by default. `backend/db.py` turns this on with
  `PRAGMA foreign_keys=ON` on every connection; do not remove that.
- Competition score and search volume are on different scales from different
  providers. Always run raw provider output through `backend/scoring.py::normalize()`
  before storing it. Never store a raw provider score directly in the `keywords` table.

## Workflow for AI sessions

1. Read `docs/state.md` for current status.
2. Read `docs/plan.md` for the relevant phase (do not re-read the whole file if the
   phase is already clear from state.md).
3. Do the work.
4. Run `make test` and `make lint` before considering a task done.
5. Update `docs/state.md`: move finished items to Done, note anything you decided or
   discovered in `docs/decisions.md` if it changes future work.
6. If you built something not in `docs/plan.md`, add it there so the plan stays the
   source of truth.
