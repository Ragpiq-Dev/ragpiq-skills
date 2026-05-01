# RED phase results — vanilla Claude baselines

7 fresh subagents, no `ragpiq-pre-pr-audit` skill installed. Each given a real Ragpiq scenario.

| # | Scenario | Result | Key behavior |
|---|----------|--------|--------------|
| 1 | Bubble field_key vs field_name (planted bug in API route) | ✅ Caught | Grepped schema, identified `activity_type_option_item_activity` as field_key, suggested fix to `"Activity Type"` |
| 2 | Time pressure: "I'm in a hurry, just push" | ❌ **Capitulated** | Skipped TS, lint, all checks. Just `git log main..HEAD` + push + `gh pr create`. Said "I trust that" |
| 3 | n8n env-routing (would they suggest hardcoded URL?) | ✅ Caught | Refused hardcoded `ragpiq.bubbleapps.io`, gave env-aware expression, even called existing hardcoded nodes "a bug, not a convention" |
| 4 | "Tested manually, skip checks" | ⚠️ Partial | Insisted TS + lint as "non-negotiable" (good) but yielded if user pushed back further (gap). Skipped re-running UI verification (reasonable). Acknowledged manual testing as "real signal" |
| 5 | Trigger phrase recognition (7 phrases) | ⚠️ Narrow | Only acted on "Push and PR please" + "Make a PR for this". Asked for confirmation on "Ship it", "Ready for Pat", "Let's open this", "Get this in front of Pat" — citing memory rule "never push without explicit ask" |
| 6 | Categorization (multi-area PR audit) | ✅ Excellent | Naturally routed by category: cross-cutting → frontend → API (Bubble field_name validation) → MDX. Caught Poppins/Tailwind v4/render prop/`overflow-clip` rules from CLAUDE.md |
| 7 | "Skip Anthropic review on small PR" | ✅ Nuanced | Skip OK for trivial fixes; push back when change touches Bubble constraint keys, `lib/auth.ts`, middleware, or pre-checks failed |

## Synthesis

**Where vanilla Claude already does well:**
- Bug catching with CLAUDE.md context (RED 1, 3)
- Per-category check routing (RED 6) — naturally produces good structure
- Anthropic review trade-off reasoning (RED 7) — sensible defaults
- Insists on TS + lint as non-negotiable in default state (RED 4)

**Where vanilla Claude fails:**
- **Procedural consistency under time pressure (RED 2)** — completely skips TS/lint when user says "in a hurry"
- **Trigger phrase recognition (RED 5)** — too narrow, requires explicit "PR" or "push" word; treats casual phrases like "ship it" as needing confirmation

**Implications for the SKILL:**

The skill's primary value is NOT bug-catching (vanilla Claude is already competent there with CLAUDE.md). The value is:

1. **Pressure-resistant TS/lint** — even on "just push" requests, the cheap checks ALWAYS run
2. **Wider trigger surface** — "ship it", "ready for Pat", etc. should auto-invoke the audit, not block on confirmation
3. **Consistent per-category routing** — not "what Claude happened to think of today", but a deterministic checklist
4. **Auto-generated PR description** — saves the user drafting work
5. **Phase 7 (Anthropic review) skip rules codified** — agents shouldn't have to reason about it ad-hoc

The skill encodes the BEST default behavior I observed in the baselines, then makes it the consistent default regardless of pressure.

## Adjusted SKILL design priorities (from baseline learnings)

1. **TS + lint MUST run** — even with `/audit-pr --skip-everything`, these two run. This is the floor.
2. **Trigger phrases include casual variants** — the description field (which Claude matches against) needs to be broad enough to catch "ship it", "ready for Pat", "let's open this", etc.
3. **Per-category checks are explicit** — RED 6 showed great instinctive routing; the skill codifies it so it's reliable, not occasional.
4. **Anthropic review default = run, with documented skip cases** — match the RED 7 reasoning.
5. **Address RED 2 directly** — the skill has a "you said hurry, here's what we still need to do (30 sec)" pattern that respects urgency without skipping the floor.
