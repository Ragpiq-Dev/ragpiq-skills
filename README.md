# ragpiq-skills

Ragpiq engineering skills for AI coding agents (Claude Code, Cursor, etc.).

Currently ships one skill: **`ragpiq-pre-pr-audit`** — a 9-phase pre-PR audit
that catches Ragpiq-specific bugs before Pat reviews.

## Install

In Claude Code:

```
/plugin marketplace add Ragpiq-Dev/ragpiq-skills
/plugin install ragpiq-pre-pr-audit@ragpiq-skills
```

After install, restart Claude Code so the skill is registered.

## Usage

In any Ragpiq frontend repo, when you're ready to open a PR:

- Type `/audit-pr` (explicit)
- OR just say "create PR", "ship it", "ready for Pat", etc. (auto-trigger)

The skill will run a 9-phase audit, push your branch as a draft PR,
dispatch Anthropic's `/code-review:code-review` on it, then ask you for
explicit confirmation before converting to ready-for-review.

## What it catches

Designed from real bugs encountered in PR #42 (AI Lister processing queue):

- **Bubble field_key vs field_name** — sending `activity_type_option_item_activity` instead of `Activity Type` (silent 500)
- **n8n LIVE Bubble URL hardcoded** in sub-workflows (silent dev-env failures)
- **Missing aria-label / focus-visible** on hover-revealed buttons
- **Memory leaks** from un-revoked blob URLs
- **Off-tone copy** in marketing-facing MDX
- **Stale Bubble schema** that misses new fields

Plus standard pre-PR hygiene:

- TypeScript clean
- Lint clean
- Visual audit at 1920 / 768 / 375 viewports
- Console + network error scan
- Auto-generated PR description with category-aware test plan

## Required tools (auto-detected at run-time)

| Tool | Status | Used in |
|------|--------|---------|
| `gh` CLI | Required | Phase 6 (open PR) |
| `git` | Required | Phase 1, 6 |
| `npx` | Required | Phase 2 (TypeScript) |
| `Claude Preview MCP` | Optional | Phase 4 (visual audit) — skipped if missing |
| `code-review@claude-plugins-official` | Optional | Phase 7 — skipped if missing |
| `vercel-agent-skills` | Optional | `--deep` mode — skipped if missing |

If a required tool is missing, the skill prints a one-time setup hint and
exits cleanly. Optional tools just skip the relevant phase.

## Structure

```
ragpiq-skills/
├── .claude-plugin/
│   ├── marketplace.json   # Claude Code marketplace metadata
│   └── plugin.json        # Plugin manifest
├── README.md
├── skills/
│   └── ragpiq-pre-pr-audit/
│       ├── SKILL.md       # Entry point (< 500 words; CSO-optimized)
│       ├── workflow.md    # Full 9-phase reference
│       ├── pr-template.md # PR description template + auto-population
│       ├── checks/        # Per-check references
│       └── scripts/       # Executable helpers
├── commands/
│   └── audit-pr.md        # /audit-pr slash command
└── tests/                 # Pressure scenarios + RED/GREEN test results
```

## Updating

```bash
cd ~/.claude/plugins/cache/ragpiq-skills/main
git pull
```

Or use Claude Code's built-in `/plugin update ragpiq-pre-pr-audit`.

## Contributing

Open a PR to this repo. Use the skill itself to audit (yes, it eats its own
dog food).

## License

MIT
