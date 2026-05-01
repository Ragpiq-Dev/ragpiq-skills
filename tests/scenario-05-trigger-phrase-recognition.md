# Scenario 05 — Trigger phrase recognition

## Setup
You are a Ragpiq frontend developer. Branch has commits ready. The user uses casual everyday language to ask for the PR to be created.

## User prompts (test each independently)

Test A: "Ship it 🚀"
Test B: "Ready for Pat"
Test C: "Let's open this thing up"
Test D: "Push and PR please"
Test E: "Get this in front of Pat"

## What we want to capture

- Does the agent recognize each phrase as "create a PR"?
- Does the agent treat any of these as informal ("just push, no audit")?
- For phrases without explicit "audit" mention, does the agent know to run the pre-PR audit anyway?
- Or does the agent only invoke the skill when user explicitly says "audit"?

## Why this scenario matters

Real users don't say "/audit-pr" — they say natural-language phrases. The skill's description field needs to match these triggers fuzzy enough that any "ship-this-PR" intent activates the audit. Test how far the description's trigger surface extends.
