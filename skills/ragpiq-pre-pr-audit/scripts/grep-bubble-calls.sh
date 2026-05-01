#!/usr/bin/env bash
# grep-bubble-calls.sh — extract Bubble call constraints from changed files
# and validate keys against reference/bubble.schema.json
#
# Usage: bash grep-bubble-calls.sh [base-branch]
#   base-branch defaults to "main"
#
# Output: list of (file:line, key, verdict) triples

set -euo pipefail

BASE_BRANCH="${1:-main}"
SCHEMA_FILE="reference/bubble.schema.json"

if [ ! -f "$SCHEMA_FILE" ]; then
  echo "ℹ Schema file not found at $SCHEMA_FILE — skipping field_name validation"
  exit 0
fi

# Find changed files that look like they call Bubble
CHANGED=$(git diff "origin/$BASE_BRANCH" --name-only -- 'app/api/**/*.ts' 'lib/api/**/*.ts' 2>/dev/null || true)

if [ -z "$CHANGED" ]; then
  echo "ℹ No Bubble-touching API files changed"
  exit 0
fi

echo "Scanning changed Bubble calls..."

# Extract every constraint key from the changed files
# Pattern: { key: "..." OR sortField: "..." inside a bubbleGet/Post/Patch call
TMPFILE=$(mktemp)
trap "rm -f $TMPFILE" EXIT

for f in $CHANGED; do
  if [ -f "$f" ]; then
    # Find lines with key: "..." or sortField: "..."
    grep -nE '(key|sortField):\s*"[^"]+"' "$f" 2>/dev/null | while IFS= read -r line; do
      lineno=$(echo "$line" | cut -d: -f1)
      content=$(echo "$line" | cut -d: -f2-)
      # Extract the quoted value
      keyvalue=$(echo "$content" | grep -oE '"[^"]+"' | head -1 | tr -d '"')
      if [ -n "$keyvalue" ]; then
        echo "$f:$lineno|$keyvalue" >> "$TMPFILE"
      fi
    done

    # Also find body keys in JSON.stringify({ ... })
    # This is simpler — look for keys that match suspect patterns
    grep -nE '"[a-z_]+(_option_|_text|_number|_image|_user|_boolean)[a-z_]*":' "$f" 2>/dev/null | while IFS= read -r line; do
      lineno=$(echo "$line" | cut -d: -f1)
      content=$(echo "$line" | cut -d: -f2-)
      keyvalue=$(echo "$content" | grep -oE '"[a-z_]+(_option_|_text|_number|_image|_user|_boolean)[a-z_]*"' | head -1 | tr -d '"')
      if [ -n "$keyvalue" ]; then
        echo "$f:$lineno|$keyvalue|SUSPECT_FIELD_KEY" >> "$TMPFILE"
      fi
    done
  fi
done

if [ ! -s "$TMPFILE" ]; then
  echo "✓ No Bubble call keys found in changed files"
  exit 0
fi

# Validate each key against the schema
WARNINGS=0
while IFS='|' read -r location key marker; do
  # Look up in schema. The schema has both `field_key` and `field_name`.
  # If the key matches a `field_key` only (not a `field_name`) → warn.
  is_field_key=$(jq -r --arg k "$key" '
    [.tables[].fields[] | select(.field_key == $k) | .field_name] | length
  ' "$SCHEMA_FILE" 2>/dev/null || echo "0")

  is_field_name=$(jq -r --arg k "$key" '
    [.tables[].fields[] | select(.field_name == $k) | .field_key] | length
  ' "$SCHEMA_FILE" 2>/dev/null || echo "0")

  if [ "$is_field_key" -gt 0 ] && [ "$is_field_name" = "0" ]; then
    correct_name=$(jq -r --arg k "$key" '[.tables[].fields[] | select(.field_key == $k) | .field_name][0]' "$SCHEMA_FILE")
    echo "⚠ $location"
    echo "    Sending \"$key\" — that's a field_key (Bubble internal slug)."
    echo "    Expected the field_name: \"$correct_name\""
    echo "    Schema: $SCHEMA_FILE"
    WARNINGS=$((WARNINGS + 1))
  fi
done < "$TMPFILE"

if [ "$WARNINGS" -eq 0 ]; then
  echo "✓ All Bubble keys in changed files match field_names (or are special _id)"
else
  echo ""
  echo "Found $WARNINGS field_key issue(s). See CLAUDE.md for the field_name rule."
  exit 1
fi
