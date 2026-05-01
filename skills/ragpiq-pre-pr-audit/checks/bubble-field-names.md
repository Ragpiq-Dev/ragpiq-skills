# Check: Bubble field_name validation

## When to run

Any changed file under `app/api/**/route.ts` or `lib/api/**` that calls `bubbleGet`, `bubblePost`, `bubblePatch`, or `bubbleGetById`.

## Why

The Bubble Data API uses **display names (`field_name`)**, NOT `field_key`, for both filter constraints AND PATCH/POST writes. Sending the field_key returns `400 Bad Request` with no field-level detail — it just silently fails. This has shipped to production multiple times in Ragpiq history (per `CLAUDE.md` gotchas section).

## Source of truth

`reference/bubble.schema.json` in the frontend repo — a snapshot of every Bubble table, every field, every option-set value.

Each field in the schema has TWO names:
- `field_key` — Bubble's internal slug. Examples: `activity_type_option_item_activity`, `Name_PRODUCT-deleted`, `holder_product_user`. **DO NOT SEND.**
- `field_name` — The display name. Examples: `Activity Type`, `Name_PRODUCT`, `owner_PRODUCT`. **THIS is what the API expects.**

## What the check does

The skill's `scripts/grep-bubble-calls.sh` script:

1. Greps the changed file(s) for any `key: "..."` or `sortField: "..."` or top-level keys in the JSON body of a `bubbleGet/Post/Patch` call
2. Looks up each candidate key in `reference/bubble.schema.json`
3. If the candidate is found ONLY as a `field_key` (not as a `field_name`) → flag as error
4. If the candidate is a constraint `value` for an option-set field → check case-sensitive match against the option-set's `display` values
5. If the value matches a `db_value` but not a `display` → flag (some Bubble setups want display)

## Common confusions

| Mistake | Why it happens | Fix |
|---------|----------------|-----|
| Sending `activity_type_option_item_activity: "Upload"` | Field_key looks descriptive; people copy-paste from Bubble's editor | Send `"Activity Type": "Upload"` instead |
| Sending `status_offer: "Pending"` | Looks right (capitalized) | Schema says option-set `display: "pending"` (lowercase) |
| Filtering by `_id` | Bubble exposes `_id` as the canonical id field | Actually OK — `_id` is special |
| Sorting by `Created Date` | Display name has a space | Correct — keep the space |

## Output format

```
⚠ app/api/business/test-route/route.ts:55
  Sending "activity_type_option_item_activity" to Bubble.
  → That's the field_key. Expected the field_name "Activity Type".
  → Schema: reference/bubble.schema.json → item_activity → field_name: "Activity Type"

⚠ app/api/business/.../route.ts:38
  Constraint key "status_offer" with value "Pending".
  → status_offer is correct (it's a field_name) ✓
  → But "Pending" doesn't match the option-set. Expected "pending" (lowercase).
  → Schema: reference/bubble.schema.json → option_sets → "offer-status" → values
```

## Schema staleness

If `reference/bubble.schema.json` was last refreshed > 30 days ago (per its `version_synced_at` top-level field), append:

```
ℹ Bubble schema last refreshed N days ago. Field-name validation is
  only as fresh as the schema. Consider refreshing if you've added new
  Bubble fields recently.
```

## False positives

The check warns, doesn't error-halt. If the user has a legitimate reason (e.g. using Bubble's `Search for` API which DOES accept some field_keys), they ship anyway — the warning is in the audit report so Pat sees it too.
