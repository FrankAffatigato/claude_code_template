# Data sources

## Keyword suggestions (free)

**Provider:** public autocomplete/suggestion endpoint (Amazon-style search
suggestions).
**Gives us:** a list of related search strings for a seed keyword. No volume or
competition numbers.
**Limits:** roughly 1 request/second before responses start getting throttled or
blocked. No auth required.
**Implementation:** `backend/providers/autocomplete.py`. Must use the shared
`RateLimiter` in `backend/providers/base.py`, not its own sleep() calls.

## Keyword metrics: volume + competition (paid)

**Provider:** placeholder — pick one when starting Phase 2. Candidates to evaluate:
- A keyword research API with an Amazon-specific dataset (search volume estimates,
  competing-product counts)
- A general SEO keyword API used as a rough proxy if an Amazon-specific one is too
  expensive for a side project

**Decision needed:** which provider, and whether its free tier is enough to build
and test against before paying for volume. Log the choice in `docs/decisions.md`
once made, including price and rate limit, so a future session doesn't have to
re-research this.

**Implementation:** `backend/providers/metrics_api.py`, behind the same
`KeywordProvider` protocol as the autocomplete provider.

## Normalization

Different providers report volume and competition on different scales (some 0-100,
some raw monthly search counts, some categorical). Raw provider output is never
stored. Everything is passed through `backend/scoring.py::normalize()` before it
touches the database, so switching providers later doesn't require a data migration
of stored scores, only a re-fetch.

## Adding a new or replacement provider

See `.claude/skills/add-data-provider/SKILL.md` for the step-by-step procedure.
