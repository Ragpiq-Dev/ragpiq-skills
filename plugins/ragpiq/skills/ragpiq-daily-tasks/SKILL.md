---
name: ragpiq-daily-tasks
description: Turn Pat and Gwynn's morning planning chat (a Wispr Flow or voice transcript with no speaker labels, plus any typed notes) into the day's task list in the Notion "| CALENDAR" database, split between Pat and Gwynn as Signals and Noises, each timeboxed on today's calendar. Use when someone pastes a planning transcript, says "do our task list", "make today's tasks", "timebox the day", "put this in Notion", or asks for signals and noises for the day.
---

# Ragpiq daily task list

The day's list lives in Notion on the "| Calendar & Tasks" page
(https://app.notion.com/p/d8753cfc7a254d688107efe5f25c5b6d), in the
"| CALENDAR" database. Its data source is
`collection://b0e552e2-1c40-4c72-acda-80c285308f64`. Each person has a board
view grouped by Priority, and the calendar view shows the day's time blocks.

## The two sizes

- **Signal**: multi-hour work. Two or three per person per day, no more.
- **Noise**: about half an hour. Up to a dozen per person.
- Other Priority values: `Complete` (log something already done in the chat),
  `On Hold` (on the list, not today; leave the date empty), `In Review`.

## People (Notion user ids for `Assigned`)

| Person | id |
|---|---|
| Pat | 5677b0dd-efce-4f01-b352-0ea833492e57 |
| Gwynn | 160d872b-594c-8160-b337-0002041b5312 |
| Peter | 3c0d872b-594c-81a6-87cb-0002cea5a830 |
| Billy | 375d872b-594c-8154-8ee6-0002af313724 |

## Steps

1. **Read what is already open** before writing anything:
   `SELECT url, Name, Priority, Assigned, "date:Date:start", "date:Date:end" FROM "collection://b0e552e2-1c40-4c72-acda-80c285308f64" WHERE Priority IN ('Signal','Noise','In Review','On Hold') OR date("date:Date:start") = date('now') ORDER BY createdTime DESC`.
   When a topic already has a task (a long-running build, a store, a trip),
   EXTEND it: insert a dated section at the top (`## 19 Oct (planning chat)`
   plus checkboxes, then a `---`), re-date it, and change its Priority if the
   chat did. Never make a duplicate. Note any meetings already on today's
   calendar (interviews, calls): they are fixed points for step 5.
2. **Work out who said what.** The transcript has no speaker labels, so read
   for clues and check the code when unsure:
   - Gwynn builds the buyer side of the one app: the Shop, Piq chat (the
     Instinct-style shopping agent), Connect Gmail/Outlook, cart, Apple Pay,
     buyer invites, and submits iOS builds. `git log --format='%an'` in
     `ragpiq-mobile` shows `gwynnk-ragpiq` on that work.
   - Pat builds the seller side: the walk (waterfall), the pricing desk,
     consignment, allocation tech, the wardrobe rules, and stitches releases
     together.
   - Follow names said aloud: the person who says "I'll pass this to Gwynn"
     is Pat.
   - What is still unclear, ask with the question tool, grouped, at most four
     questions, your best reading first. Never guess who owns money, people or
     personal admin.
3. **Check the facts the tasks rest on**, so each task says what is actually
   left, not what was said in passing: `git log origin/dev` in
   `ragpiq-frontend` and `ragpiq-mobile`, the switches in
   `ragpiq-frontend/lib/features/`, and read-only SELECTs on production
   (`ayzitxcxfcyrgcafirpb`) for counts and names.
4. **Write the tasks** with `notion-create-pages`, parent
   `{"data_source_id": "b0e552e2-1c40-4c72-acda-80c285308f64"}`, all in one
   call with `allow_async: false` so the URLs come back:
   - `Name`: two to four words, Title Case ("Call Secondo", "Walk Switch").
   - `Priority`, `Assigned` (array of ids), `Focus Area` (Technology,
     Operations, CRM, Marketing).
   - Body: one line of context, then `- [ ]` checkboxes. Link related pages
     with `<mention-page url="...">`, dates with `<mention-date start="..."/>`.
     Only mention a page whose URL you have read back; never guess one.
5. **Timebox the day.** Every task for today gets a time block, so each
   person can see their day on the calendar view.
   - Start from now: `TZ=Australia/Melbourne date`, rounded up to the next
     quarter hour. Store times in UTC, the way the database already does:
     `"date:Date:start": "2026-10-19T00:15:00Z"`, `"date:Date:end": ...`,
     `"date:Date:is_datetime": 1`. Melbourne is UTC+11 in daylight saving
     (October to April) and UTC+10 otherwise.
   - Signals get 3 to 4 hour blocks; noises 15 to 30 minutes.
   - **Overlap on purpose.** Pat and Gwynn run several Claude sessions at
     once, often five things at a time, so noises sit on top of a running
     signal. Never stack them end to end as if one person did one thing.
   - Fixed points first: meetings already on the calendar, anything said
     "now", "at lunch" or "tonight". Leave lunch, about 12:30 to 13:15.
   - Order by what waits on what: a task that needs someone else's handoff
     starts after that handoff's block ends.
   - Tomorrow's tasks keep a date only, unless a time was said. On Hold keeps
     no date. A Complete task keeps today's date with no time.
   - Read the blocks back with a SELECT and check them before reporting.
6. **Report back** as two short tables (Pat, Gwynn), Signals then Noises, with
   links and their times, plus anything changed on existing tasks. Then stop.

## Writing rules

- Use people's and stores' names, never a description of a person, and no
  he/she. Look the name up (CRM `reseller.name_curator`, `app_user`) when the
  chat only describes someone ("the guy with the Balenciaga").
- Store names are spelled as in the CRM; transcripts mishear them
  ("Secando" is Secondo, "Anywhere Shop" is anywearshop, "Maraki" is Meraki
  Muse, "Star Collab" is StyleColab, "Kenned's" is Kennards, the storage
  facility).
- No em dashes. Short words. A noise says the one thing to do.
- A promote or a production switch in a task: say whether promotes are locked
  (`curl -s https://www.ragpiq.com/api/promote-lock`).
