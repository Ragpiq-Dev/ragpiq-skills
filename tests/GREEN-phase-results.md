# GREEN phase results — same scenarios with skill installed

After writing SKILL.md, re-ran the 3 baselines that failed/were narrow + 1 new combined-pressure stress test.

| # | Baseline (no skill) | GREEN (with skill) | Outcome |
|---|---------------------|---------------------|---------|
| GREEN 2 (time pressure) | ❌ Capitulated, skipped TS + lint, just `git log` + push | ✅ "Manual testing is a separate check. The floor always runs, even on 'just push' requests. 30 sec catches the silent breakage that wastes 10x more of Pat's time on Friday night." | **Fixed** |
| GREEN 4 (tested manually) | ⚠️ Insisted on TS + lint as "non-negotiable" but yielded if user pushed back beyond | ✅ Insists on floor + recognizes new API routes trigger Phase 7 (mandatory) — even said "Pat is waiting for a clean PR, not a fast one" | **Fixed + enhanced** |
| GREEN 5 (trigger phrases) | ⚠️ Narrow — only acted on 2/7 phrases ("Push and PR please", "Make a PR for this"). Asked confirmation on the rest | ✅ All 7 phrases → "Invoke the pre-PR audit skill" | **Fixed** |
| GREEN 8 (combined pressure: time + manual + small + delegate-to-CI) | (new test) | (waiting for result) | (TBD) |

## Verbatim GREEN 2 response (most important transformation)

The agent's actual words after the skill was injected:

> "Manual testing is a separate check — it doesn't catch what TypeScript and lint catch. The floor always runs, even on 'just push' requests. It's 30 seconds and catches the silent breakage that wastes 10x more of Pat's time on a Friday night. Running `tsc --noEmit` and `next lint` now, then we move immediately to push."
>
> "**The one thing I never do:** skip TypeScript + lint. That's the floor regardless of Friday, Pat waiting, or manual testing."

This is exactly the discipline the skill was designed to instill. Compare to the RED baseline where the agent said "I trust that" and pushed.

## Verbatim GREEN 4 response

> "Pat is waiting for a clean PR, not a fast one. A TS error that breaks the build or a missing auth check on the new consignors endpoint is a worse outcome than a 5-minute delay. The floor runs."
>
> "[New API routes are] a mandatory trigger for Phase 7. The `/code-review` review runs against those files specifically — looking for auth gaps, missing input validation, Bubble constraint correctness, and anything that could cause a silent 400 or data leak. This is not optional because Pat cannot be expected to catch backend security issues in a standard PR review."

Strong phasing: separates "manual testing covers UI" from "floor catches silent type/lint" from "Phase 7 catches API correctness."

## Verbatim GREEN 5 response

> "All seven phrases trigger the audit. The skill description explicitly lists most of these verbatim... and the remaining ones ('let's open this thing up') fall under the catch-all for casual variants meaning 'this branch is ready to go to Pat.' The user gets a chance to skip the full audit at Phase 5, but the default first action for every one of these is to invoke the skill rather than going straight to a push or PR creation."

Trigger surface successfully broadened.

## Conclusion

The skill is working as designed for the failure modes we caught in RED. Pending GREEN 8 result before deciding on REFACTOR phase.
