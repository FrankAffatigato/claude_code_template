# Architecture

## Overview

```
                    +---------------------+
                    |   Frontend (React)  |
                    |  SeedForm           |
                    |  OpportunityTable   |
                    |  OpportunityChart   |
                    +----------+----------+
                               | HTTP (fetch, JSON)
                               v
                    +---------------------+
                    |  FastAPI (backend)  |
                    |  routes/keywords.py |
                    |  routes/niches.py   |
                    +----------+----------+
                               |
                               v
                    +---------------------+
                    | keyword_service.py  |   <- orchestration only,
                    |  expand_seed()      |      no provider-specific code
                    +----------+----------+
                               |
                +--------------+--------------+
                v                             v
    +----------------------+     +--------------------------+
    | AutocompleteProvider |     |  MetricsApiProvider       |
    | (free suggestions)   |     |  (paid volume/competition)|
    +----------------------+     +--------------------------+
                               |
                               v
                    +---------------------+
                    |   scoring.py         |
                    |  normalize()         |
                    |  opportunity_score() |
                    +----------+----------+
                               |
                               v
                    +---------------------+
                    |  SQLite (db.py)      |
                    |  Keyword / Niche /   |
                    |  Snapshot tables     |
                    +---------------------+
```

## Request flow: a new seed search

1. User submits a seed keyword in `SeedForm`.
2. Frontend calls `POST /niches` with `{seed}`.
3. Route handler calls `keyword_service.expand_seed(seed)`.
4. `expand_seed`:
   a. Calls `AutocompleteProvider.suggest(seed)` to get a list of related keyword
      strings (throttled to 1 req/sec).
   b. Calls `MetricsApiProvider.metrics(keyword)` for each keyword to get raw
      volume/competition.
   c. Passes each raw metric through `scoring.normalize()`.
   d. Computes `scoring.opportunity_score()` across the full set.
   e. Persists a `Niche` row and a `Snapshot` row (keyword list + scores + timestamp)
      via SQLAlchemy.
5. Route returns the `Niche` id and scored keyword list as JSON.
6. Frontend renders `OpportunityTable` and `OpportunityChart` from the response.

## Why a provider protocol instead of calling APIs directly in routes

The free autocomplete source and the paid metrics API are both likely to change
(rate limits, pricing, deprecation). `backend/providers/base.py` defines a
`KeywordProvider` protocol so a new provider can be dropped in without touching
`keyword_service.py` or any route. See `.claude/skills/add-data-provider/SKILL.md`
for the procedure.

## Why SQLite and not Postgres

This is a single-user local/side-project tool. SQLite means zero setup for anyone
cloning the repo. If this ever needs concurrent multi-user writes, swap the
SQLAlchemy engine URL and add Alembic migrations; nothing else in the architecture
changes because all DB access goes through `backend/db.py` and `backend/models.py`.

## Why no ORM migrations tool in v1

`Base.metadata.create_all()` is enough while the schema is still moving fast and
there is no production data to preserve. Revisit (add Alembic) before the first
deploy anyone else depends on. Tracked in `docs/decisions.md`.
