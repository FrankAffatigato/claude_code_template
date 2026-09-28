# Decisions log

Short entries only: what was decided, why, and what it rules out. This is not a diary
of the work, it's a record of choices so they don't get silently re-litigated or
re-asked in a later session. Add a new entry per decision; do not edit old entries
except to add a "superseded by" note.

---

## 2026-09-28: SQLite instead of Postgres for v1

Single-user side project, no concurrent-write requirement. SQLite means anyone
cloning the repo needs zero infra setup. Rules out: multi-user concurrent writes
without a later migration. Revisit if this becomes a shared/deployed tool.

---

## 2026-09-28: Opportunity score formula for v1

`opportunity = volume * (1 - competition/100)`, then re-normalized to 0-100 across
the current result set (not a fixed global scale, since "high volume" is relative to
the seed's niche). This is a simple starting formula, not a validated one. Rules out:
comparing opportunity scores across two different seed searches as if they were on
the same scale — they aren't, by design, in v1. If cross-search comparison becomes a
requirement, this needs a fixed reference scale instead.

---

## 2026-09-28: No auth / no user accounts in v1

This is a personal tool. Rules out: deploying it anywhere publicly reachable without
adding auth first. If that becomes a goal, add auth as its own phase before deploy,
not as an afterthought.

---

## Template for new entries

```
## YYYY-MM-DD: <short title>

What was decided. Why. What it rules out or what would need to change to revisit it.
```
