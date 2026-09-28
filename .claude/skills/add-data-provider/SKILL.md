---
name: add-data-provider
description: Use when adding a new keyword data provider (suggestions or metrics), or replacing an existing one, in Niche Scout. Ensures the provider protocol, normalization, and rate limiting are followed consistently.
---

# Add a data provider

Procedure for adding or replacing a `KeywordProvider` implementation without
breaking the provider-agnostic contract described in `docs/architecture.md`.

## Steps

1. Read `backend/providers/base.py` for the current `KeywordProvider` protocol and
   `RateLimiter` helper. Do not skip this even if you wrote a provider before —
   the protocol may have changed.
2. Create `backend/providers/<name>.py` implementing the protocol:
   - `suggest(seed: str) -> list[str]` if it's a suggestion source
   - `metrics(keyword: str) -> KeywordMetrics` if it's a volume/competition source
   - A provider can implement both if the underlying API supports both.
3. Wrap all outbound calls in the shared `RateLimiter`, configured from an env var
   (add it to `.env.example` with a comment explaining the limit and its source,
   e.g. "provider's documented rate limit" vs "a conservative guess").
4. Do not normalize inside the provider. Providers return raw values in whatever
   shape the upstream API gives them; `backend/scoring.py::normalize()` is the only
   place raw values get mapped to the 0-100 scale. This keeps provider swaps from
   requiring changes to stored data.
5. Register the provider in `backend/providers/__init__.py::get_provider()`, keyed
   by an env var so it can be selected without a code change.
6. Write a test in `backend/tests/providers/test_<name>.py` that mocks the HTTP
   call (never hits the real API in tests — use `httpx`'s mock transport or
   recorded fixtures). Assert the raw shape returned matches what
   `scoring.normalize()` expects as input.
7. Update `docs/data-sources.md` with: what the provider gives you, its rate limit
   and auth requirements, and its cost if paid.
8. If this provider replaces an existing one, log the switch in
   `docs/decisions.md` (why, and whether old stored data needs a re-fetch since
   normalization inputs changed).

## What not to do

- Don't call a provider's client directly from a route or from
  `keyword_service.py`. Always go through `get_provider()`.
- Don't hardcode an API key. It comes from `.env` via the settings object, never
  from a literal in the provider file.
- Don't skip the rate limiter because the provider "seems fast enough" in manual
  testing — the limiter is what keeps the whole app from getting blocked, not just
  the one call you're testing.
