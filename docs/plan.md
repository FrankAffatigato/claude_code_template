# Plan: Niche Scout

## Goal

Given a seed keyword (e.g. "dog harness"), return a ranked list of related keywords
scored on an "opportunity" axis: decent search demand, low competition. Output as a
table plus a demand-vs-competition scatter plot, so a seller can eyeball which
keywords sit in the good quadrant (high demand, low competition).

This is a v1 for personal/side-project use, not a production SaaS. Optimize for
"works correctly and is easy for another session to pick back up," not for scale.

## Out of scope for v1

- User accounts / auth
- Saving searches server-side per user (local browser storage is fine)
- Anything beyond English-language, Amazon-style keyword data
- Automated competitor listing scraping (legal/ToS risk; revisit later if needed)

## Phases

### Phase 1: Backend skeleton and data model
- [ ] FastAPI app boots, health check route
- [ ] SQLAlchemy models: `Keyword`, `Niche` (a saved seed search), `Snapshot` (a
      point-in-time set of scored keywords for a niche)
- [ ] SQLite file created on startup, no migrations tool for v1 (plain
      `Base.metadata.create_all`)
- Done when: `make backend` runs, `GET /health` returns 200, DB file is created.

### Phase 2: Keyword provider layer
- [ ] `KeywordProvider` protocol: `suggest(seed: str) -> list[str]` and
      `metrics(keyword: str) -> KeywordMetrics` (volume, competition, both 0-100
      after normalization)
- [ ] Autocomplete provider: hits a public suggestion endpoint, free, rate-limited
- [ ] Metrics provider: paid API for volume/competition (see
      `docs/data-sources.md` for the chosen provider and why)
- [ ] Providers are swappable via `backend/providers/__init__.py::get_provider()`,
      chosen by env var, so a provider can be replaced without touching routes
- Done when: calling `keyword_service.expand_seed("dog harness")` returns a list of
  `KeywordMetrics` objects with real (not mocked) data.

### Phase 3: Scoring
- [ ] `normalize()`: maps raw provider output to 0-100 ints
- [ ] `opportunity_score()`: combines volume and competition into a single 0-100
      score. v1 formula: `opportunity = volume * (1 - competition/100)`, then
      re-normalized to 0-100 across the result set. Document the formula in
      `docs/decisions.md` if it changes.
- [ ] Unit tests for both functions with known inputs/outputs
- Done when: `pytest backend/tests/test_scoring.py` passes and covers edge cases
  (zero volume, max competition, empty result set).

### Phase 4: API routes
- [ ] `POST /niches` — body: `{seed: str}`. Runs the full pipeline (expand -> score
      -> store), returns the `Niche` id and its scored keywords.
- [ ] `GET /niches/{id}` — returns stored keywords for a past search
- [ ] `GET /keywords?niche_id=&sort=opportunity` — sortable/filterable keyword list
- Done when: all three routes have a passing pytest test using a test DB (not the
  dev DB).

### Phase 5: Frontend
- [ ] `SeedForm`: text input + submit, calls `POST /niches`
- [ ] `OpportunityTable`: sortable table of keyword, volume, competition,
      opportunity score
- [ ] `OpportunityChart`: Recharts scatter plot, x = competition, y = volume, dot
      size or color = opportunity score
- [ ] Loading and error states for the API call (provider rate limits mean this can
      take several seconds)
- Done when: a seed keyword typed in the browser produces a populated table and
  chart without a page reload.

### Phase 6: Polish
- [ ] Basic input validation (empty seed, seed too long)
- [ ] Simple caching: don't re-fetch a seed searched in the last 24h, serve the
      stored snapshot instead
- [ ] README screenshots
- Done when: repeating the same seed search within 24h does not call the paid
  metrics provider again (verify via provider call count in a test).

### Phase 7: Deploy
- [ ] Pick a host for the backend (a small always-on box or a container platform;
      SQLite needs a persistent disk, not ephemeral storage, so serverless platforms
      that wipe the filesystem between requests are out unless the DB is moved to a
      hosted Postgres first)
- [ ] Pick a host for the frontend (static hosting is enough, it's a Vite build)
- [ ] Move secrets (provider API keys) into the host's env var / secrets manager,
      never committed, never baked into the frontend bundle
- [ ] Add auth before making this reachable outside your own machine (see "Out of
      scope for v1" above, this is the point where that decision has to be revisited,
      not skipped)
- [ ] Basic logging: which seeds were searched, provider call counts, and errors,
      enough to know if the paid metrics provider is being called more than expected
- [ ] Smoke test: a fresh clone of the repo, deployed from scratch, produces a working
      seed search end to end
- Done when: the app is reachable at a real URL, a seed search works there, and no
  secret is visible in the deployed frontend bundle or a public repo.

## Explicitly deferred to v2

- Multi-marketplace support (Etsy, Walmart, not just Amazon-style data)
- Trend-over-time charts (would need recurring snapshots)
- Export to CSV

## How to use this plan in a session

Work one phase at a time. Before starting a phase, check `docs/state.md` to confirm
it's actually next and nothing upstream is blocking it. When a phase's checkboxes are
all done, check the "Done when" condition yourself (run the test/command), then check
the boxes and update `docs/state.md`. Don't check a box because the code was written;
check it because the done condition was verified.
