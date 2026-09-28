# Resources: learning to build with an AI coding agent

Short list, kept current-ish. The two Anthropic docs links get updated in place, so
they're the ones worth bookmarking; blog posts age out faster.

## Anthropic's own material (most directly relevant)

- Claude Code docs: https://docs.claude.com/en/docs/claude-code/overview
  The official docs for the tool itself: CLAUDE.md conventions, skills, subagents,
  settings.json, hooks, slash commands.
- Claude Code best practices: https://www.anthropic.com/engineering/claude-code-best-practices
  Anthropic's own engineering write-up on this exact workflow: plan-then-build,
  CLAUDE.md, subagents, why to keep a written plan and state file across sessions.
- Subagents: https://docs.claude.com/en/docs/claude-code/sub-agents
  How to define a subagent with its own prompt and narrower tool access (used for
  this repo's `.claude/agents/code-reviewer.md`).
- Prompt engineering overview: https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview
  Not Claude Code specific, but the same clarity principles apply to writing a good
  SKILL.md or CLAUDE.md: be explicit, give examples, state the done condition.

## General agentic-coding practice

- Simon Willison's blog: https://simonwillison.net/
  Writes constantly and specifically about day-to-day work with coding agents.
  Grounded, practitioner-level, not hype.
- Search "spec-driven development" or "plan mode" plus "Claude Code" or "AI coding
  agent" for more practitioner write-ups on the plan.md -> build -> state.md loop
  this repo uses. Quality varies; treat the two Anthropic links above as the anchor.

## How this maps to the files in this repo

| Concept | File here |
|---|---|
| Standing instructions, loaded every session | `CLAUDE.md` |
| The build plan, phase by phase | `docs/plan.md` |
| How the pieces fit together and why | `docs/architecture.md` |
| Decisions made and what they rule out | `docs/decisions.md` |
| What's done / next, read first each session | `docs/state.md` |
| A reusable step-by-step procedure | `.claude/skills/*/SKILL.md` |
| A saved prompt triggered by name | `.claude/commands/*.md` |
| A narrower-scoped helper (e.g. a reviewer) | `.claude/agents/*.md` |
