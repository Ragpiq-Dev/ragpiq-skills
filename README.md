# ragpiq-skills

Claude Code plugin marketplace for Ragpiq. House skills live here once; every machine and teammate installs the plugin and pulls updates from this repo.

## One-time setup (per machine)

From any Claude Code session:

```
/plugin marketplace add Ragpiq-Dev/ragpiq-skills
/plugin install ragpiq@ragpiq-skills
/reload-plugins
```

Then turn on auto-update so new skill versions arrive on their own: run `/plugin`, open the **Marketplaces** tab, select `ragpiq-skills`, choose **Enable auto-update**.

The Claude account doesn't matter; any machine that can reach this repo can install. Repos that declare this marketplace in their checked-in `.claude/settings.json` (`extraKnownMarketplaces` + `enabledPlugins`) prompt collaborators to install automatically when they trust the folder.

## Updating a skill

Edit the `SKILL.md`, open a PR, merge to `main`. That's the whole release: plugins here deliberately omit a `version` field, so every commit to `main` counts as a new version. Machines with auto-update enabled pick it up in the background (a notice suggests `/reload-plugins`, or it loads next session). Without auto-update, run `/plugin marketplace update ragpiq-skills`.

## Adding a skill

Add `plugins/ragpiq/skills/<skill-name>/SKILL.md` with `name` + `description` frontmatter and open a PR. It ships to everyone who already has the plugin; no new install step. Check your work with:

```
claude plugin validate .
```

## Contents

- **ragpiq** (plugin)
  - `ragpiq-front-end`: house UI/UX rules (copy budgets, spacing, one-decision-at-a-time flows, big SVG illustrations). Loads automatically whenever Claude works on user-facing UI.
