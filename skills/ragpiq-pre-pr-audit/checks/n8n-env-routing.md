# Check: n8n env-routing scan

## When to run

- Any changed file under a path containing n8n workflow JSONs
- OR any changed file mentions `https://ragpiq.bubbleapps.io` or `https://ragpiq.com/api/1.1/wf/` outside of CDN URLs

## Why

Ragpiq's frontend proxy at `app/api/business/upload/n8n/route.ts` already sends a `bubble_env` parameter to n8n with values `"production"` (live) or `"development"` (test). The n8n workflow nodes need to USE this parameter to route Bubble calls to the right env. Otherwise localhost dev writes data into LIVE Bubble (or vice versa) and silently fails.

This was the root cause of the 30-min n8n debugging session in PR #42 testing — sub-workflows had hardcoded `https://ragpiq.bubbleapps.io/api/1.1/wf/1_add_images` URLs that always pointed live, even when the trigger came from localhost test env.

## What "correct" looks like

Env-aware expression in the URL field of every HTTP node that calls a Bubble workflow:

```
={{ $('Webhook').item.json.body.bubble_env === "development" ? "https://ragpiq.bubbleapps.io/version-test" : "https://ragpiq.bubbleapps.io" }}/api/1.1/wf/1_add_images
```

(For sub-workflows that don't have direct webhook access, the parent must pass `bubble_env` via Edit Fields / Set node BEFORE invoking the sub.)

## What "incorrect" looks like (flag these)

```
https://ragpiq.bubbleapps.io/api/1.1/wf/anything
https://ragpiq.com/api/1.1/wf/anything       ← also wrong; same issue
```

(CDN URLs like `https://0ddd...cdn.bubble.io/...` are FINE — those serve images and are env-agnostic.)

## Defaults to encode

When suggesting code to the user:

- New HTTP node calling a Bubble workflow → suggest the env-aware expression
- Existing hardcoded LIVE URL → flag as bug, suggest replacement
- Existing `version-test`-only URL → flag as test-only bug (won't work in prod)

## Output format

```
⚠ Hardcoded LIVE Bubble URL detected.
  Pattern: https://ragpiq.bubbleapps.io/api/1.1/wf/1_add_images
  → Replace with env-aware:
    ={{ $('Webhook').item.json.body.bubble_env === "development" ? "https://ragpiq.bubbleapps.io/version-test" : "https://ragpiq.bubbleapps.io" }}/api/1.1/wf/1_add_images
  → For sub-workflows: ensure parent passes bubble_env via Edit Fields/Set
    BEFORE invoking; reference: AI LISTING ALL → Edit Fields5/6
```

## Pre-requisite

This check assumes the n8n env-routing rule is documented in the frontend `CLAUDE.md`. If not, add it (see spec doc — pre-requisite section). Without the CLAUDE.md rule, Anthropic's review won't catch the same bugs via Agent #1.
