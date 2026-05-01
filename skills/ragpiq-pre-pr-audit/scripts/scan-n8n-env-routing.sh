#!/usr/bin/env bash
# scan-n8n-env-routing.sh — flag hardcoded LIVE Bubble URLs
#
# Usage: bash scan-n8n-env-routing.sh [base-branch]
#   base-branch defaults to "main"
#
# Output: warnings for any hardcoded ragpiq.bubbleapps.io workflow URLs

set -euo pipefail

BASE_BRANCH="${1:-main}"

# Files we care about: changed files that mention ragpiq Bubble URLs (excluding CDN)
CHANGED=$(git diff "origin/$BASE_BRANCH" --name-only 2>/dev/null || true)

if [ -z "$CHANGED" ]; then
  exit 0
fi

WARNINGS=0
for f in $CHANGED; do
  if [ -f "$f" ]; then
    # Look for hardcoded LIVE Bubble workflow URLs
    # Excludes CDN URLs (cdn.bubble.io)
    while IFS= read -r line; do
      lineno=$(echo "$line" | cut -d: -f1)
      url=$(echo "$line" | grep -oE '"https://ragpiq\.(bubbleapps\.io|com)/api/1\.1/wf/[^"]+"' | head -1)
      if [ -n "$url" ]; then
        # Check if there's an env switch nearby (within 5 lines)
        ctx_start=$((lineno > 5 ? lineno - 5 : 1))
        ctx_end=$((lineno + 5))
        ctx=$(sed -n "${ctx_start},${ctx_end}p" "$f" 2>/dev/null || echo "")
        if ! echo "$ctx" | grep -qE 'bubble_env|version-test'; then
          echo "⚠ $f:$lineno"
          echo "    Hardcoded Bubble URL: $url"
          echo "    No env switch nearby. Make this env-aware:"
          echo "    ={{ \$('Webhook').item.json.body.bubble_env === \"development\" ? \"https://ragpiq.bubbleapps.io/version-test\" : \"https://ragpiq.bubbleapps.io\" }}/api/1.1/wf/..."
          WARNINGS=$((WARNINGS + 1))
        fi
      fi
    done < <(grep -n 'https://ragpiq\.\(bubbleapps\.io\|com\)/api/1\.1/wf/' "$f" 2>/dev/null || true)
  fi
done

if [ "$WARNINGS" -eq 0 ]; then
  echo "✓ No hardcoded LIVE Bubble URLs in changed files"
else
  echo ""
  echo "Found $WARNINGS env-routing issue(s)."
  exit 1
fi
