# Pre-PR Audit Workflow — Full 9-Phase Detail

This is the long-form reference. SKILL.md links here when an agent needs the full procedure.

---

## Phase 1 — Preflight (5–10 sec)

```bash
# Sanity: clean tree
git status --porcelain
# Halt if there are uncommitted changes; tell user to commit or stash

# Sanity: not on main
[ "$(git branch --show-current)" = "main" ] && echo "ERROR: on main" && exit 1

# Identify base branch
BASE=$(git merge-base HEAD main >/dev/null 2>&1 && echo "main" || echo "master")

# Enumerate changed files
CHANGED=$(git diff origin/$BASE --name-only)
```

Categorize each changed file:

| Pattern | Category |
|---------|----------|
| `app/**/*.tsx`, `components/**/*.tsx` | Frontend React |
| `app/api/**/route.ts` | API route |
| `lib/**` | Lib (check imports — could be either) |
| n8n workflow JSON paths | n8n workflow |
| `content/**/*.mdx`, `app/(marketing)/**`, `app/resellers/**` | Marketing/MDX |
| `docs/superpowers/specs/**`, `docs/superpowers/plans/**` | Spec/plan |
| `CLAUDE.md` | Dev infra |

Print summary to user:

```
PR will include:
  • 3 frontend files (components/business/inventory/*)
  • 1 API route (app/api/business/test-route/route.ts) — touches Bubble
  • 0 n8n changes
  • 1 MDX file (content/support/getting-started.mdx) — marketing
```

---

## Phase 2 — Cross-cutting checks (10–30 sec) — THE FLOOR

These ALWAYS run. No flag bypasses them.

```bash
npx tsc --noEmit                  # halt if errors
[ -f package.json ] && grep -q '"lint"' package.json && npm run lint  # halt if lint fails
git log --oneline origin/$BASE..HEAD   # show commit story to user
```

If TS or lint fails → halt entire audit. Show errors. User fixes, re-runs `/audit-pr`.

**Pressure resistance:** if user said "I'm in a hurry" — TS + lint still run. They take 30 sec. Tell user explicitly: "Floor checks are non-negotiable; running TS + lint (30 sec). Heavier audit phases skipped per your request."

---

## Phase 3 — Ragpiq-specific local checks (10–20 sec)

Per category, fire the relevant grep / script (see `checks/` directory). Skip irrelevant categories.

| Category present? | Run check |
|-------------------|-----------|
| API route OR lib/api/** with bubbleGet/Post/Patch | `scripts/grep-bubble-calls.sh` |
| Any file mentions `ragpiq.bubbleapps.io` (excluding CDN URLs) | `scripts/scan-n8n-env-routing.sh` |
| Any MDX or marketing file changed | `checks/brand-voice.md` (LLM call) |
| Any Bubble route AND schema > 30 days | print staleness reminder |
| Root `CLAUDE.md` changed | print drift reminder |

Output: structured findings list (✓ / ⚠️ / ℹ).

---

## Phase 4 — Visual audit (~1 min — only if frontend changed)

Skip if no `*.tsx` files changed, OR if `--skip-visual` flag given.

Use Claude Preview MCP:

1. Determine target route(s):
   - Multi-route diff → pick route with most line changes
   - Print chosen route up front so user can override mid-flight ("test /business/inventory instead")
2. Resize + screenshot:
   - 1920×1080 (desktop)
   - 768×1024 (tablet)
   - 375×812 (mobile)
3. Console scan: `preview_console_logs --level error`. Compare against pre-audit baseline.
4. Network scan: `preview_network --filter failed`.

Findings: any new console error or 4xx/5xx network → flag.

---

## Phase 5 — User checkpoint (interactive)

Print a structured summary:

```
Pre-PR audit complete.
  ✓ TypeScript clean
  ✓ Lint clean
  ✓ 3 frontend files, 1 API route — Bubble field_names verified against schema
  ✓ Visual audit at 3 viewports — no new console errors
  ⚠ MDX touches marketing voice — recommend reading `content/support/getting-started.mdx:42`

Ready to push and open draft PR?
  y     — push and open draft (Phases 6-8)
  fix   — exit so I can fix issues, re-run /audit-pr later
  cancel — abort, no push
```

Wait for explicit user response.

---

## Phase 6 — Push & open DRAFT PR (15 sec)

```bash
# Push if needed
git push -u origin "$(git branch --show-current)"

# Auto-generate title and body via scripts/pr-template.py
TITLE=$(scripts/pr-template.py --title)
BODY=$(scripts/pr-template.py --body)

# Open as DRAFT — explicit
gh pr create --draft --title "$TITLE" --body "$BODY"
PR_URL=$(gh pr view --json url -q .url)
```

Show PR URL to user.

---

## Phase 7 — Anthropic /code-review:code-review (~60–90 sec, cost ~$0.30)

**Skip rules** (only skip if ALL true):
- Diff < 20 lines AND
- No new files AND
- No `lib/auth.ts` / middleware / API routes / token-handling files touched AND
- Phases 1–4 passed cleanly AND
- User did NOT change `CLAUDE.md` in this PR

Otherwise (i.e., default): run.

```bash
# Invoke the official Anthropic skill on the draft PR
# (this skill posts a comment to the PR with confidence-scored findings ≥80)
claude /code-review:code-review "$PR_URL"
```

Poll `gh pr view --json comments` until the review comment lands (timeout ~120 sec). Read it back into chat.

---

## Phase 8 — Final decision (always explicit)

**Always ask the user, even on a clean review:**

```
Anthropic code review found [N] issues:
  - [Critical] field_key vs field_name in app/api/.../route.ts:52
  - [Important] Missing aria-label on collapse button

Choose:
  1. Convert to ready-for-review (Pat will be notified)
  2. Stay as draft (you'll fix issues, then convert manually)
  3. Close + start over
```

Wait for explicit y/n from user. Per Patrick's memory rule: "Shared-state actions need per-action confirmation."

If chosen "1": `gh pr ready "$PR_URL"`.
If chosen "2": no action; user fixes, may re-run `/audit-pr` to re-verify.
If chosen "3": `gh pr close "$PR_URL"`.

---

## Phase 9 — Tell Pat (optional)

If user picked option 1, optionally:

```bash
gh pr comment "$PR_URL" --body "@pat-the-reviewer ready for review."
```

Only do this if user requests OR if Patrick's preferences say to. Default: do not auto-tag.

---

## Skip flag matrix

| Flag | Skip Phase 1 | Skip Phase 2 (FLOOR) | Skip Phase 3 | Skip Phase 4 | Skip Phase 5 (checkpoint) | Skip Phase 6 (push) | Skip Phase 7 | Skip Phase 8 (checkpoint) |
|------|--------------|----------------------|--------------|---------------|---------------------------|---------------------|--------------|---------------------------|
| `/audit-pr` (default) | No | No | No | No | No | No | No | No |
| `--skip-visual` | No | No | No | YES | No | No | No | No |
| `--skip-anthropic` | No | No | No | No | No | No | YES | No |
| `--draft-only` | No | No | No | No | No | No | No | Phase 8 only allows draft / close, not ready |
| `--no-push` | No | No | No | No | Phase 5 prints findings + STOPS | YES | YES | YES |
| `--deep` | No | No | No | No (extends Phase 4 with web-design-guidelines) | No | No | No | No |

**Important:** Phase 2 (floor) cannot be skipped by any flag. There is no `--skip-floor` flag by design.

---

## Pressure-resistance script (paste this when user pushes back)

If user says "skip everything, just push" — respond:

```
I'll respect that for Phases 4-7 (visual + Anthropic review).

Phase 2 (TypeScript + lint) is the floor — it always runs, even on
"just push" requests. It's 30 seconds and catches the kind of silent
breakage that wastes 10x more of Pat's time later.

Running TS + lint now, then pushing as DRAFT, then asking you for the
final ready-for-review confirmation.
```

If user says "no I really mean it, skip TS too" — respond once:

```
TS errors will fail the Vercel build and block Pat from merging anyway.
Are you sure you want to skip? (yes / let-it-run)
```

If they say yes → skip + warn loudly. Otherwise run TS.
