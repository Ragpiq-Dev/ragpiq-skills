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

**Auto-update only runs in the terminal.** Claude Code refreshes a marketplace in an interactive terminal session and nowhere else, so anyone working in the desktop app stays on the version from the day they installed (one machine was five merges behind on 4 Oct 2026, with auto-update on). `ragpiq-frontend` refreshes the plugin for you at every session start (`.claude/hooks/refresh-ragpiq-skills.mjs`). In any other repo, or to update right now, run these in a terminal:

```
claude plugin marketplace update ragpiq-skills
claude plugin update ragpiq@ragpiq-skills
```

The new version loads from your next session.

The Claude account doesn't matter; any machine that can reach this repo can install. Repos that declare this marketplace in their checked-in `.claude/settings.json` (`extraKnownMarketplaces` + `enabledPlugins`) prompt collaborators to install automatically when they trust the folder.

## Updating a skill

Edit the `SKILL.md`, open a PR, merge to `main`. That's the whole release: plugins here deliberately omit a `version` field, so every commit to `main` counts as a new version. Terminal sessions with auto-update enabled pick it up in the background (a notice suggests `/reload-plugins`, or it loads next session). Desktop app sessions get it through the session-start refresh in `ragpiq-frontend`, or the two commands above. Anyone with write access to this repo can do this, not only the person who usually does.

## Adding a skill

Add `plugins/ragpiq/skills/<skill-name>/SKILL.md` with `name` + `description` frontmatter and open a PR. It ships to everyone who already has the plugin; no new install step. Check your work with:

```
claude plugin validate .
```

## Contents

- **ragpiq** (plugin)
  - `ragpiq-front-end`: house UI/UX rules (copy budgets, plain words, spacing, button labels, one-decision-at-a-time flows, the house drawings). Loads automatically whenever Claude works on user-facing UI.
  - `ragpiq-todo`: turns work that just shipped into a short list of what to do next, action items only, under Setup / Test / Won't work / Your call. Ask "what do I need to do" or "how do I test this".
  - `video-edit`: how Ragpiq cuts and ships social video — transcript-driven editing with the picture untouched (no filters, native 4K60 HDR, hard cuts, no fades) and a verify loop that re-transcribes the output before anyone watches. Ships working scripts (`edl_build.py`, `verify.py`, cut-point + transcription helpers). Human-facing standard: `ragpiq-ops` → `operations/sops/2026-07-30-video-content-standard.md`.
