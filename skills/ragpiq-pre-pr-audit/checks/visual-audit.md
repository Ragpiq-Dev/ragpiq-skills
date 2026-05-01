# Check: Visual audit (Phase 4)

## When to run

Phase 4 runs whenever any `*.tsx`, `*.css`, or `*.mdx` file changed AND `--skip-visual` is not set.

Skipped automatically for backend-only PRs (only `app/api/**/*.ts`, `lib/api/**/*.ts`, etc. changed).

## Pre-requisites

The skill needs Claude Preview MCP available. Verify with `mcp__Claude_Preview__preview_list`. If not available, print:

```
⚠ Claude Preview MCP not detected. Skipping visual audit.
  Phase 4 requires the preview MCP. Install via Settings → MCP.
  Other phases (1-3, 5-9) will continue.
```

Otherwise proceed.

## What the check does

### Step 1: Pick the target route

```bash
# The most-changed *.tsx file by line count is the visual-target candidate
TARGET_ROUTE=$(git diff origin/main --numstat -- '*.tsx' \
  | awk '{print $1+$2"\t"$3}' \
  | sort -rn \
  | head -1 \
  | awk '{print $2}')
```

Convert that file path to a URL path (heuristic):

| File path | Route |
|-----------|-------|
| `components/business/inventory/X.tsx` | `/business/inventory` |
| `app/business/inventory/page.tsx` | `/business/inventory` |
| `app/(marketing)/about/page.tsx` | `/about` |
| `components/SiteHeader.tsx` | (check multiple routes — print options) |

Print to user:

```
Target route for visual audit: /business/inventory
(based on most line changes in components/business/inventory/InventoryView.tsx)
Override with --route /your/path or say "test /business/X instead"
```

### Step 2: Establish console baseline

Before doing anything visual, capture current console state:

```javascript
// preview_console_logs to count current errors
```

This is the baseline. Anything new during the audit is "new."

### Step 3: Test viewports

```javascript
preview_resize({ width: 1920, height: 1080 });
preview_eval({ expression: `window.location.assign("http://localhost:3001${TARGET_ROUTE}"); 'navigating'` });
// wait 4s
preview_screenshot();
preview_console_logs({ level: 'error' });

preview_resize({ width: 768, height: 1024 });
// no need to navigate again — page resized
preview_screenshot();

preview_resize({ width: 375, height: 812 });
preview_screenshot();
```

### Step 4: Network scan

```javascript
preview_network({ filter: 'failed' });
```

Any 4xx/5xx that wasn't in the baseline → flag.

### Step 5: Hand back the findings

Output:

```
Visual audit:
  ✓ 1920×1080 — no new console errors
  ✓ 768×1024 — no new console errors
  ✓ 375×812 — no new console errors
  ✓ Network: 0 failed requests during audit
```

Or:

```
⚠ Visual audit found:
  - 1920×1080: 1 new console.error in <ProcessingCard> ("Cannot read property 'images' of undefined")
  - Network: GET /api/business/something/drafts → 500 (1 occurrence)
```

## Auth / state pre-conditions

If the target route requires auth (e.g. `/business/*`) and the preview isn't authed → tell user, don't crash:

```
⚠ Visual audit can't reach /business/inventory — preview is not authenticated.
  Sign in at http://localhost:3001/login then re-run /audit-pr.
  (Or skip with --skip-visual.)
```

## --deep mode

If `--deep` flag is set AND `vercel-agent-skills:web-design-guidelines` is installed:

1. After the basic visual audit, invoke `web-design-guidelines` against changed files
2. Append its findings to the audit report

This adds 60-90 sec but catches a11y issues, focus state issues, performance hints, and more. Worth it for big landing-page PRs.

## What this check ISN'T

Not a full UX walk-through (no clicking, no flow testing). Just multi-viewport + console + network. Heavier interactive testing is intentionally manual — humans are still the final UX judge.
