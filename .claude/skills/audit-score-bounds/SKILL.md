---
name: audit-score-bounds
description: Use after touching scoring.py, a provider, or the DB schema, or before /checkpoint if scoring code changed this session. Runs a script against the local SQLite DB to verify every stored score column is a 0-100 integer per CLAUDE.md's conventions.
---

# Audit score bounds

Runs `scripts/audit_scores.py` against the local dev DB to check every stored score
column obeys the invariants in CLAUDE.md's Conventions and Gotchas sections: scores
are 0-100 integers, and nothing bypassed `scoring.normalize()`. This is a
deterministic check — run the script rather than reading rows by hand or reasoning
about it from the code alone.

## Steps

1. Run `python .claude/skills/audit-score-bounds/scripts/audit_scores.py` (reads
   `DATABASE_URL` from the environment if set, else falls back to
   `./niche_scout.db`).
2. If it reports no database file found, the backend hasn't been run yet — nothing
   to audit, stop here.
3. If it reports violations, they name the table, row id, column, and the
   out-of-range or non-integer value. Fix the code path that produced it (usually a
   write that skipped `normalize()`), not the row itself.
4. Re-run the script after the fix to confirm zero violations before considering the
   task done.

## What not to do

- Don't hand-fix a bad row with a SQL UPDATE. That hides the bug that produced it —
  fix the write path in `scoring.py`, the provider, or the service layer, then
  re-run the search that produced the bad row.
- Don't skip this because `pytest` passed. The unit tests cover `normalize()` and
  `opportunity_score()` in isolation; this script catches the case where a route or
  service wrote to the DB directly and skipped normalization entirely.
