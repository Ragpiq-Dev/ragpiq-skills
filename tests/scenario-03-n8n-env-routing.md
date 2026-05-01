# Scenario 03 — n8n env-routing (LIVE Bubble URL hardcoded)

## Setup
You are a Ragpiq engineer adding a new HTTP node to an n8n workflow. The workflow is `((SUB)) FRONT STANDARD` and you're adding a step that calls a new Bubble workflow named `mark_image_processed`.

The existing nodes in this workflow already call Bubble using URLs like:
```
https://ragpiq.bubbleapps.io/api/1.1/wf/1_add_images
```

You are about to add the new node with a similar URL pattern.

The repo's `CLAUDE.md` has Ragpiq-specific Bubble env routing knowledge: localhost dev hits `version-test` Bubble, production hits the live `ragpiq.bubbleapps.io`. The frontend proxy at `app/api/business/upload/n8n/route.ts` already sends a `bubble_env` parameter to n8n with values `"production"` or `"development"`.

## User prompt

> "I'm adding a new HTTP node to the ((SUB)) FRONT STANDARD n8n workflow that calls Bubble's mark_image_processed workflow. Help me write the URL. The other nodes in this workflow use https://ragpiq.bubbleapps.io/api/1.1/wf/1_add_images so I'll follow the same pattern."

## What we want to capture

- Does the agent give the user the hardcoded LIVE URL? (the easy/wrong answer)
- Does the agent ask: "is this called from a flow that needs to support test env?"
- Does the agent suggest the env-aware expression `={{ ... bubble_env === "development" ? "/version-test" : "" ...}}`?
- Does the agent reference the precedent (HTTP Request3 in MAIN NOV uses this pattern)?
- What rationalizations does the agent use to skip the env check?
