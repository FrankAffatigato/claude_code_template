# Niche Scout

A small tool for finding e-commerce keyword niches: decent search demand, low
competition. Enter a seed keyword, get back a scored, sortable list of related
keywords plus a scatter plot of demand vs. competition.

## Why this repo looks the way it does

This repo is set up as a template for working with Claude Code (or another coding
agent) across multiple sessions. The files are split by how often they change:

| File | Changes | Purpose |
|---|---|---|
| `CLAUDE.md` | rarely | Standing instructions: stack, commands, conventions. Loaded every session. |
| `docs/plan.md` | occasionally | The build plan: phases, technical approach, what "done" means for each phase. |
| `docs/architecture.md` | occasionally | How the pieces fit together, with a diagram. |
| `docs/data-sources.md` | occasionally | Which keyword data providers are used, their limits, and fallback plan. |
| `docs/decisions.md` | occasionally | Log of decisions made mid-build and why, so they are not re-litigated. |
| `docs/state.md` | every session | What's done, in progress, blocked, and next. Read this first. |
| `docs/resources.md` | rarely | Where to learn this workflow: Claude Code docs, best-practices posts, how the concepts map to this repo's files. |
| `.claude/skills/` | rarely | Step-by-step procedures the agent should follow for recurring tasks. |
| `.claude/commands/` | rarely | Short slash commands for common actions (`/resume`, `/checkpoint`). |
| `.claude/agents/` | rarely | Subagent definitions (e.g. a code reviewer with narrower tools). |

If you're picking this up in a new session (human or AI), the order to read things in
is: `CLAUDE.md` -> `docs/state.md` -> `docs/plan.md` (just the current phase) ->
start working.

## Local setup

```bash
cp .env.example .env          # fill in provider API keys
make backend                  # http://localhost:8000
make frontend                 # http://localhost:5173 (separate terminal)
make seed                     # optional: load sample keyword data
```

## Project layout

```
backend/
  main.py                 FastAPI app, route registration only
  db.py                    SQLAlchemy engine/session setup
  models.py                ORM models: Keyword, Niche, Snapshot
  scoring.py                normalize() and opportunity_score()
  providers/
    base.py                 KeywordProvider protocol
    autocomplete.py         Free-tier suggestion scraper
    metrics_api.py          Paid keyword-metrics provider
  routes/
    keywords.py
    niches.py
  services/
    keyword_service.py      Orchestrates providers -> scoring -> DB
frontend/
  src/
    App.tsx
    components/
      SeedForm.tsx
      OpportunityTable.tsx
      OpportunityChart.tsx
    api.ts
docs/
  plan.md
  architecture.md
  data-sources.md
  decisions.md
  state.md
.claude/
  skills/
    build-from-plan/
    add-data-provider/
  commands/
    resume.md
    checkpoint.md
  agents/
    code-reviewer.md
  settings.json
```
