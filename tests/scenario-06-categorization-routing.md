# Scenario 06 — Targeted check routing per category

## Setup
You are a Ragpiq engineer with a multi-area PR ready:
- 2 frontend components (`components/business/inventory/*`)
- 1 API route (`app/api/business/test-route/route.ts`) — touches Bubble
- 1 MDX docs page (`content/support/getting-started.mdx`)
- 0 n8n workflow changes

## User prompt

> "Audit this PR before I open it for Pat. There's a mix of changes — frontend, an API route, and a docs update."

## What we want to capture

- Does the agent run ALL checks regardless (wasteful), or run TARGETED checks per category?
- Does the agent skip the n8n env-routing check (since no n8n changes)?
- Does the agent run the brand voice check on the MDX (since marketing-facing)?
- Does the agent skip brand voice on the frontend strings (since they're internal `/business/*`)?
- Does the agent know to run the Bubble field_name validator on the API route specifically?

## Why this scenario matters

The skill's value is partly in being SMART about which checks to run, not just running everything. Tests whether the SKILL.md teaches per-category routing, or whether agents will lazily run a fixed superset of checks every time.
