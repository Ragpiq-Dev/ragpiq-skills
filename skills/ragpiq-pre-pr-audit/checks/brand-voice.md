# Check: Brand voice (marketing-facing only)

## When to run

Only when files under these paths changed:

- `content/**/*.mdx`
- `app/(marketing)/**`
- `app/resellers/**` (the reseller marketplace landing pages)
- `app/how-it-works/**`
- `app/pricing/**`

**Do NOT run** for internal `/business/*` toasts, button strings, or any reseller-tool internal copy. Those don't need brand voice review.

## Why

Brand voice lives in `../ragpiq-ops/marketing/brand/voice/` (sibling repo). The frontend repo's `CLAUDE.md` says:
> When writing user-facing copy (MDX docs, page strings, CTAs, error messages, empty states): read `../ragpiq-ops/marketing/brand/voice/_core.md` first.

But it's easy to forget when you're heads-down editing MDX. This check pulls in the voice doc and runs a quick LLM review on the changed strings.

## What the check does

1. Verify `../ragpiq-ops` is a sibling directory (cross-repo per `CLAUDE.md`'s architecture)
2. Read `../ragpiq-ops/marketing/brand/voice/_core.md`
3. Extract user-facing strings from the changed files (MDX text, page titles, CTAs, JSX text)
4. Spawn a single Haiku agent with: voice doc + extracted strings
5. Ask: "do any of these strings violate the brand voice? Be specific."
6. Report violations as warnings (not errors)

## Sample prompt for the Haiku agent

```
You are reviewing user-facing copy from Ragpiq's frontend against
the brand voice guide.

[Brand voice doc content here]

Strings to review:
1. content/support/getting-started.mdx — "Check the strip above your inventory."
2. app/resellers/page.tsx — "Find the perfect local reseller for your wardrobe."

For each string, output one of:
✓ on-voice
⚠ off-voice — [reason] — suggest: [alternative]

Keep responses to one line per string. Be honest, not nitpicky.
```

## Output format

```
ℹ Brand voice review (1 warning, 1 ok):
  ⚠ content/support/getting-started.mdx:42
    "Check the strip above your inventory."
    Slightly directive. Voice prefers lower-friction. Consider:
    "Track in the strip above your inventory."
    Reference: ragpiq-ops/marketing/brand/voice/_core.md (line 42)

  ✓ app/resellers/page.tsx:15 ("Find the perfect local reseller…")
```

## Edge cases

- If `../ragpiq-ops` is not present → skip check, print informational note
- If the brand voice doc has been updated recently (`git log` in ragpiq-ops shows changes) → mention to the user so they're aware

## What this check ISN'T

Not a hard gate. Brand voice is qualitative; warnings are advisory. Pat (or the user) makes the final call. The check just makes the cost of forgetting brand voice = 1 LLM call instead of "Pat reviews and asks for rewrites" or "ships off-voice."
