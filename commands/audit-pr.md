---
description: Run the Ragpiq pre-PR audit before opening a PR
allowed-tools: Bash(git*), Bash(gh*), Bash(npm*), Bash(npx*)
---

Run the Ragpiq pre-PR audit on the current branch.

This invokes the `ragpiq-pre-pr-audit` skill which orchestrates a 9-phase
audit: preflight, TypeScript + lint floor, Ragpiq-specific checks (Bubble
field_name, n8n env-routing, brand voice), live-preview multi-viewport
visual audit, push as draft PR, dispatch Anthropic /code-review:code-review
on the draft, then explicit user OK before convert-to-ready.

## Arguments

`$ARGUMENTS` — optional flags:

- `--skip-visual` — skip Phase 4 (visual audit)
- `--skip-anthropic` — skip Phase 7 (Anthropic /code-review)
- `--draft-only` — never auto-convert to ready
- `--no-push` — local checks only (dry run)
- `--deep` — invoke vercel-agent-skills:web-design-guidelines if installed
- `--route /path` — override target route for visual audit

## Behavior

Follow the workflow in `skills/ragpiq-pre-pr-audit/SKILL.md` and
`workflow.md`. The Phase 2 floor (TypeScript + lint) is non-skippable
by any flag — it is the floor by design.

After running, surface findings to the user and wait for explicit
confirmation before each shared-state action (push, open PR, convert
draft to ready).

🤖 Ragpiq pre-PR audit
