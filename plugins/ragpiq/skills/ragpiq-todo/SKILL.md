---
name: ragpiq-todo
description: Turn work that just shipped into a short list of what Pat has to do next. Reviews the current session and the most recent commits or PRs, then emits action items only, a few words each, under Setup / Test / Won't work / Your call. Use when asked "what do I need to do", "how do I test this", "give me the steps", "what's left", "turn that into a to-do", or after finishing a chunk of work when the next move is somebody clicking or configuring something. Also use when a previous answer explained too much and needs boiling down to steps.
---

# Ragpiq To Do

Somebody has to go and do this. Tell them what, in as few words as possible, in the order they will do it.

You have just built something. You know why. **They do not need the why here.** The why goes in your prose above the list; the list is only the hand movements.

## The shape

Four headings, this order, skip any that would be empty:

```
**Setup**
1. …
2. …

**Test**
1. …
2. …

**Won't work on staging**
- …

**Your call**
- …
```

- **Setup** — config outside the codebase. Provider dashboards, env vars, accounts, keys, DNS. Things done once.
- **Test** — the click-through, in reachable order. Sign in before the page that needs it.
- **Won't work** — what they will otherwise waste an hour discovering. Say where it does work.
- **Your call** — decisions owed to them, not tasks. Each carries its PR links.

## Every line

- One action, one line. Aim for 10 words. Never past 15.
- Start with the verb or the exact place: "Visit", "Sign in as", "Square menu →".
- Use `→` to chain a path through UI or menus. It beats a sentence.
- Backtick anything they type, paste or click: URLs, env var names, routes, button labels, option names.
- Exact values only. `SQUARE_WEBHOOK_SIGNATURE_KEY`, not "the signing key". `/business/checkout`, not "the checkout page".
- Numbers where a threshold bites: "add item under $25", not "add a cheap item".
- Markdown links for PRs and issues, never a bare `#553`.
- No reasons, no reassurance, no "this will let you…". One parenthetical is allowed when the value would otherwise look wrong: "(current value is a placeholder)".
- AU English. No em dashes.

## Before you write it

The list is worthless if a step is impossible or already done. So:

- **Read what actually shipped.** The session's own work, plus `git log` or the merged PRs. Never list a step for something you did not build.
- **Check each Setup item is still needed.** Read the env, query the dev database, curl the route. Drop what is already in place; a list of nine items where six are done gets abandoned.
- **Name the blocker you found.** If a value is wrong or a prerequisite is missing, that is the most valuable line in the list.
- **Verify the walkthrough is reachable.** If the test needs a shop with connected Square and no such shop exists, that is a Setup line, not a silent assumption.
- **Say which environment.** Staging and production behave differently. Put it in the heading if it matters.

## Never

- Never explain what you built. That is the prose above the list.
- Never a step that only describes state ("the card now shows Live"). A step is something they do.
- Never a vague step ("configure the webhook"). Name the URL and the events.
- Never pad to look thorough. Six real steps beat twelve.
- Never list a task under **Your call**. That heading is decisions only.
- Never invent a step you have not verified is possible.

## Worked example

```
**Setup**
1. Square sandbox dashboard → add redirect `https://staging.ragpiq.com/api/marketplaces/square/callback`
2. Same app → add webhook `https://staging.ragpiq.com/api/webhooks/square`, tick `order.created`, `order.updated`, `payment.created`, `terminal.checkout.updated`
3. Copy that webhook's signature key → Vercel → Preview → `SQUARE_WEBHOOK_SIGNATURE_KEY` (current value is a placeholder)

**Test**
1. Visit `staging.ragpiq.com/?key=<STAGING_ACCESS_KEY>` once
2. Sign in as Ragpiq Thornbury
3. `/business/integrations` → Square → Connect
4. Square menu → Pair Terminal → "Tap succeeds" → Use this reader
5. `/business/checkout` → add item under $25 → Continue → Card machine → send
6. Check: one sale row, right split, item delisted
7. Repeat pairing with "Customer cancels", "Reader times out", "Reader stays waiting" (test Cancel)

**Won't work on staging**
- Real reader hardware (prod only)
- Square amounts over $25
- Shopify sale recording (webhooks go to prod)

**Your call**
- Promote `dev` → `main`? [#548](https://github.com/Ragpiq-Dev/ragpiq-frontend/pull/548) and [#551](https://github.com/Ragpiq-Dev/ragpiq-frontend/pull/551) are staging-only.
```

## Before you ship it

- [ ] Every line is an action, not a description
- [ ] Every URL, env var, route and button label is exact and backticked
- [ ] Setup items verified as still missing; done ones dropped
- [ ] Test steps run in reachable order
- [ ] Blockers named under Won't work, with where it does work
- [ ] Your call holds decisions only, each with PR links
- [ ] No line explains why
- [ ] AU English, no em dashes
