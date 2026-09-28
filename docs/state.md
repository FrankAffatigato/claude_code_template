# State

Last updated: 2026-09-28 (repo scaffold created, no application code written yet)

Read this file first in any new session. It should always reflect reality, not
intent — if something is half-done, say so in In progress, don't mark it Done.

## Done

- Repo scaffold: `CLAUDE.md`, `README.md`, `docs/plan.md`, `docs/architecture.md`,
  `docs/data-sources.md`, `docs/decisions.md`, this file
- `.claude/` config: two skills (`build-from-plan`, `add-data-provider`), two
  commands (`/resume`, `/checkpoint`), one subagent (`code-reviewer`),
  `settings.json`
- `requirements.txt`, `Makefile`, `.env.example`, `.gitignore`

## In progress

- Nothing yet. Phase 1 (backend skeleton) has not been started.

## Blocked

- Phase 2 needs a decision on which paid keyword-metrics provider to use (see open
  question in `docs/data-sources.md`). Not blocking Phase 1.

## Next

1. Start Phase 1 in `docs/plan.md`: FastAPI skeleton, SQLAlchemy models, health
   check route.
2. Use the `build-from-plan` skill to work through it phase by phase.
3. Before Phase 2, resolve the metrics-provider decision and log it in
   `docs/decisions.md`.

## Notes for whoever picks this up

- No code has been run yet. `make backend` will fail until Phase 1 exists.
- The plan's phases are meant to be done in order; Phase 3 (scoring) depends on
  Phase 2 (providers) returning real data, not mocks, so scoring can be tuned
  against real numbers.
