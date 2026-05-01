#!/usr/bin/env python3
"""
pr-template.py — auto-generate PR title + body from branch state.

Usage:
  python3 pr-template.py --title              # print title only
  python3 pr-template.py --body                # print full body
  python3 pr-template.py --body --audit-report '...'   # include audit summary

Auto-population rules:
  Title: latest commit subject; prefer feat() over fix(); truncate to 70 chars
  Summary: first few commits + spec doc top section (if found)
  Bug fixes: commits with fix(...) prefix
  Architecture: git diff --stat grouped by directory
  Test plan: static template + change-type detection

Designed to be POSIX-friendly + zero external deps.
"""

import argparse
import os
import re
import subprocess
import sys
from collections import defaultdict


def run(cmd):
    """Run a shell command and return stdout (or empty on failure)."""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, check=False
        )
        return result.stdout.strip()
    except Exception:
        return ""


def get_base_branch():
    """Detect the base branch (main or master)."""
    if run("git show-ref --verify --quiet refs/heads/main"):
        return "main"
    return "master"


def get_commits(base):
    """Return commits on this branch, newest first.
    Each commit is a dict: {sha, subject, type}."""
    log = run(f"git log --pretty=format:'%H|%s' origin/{base}..HEAD")
    if not log:
        return []
    commits = []
    for line in log.splitlines():
        parts = line.split("|", 1)
        if len(parts) != 2:
            continue
        sha, subject = parts
        type_match = re.match(r"^(\w+)(?:\(.+?\))?:", subject)
        commits.append({
            "sha": sha,
            "subject": subject,
            "type": type_match.group(1) if type_match else "",
        })
    return commits


def pick_title(commits):
    """Pick the headline commit subject; prefer feat over fix."""
    feats = [c for c in commits if c["type"] == "feat"]
    if feats:
        title = feats[0]["subject"]
    elif commits:
        title = commits[0]["subject"]
    else:
        title = "(no commits)"
    return title[:70]


def categorize_files(base):
    """Group changed files by category for the architecture section."""
    diff = run(f"git diff origin/{base} --name-status")
    if not diff:
        return {}, {}
    new_by_cat = defaultdict(list)
    mod_by_cat = defaultdict(list)
    for line in diff.splitlines():
        parts = line.split("\t")
        if len(parts) < 2:
            continue
        status, path = parts[0], parts[-1]
        cat = pick_category(path)
        bucket = new_by_cat if status == "A" else mod_by_cat
        bucket[cat].append(path)
    return dict(new_by_cat), dict(mod_by_cat)


def pick_category(path):
    if path.startswith("app/api/"):
        return "API routes"
    if path.startswith("components/") or (
        path.startswith("app/") and path.endswith(".tsx")
    ):
        return "Frontend"
    if path.startswith("lib/"):
        return "Lib"
    if path.startswith("content/") or path.endswith(".mdx"):
        return "Docs/MDX"
    if path.startswith("docs/superpowers/specs"):
        return "Specs"
    if path.startswith("docs/superpowers/plans"):
        return "Plans"
    if "n8n" in path.lower() and path.endswith(".json"):
        return "n8n workflows"
    if path == "CLAUDE.md":
        return "Dev infra"
    return "Other"


def has_category(new_by_cat, mod_by_cat, cat):
    return cat in new_by_cat or cat in mod_by_cat


def render_architecture(new_by_cat, mod_by_cat):
    out = []
    if any(new_by_cat.values()):
        out.append("**New files:**")
        for cat, files in sorted(new_by_cat.items()):
            for f in files:
                out.append(f"- `{f}` — _{cat}_")
    if any(mod_by_cat.values()):
        out.append("")
        out.append("**Modified files:**")
        for cat, files in sorted(mod_by_cat.items()):
            for f in files:
                out.append(f"- `{f}` — _{cat}_")
    return "\n".join(out)


def render_bug_fixes(commits):
    fixes = [c for c in commits if c["type"] == "fix"]
    if not fixes:
        return ""
    out = ["### Bug fixes uncovered", ""]
    for c in fixes:
        out.append(f"- {c['subject']}")
    return "\n".join(out) + "\n"


def render_test_plan(new_by_cat, mod_by_cat):
    has_frontend = has_category(new_by_cat, mod_by_cat, "Frontend")
    has_api = has_category(new_by_cat, mod_by_cat, "API routes")
    has_n8n = has_category(new_by_cat, mod_by_cat, "n8n workflows")
    has_mdx = has_category(new_by_cat, mod_by_cat, "Docs/MDX")

    out = ["## Test plan", ""]
    out.append("- [ ] TypeScript clean (✓ verified by audit)")
    out.append("- [ ] Lint clean (✓ verified by audit)")
    if has_frontend:
        out.append("- [ ] Visual audit at 1920/768/375 (✓ verified by audit)")
        out.append("- [ ] No new console errors (✓ verified by audit)")

    if has_frontend:
        out.append("\n### Frontend changes")
        out.append("- [ ] Sign in as reseller, walk through happy path")
        out.append("- [ ] Test on mobile viewport")
        out.append("- [ ] Verify no layout shift on slow network")
    if has_api:
        out.append("\n### API changes")
        out.append("- [ ] Test with valid auth")
        out.append("- [ ] Test with invalid auth")
        out.append(
            "- [ ] Verify Bubble field_names against `reference/bubble.schema.json`"
        )
        out.append("- [ ] Confirm error responses are graceful")
    if has_n8n:
        out.append("\n### n8n changes")
        out.append(
            "- [ ] Workflow updated AND deployed live (n8n auto-saves but verify active)"
        )
        out.append("- [ ] Test execution on test env")
        out.append("- [ ] Confirm bubble_env routing correct")
    if has_mdx:
        out.append("\n### Brand-voice changes")
        out.append(
            "- [ ] Reads in Ragpiq voice (per `../ragpiq-ops/marketing/brand/voice/_core.md`)"
        )
    return "\n".join(out)


def find_spec_plan_paths(base):
    """Look for new files under docs/superpowers/specs or plans."""
    diff = run(f"git diff origin/{base} --name-only")
    spec, plan = None, None
    for line in diff.splitlines():
        if line.startswith("docs/superpowers/specs/") and line.endswith(".md"):
            spec = line
        elif line.startswith("docs/superpowers/plans/") and line.endswith(".md"):
            plan = line
    return spec, plan


def render_notes(spec, plan, audit_report=""):
    out = ["## Notes for review", ""]
    if spec:
        out.append(f"- Spec: `{spec}`")
    if plan:
        out.append(f"- Plan: `{plan}`")
    out.append("")
    if audit_report:
        out.append("### Pre-PR audit")
        out.append(audit_report)
    return "\n".join(out)


def render_body(commits, base, audit_report=""):
    new_by_cat, mod_by_cat = categorize_files(base)
    summary = "\n".join(f"- {c['subject']}" for c in commits[:3])
    body = []
    body.append("## Summary\n")
    body.append(summary)
    body.append("")
    fixes = render_bug_fixes(commits)
    if fixes:
        body.append(fixes)
    body.append("### Architecture\n")
    body.append(render_architecture(new_by_cat, mod_by_cat))
    body.append("")
    spec, plan = find_spec_plan_paths(base)
    if spec or plan:
        body.append("### How it works\n")
        body.append("See spec / plan linked below for full design context.\n")
    body.append(render_test_plan(new_by_cat, mod_by_cat))
    body.append("")
    body.append(render_notes(spec, plan, audit_report))
    body.append("")
    body.append("🤖 Generated with [Claude Code](https://claude.com/claude-code) via /audit-pr")
    return "\n".join(body)


def main():
    parser = argparse.ArgumentParser(description="Generate PR title or body")
    parser.add_argument("--title", action="store_true", help="Print title only")
    parser.add_argument("--body", action="store_true", help="Print full body")
    parser.add_argument(
        "--audit-report",
        default="",
        help="Audit findings to include in 'Pre-PR audit' section",
    )
    parser.add_argument("--base", default="", help="Base branch (default: auto-detect)")
    args = parser.parse_args()

    base = args.base or get_base_branch()
    commits = get_commits(base)

    if args.title:
        print(pick_title(commits))
        return
    if args.body:
        print(render_body(commits, base, args.audit_report))
        return
    parser.print_help()
    sys.exit(1)


if __name__ == "__main__":
    main()
