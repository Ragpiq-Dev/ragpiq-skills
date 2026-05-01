# PR Description Template

This is the template the audit auto-fills via `scripts/pr-template.py`. Same shape every PR so Pat learns to scan it fast.

---

## Template (markdown)

```markdown
## Summary

<1-3 bullets — auto-pulled from latest commit subject + spec doc top section if present>

### What's new
<LLM-summarised from the diff: the actual user-facing changes>

### Bug fixes uncovered
<auto-detected: any commits in this branch with `fix(...)` prefix → bullet list>

### Architecture
<file map auto-generated from `git diff origin/main --stat`, grouped by category>

### How it works (if non-trivial)
<2-4 sentences pulled from spec/plan if they exist on the branch — otherwise omitted>

## Test plan

<auto-populated checklist from the audit findings + standard items>

- [ ] TypeScript clean (✓ verified by audit)
- [ ] Lint clean (✓ verified by audit)
- [ ] Visual audit at 1920/768/375 (✓ verified by audit if frontend touched)
- [ ] No new console errors (✓ verified by audit)
- [ ] <change-type-specific items below>

### Frontend changes (only shown if frontend touched)
- [ ] Sign in as reseller, walk through happy path
- [ ] Test on mobile viewport
- [ ] Verify no layout shift on slow network

### API changes (only shown if API touched)
- [ ] Test with valid auth
- [ ] Test with invalid auth
- [ ] Verify Bubble field_names against `reference/bubble.schema.json`
- [ ] Confirm error responses are graceful

### n8n changes (only shown if n8n touched)
- [ ] Workflow updated AND deployed live (n8n auto-saves but verify active)
- [ ] Test execution on test env
- [ ] Confirm bubble_env routing correct

### Brand-voice changes (only shown if MDX/marketing touched)
- [ ] Reads in Ragpiq voice (per ../ragpiq-ops/marketing/brand/voice/_core.md)

## Notes for review

<auto-pulled if these exist on the branch:>
- Spec: `docs/superpowers/specs/<file>`
- Plan: `docs/superpowers/plans/<file>`
- Related PRs: <auto-detected from commit messages mentioning #N>

### Pre-PR audit

- ✓ TypeScript clean
- ✓ <N> frontend files, <M> API routes, <K> n8n changes
- ✓ Visual audit at 3 viewports — no new console errors
- ✓ Anthropic code review: <inline link to bot comment, or "skipped — small fix">

🤖 Generated with [Claude Code](https://claude.com/claude-code) via /audit-pr
```

---

## Auto-population rules

| Section | Source | User edits before PR? |
|---------|--------|-------------------------|
| Title | Latest commit subject (max 70 chars; prefer `feat(...)` over `fix(...)`) | Edit if needed before push |
| Summary | First few commits + `## Summary` section of spec doc if found | Sometimes — for nuance |
| What's new | LLM-summarized diff (1 Haiku call, ~$0.005) | Rarely |
| Bug fixes uncovered | Commits with `fix(*)` prefix → first line | Never |
| Architecture | `git diff --stat origin/main` grouped by directory + category | Never |
| Test plan | Static template + change-type detection | Sometimes — context-specific items |
| Notes for review | Spec/plan/related PR detection | Rarely |
| Pre-PR audit | Audit phase output (just the summary lines) | Never |

---

## Title generation rule

```python
# Pseudocode
commits = get_branch_commits()  # newest first
feat_commits = [c for c in commits if c.subject.startswith("feat(")]
fix_commits = [c for c in commits if c.subject.startswith("fix(")]

# Prefer the headline feat
if feat_commits:
    title = feat_commits[0].subject
elif fix_commits:
    title = fix_commits[0].subject
else:
    title = commits[0].subject  # latest

title = title[:70]  # truncate per CLAUDE.md
```

---

## Template variants by category

### Frontend-only PR

Show only:
- Summary, What's new, Architecture, How it works, Test plan (frontend), Notes, Pre-PR audit

Hide: API checklist, n8n checklist, brand-voice checklist (unless marketing files touched).

### Backend-only PR (API routes, lib/, no frontend)

Show only:
- Summary, What's new, Architecture, Test plan (API), Notes, Pre-PR audit

Hide: frontend checklist, visual audit lines.

### Pure docs/spec PR

Minimal template:
- Summary, file list, Pre-PR audit (just TS clean confirmation)

---

## Examples

### Example 1: This PR (skill creation)

Title: `feat(skill): add ragpiq-pre-pr-audit skill`

Body would auto-generate from the commit history + spec doc top section.

### Example 2: PR #42 (AI Lister Processing Queue)

Title: `feat(business): AI Lister processing queue + recent consignors` ✓ matches what we shipped

Body: same shape as the actual PR #42 description (which was hand-written). Auto-generation matches that pattern.
