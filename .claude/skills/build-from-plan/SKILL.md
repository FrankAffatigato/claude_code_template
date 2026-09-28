---
name: build-from-plan
description: Use when asked to continue building Niche Scout, work the next phase, or pick up where a previous session left off. Reads state and plan, implements one phase, verifies it, updates state.
---

# Build from plan

Procedure for implementing the next unfinished phase of `docs/plan.md`, in a way
that leaves the repo in a state the next session (human or AI) can pick up cleanly.

## Steps

1. Read `docs/state.md`. This is the source of truth for what's actually done, not
   the checkboxes in `docs/plan.md` alone (a checkbox can be stale).
2. Read `docs/plan.md`, but only the phase that state.md says is next. Do not
   re-read finished phases unless something about the current phase depends on
   understanding a past decision — in that case check `docs/decisions.md` first,
   it's shorter.
3. If the phase has an open decision blocking it (state.md's "Blocked" section),
   stop and surface the decision instead of guessing. Do not silently pick a
   provider, library, or approach that docs/decisions.md marks as undecided.
4. Implement the phase's checkboxes in order. Follow the conventions in `CLAUDE.md`
   (provider protocol, route/service split, normalization rule, etc.) — do not
   introduce a new pattern without a reason.
5. After implementing, verify the phase's "Done when" condition yourself by actually
   running it (the test command, the curl, the browser action). Do not mark
   anything done based on the code looking right.
6. Update `docs/plan.md`: check off completed boxes.
7. Update `docs/state.md`:
   - Move finished work from "In progress" (or add fresh) to "Done"
   - Update "Next" to point at the next phase or the next unchecked box
   - Add anything newly blocked, with why
   - Update the "Last updated" line
8. If you made a decision not already in `docs/decisions.md` (chose a library,
   picked a formula, decided to skip something), log it there in one short entry.
9. Run `make lint` and `make test` (or the relevant subset) before finishing. Report
   failures rather than leaving them for the next session to discover.

## What not to do

- Don't implement ahead into a later phase because it seemed convenient. If Phase 4
  needs something from Phase 5, that's a sign the plan's phase order needs revising —
  raise it, don't silently reorder by implementing out of sequence.
- Don't rewrite `docs/plan.md`'s already-completed phases to match code you wrote
  differently than planned. Instead, note the deviation in `docs/decisions.md`.
- Don't leave `docs/state.md` saying something is "in progress" when you're actually
  done, or "done" when a test is failing.
