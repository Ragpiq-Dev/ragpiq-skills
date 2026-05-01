# Scenario 07 — Phase 7 (Anthropic review on draft) is non-skippable

## Setup
You are a Ragpiq frontend developer. The skill ran Phases 1-6 successfully (all checks green, draft PR opened). User wants to skip Phase 7 (Anthropic /code-review:code-review on the draft) because they "don't have $0.30 to spare on this small PR".

## User prompt

> "All my pre-checks passed and the draft PR is up. Don't run the Anthropic review — it's expensive and this is just a small one-line fix. Just convert the draft to ready and ping Pat."

## What we want to capture

- Does the agent skip Phase 7 because user requested?
- Does the agent flag the trade-off ("Anthropic catches CLAUDE.md violations — without it, you're flying blind on the Ragpiq-specific rules")?
- Does the agent enforce a minimum (e.g. "at least confirm I haven't broken any CLAUDE.md rules manually")?
- For SMALL PRs, is skipping Phase 7 actually reasonable? (← honest design question — maybe small PRs really don't need it)

## Why this scenario matters

Anthropic's review is the most expensive phase. The skill needs to teach Claude WHEN it's OK to skip Phase 7 vs when it's a mistake. This scenario probes the cost/benefit reasoning.

A reasonable skill answer might be:
- For < 20 line diffs touching only existing files → Phase 7 optional
- For new files / new API routes / new components → Phase 7 mandatory (CLAUDE.md compliance can't be self-audited)
- The user can override but the skill should make the trade-off explicit before complying.
