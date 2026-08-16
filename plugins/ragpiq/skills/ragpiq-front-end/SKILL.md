---
name: ragpiq-front-end
description: How Ragpiq builds front ends. House rules for copy, spacing, layout, one-decision-at-a-time flows and the big-SVG illustration style. Use whenever you design, build or restyle anything a user will see in a Ragpiq repo, including pages, screens, components, wizards, forms, dialogs, empty states and email templates. Trigger on requests like "build the page for X", "add a screen", "create the signup flow", "redesign this" or "improve the UX", and on any feature work that touches UI, even if the user never mentions design. Follow it ahead of generic design guidance. Skip it only for work with no user-facing surface, such as pure API, script or data changes.
---

# Ragpiq Front End

Less is more. A Ragpiq screen asks one question at a time, in as few words as possible, with air around everything and one big drawing doing the talking. These rules apply to everything a user sees, from a full flow to a single empty state or email, and they beat generic design instinct. Data-dense internal surfaces (admin tables, dashboards) keep the word and spacing discipline; the one-decision flow shape governs consignor and reseller-facing screens.

## One decision at a time

Ask for one thing, then move on. A five-field form is five screens.

- Screen skeleton, top to bottom: progress dots → illustration → title → one help line → the one control → full-width Continue → optional quiet line → quiet Back.
- Continue is disabled until the input is valid. That is the validation UI.
- Enter advances (a real form submit). The first input is autofocused.
- The title is the field's visual label. Keep the real label sr-only.
- Fields that form one mental unit stay together: first and last name, BSB and account number.
- Address is search-first: one search box, with granular fields behind an "Edit details" disclosure.
- A fully optional step stays one screen, so skipping stays one tap.
- Skips are quiet. Morph the Continue label ("Skip for now") or add one secondary line, never a competing button.
- Failures arrive as toasts, not inline field errors. After repeated failure, offer "Continue and finish this later".
- An already-completed screen shows a quiet confirmation (masked data, small edit link), not a refillable form.
- Reuse the repo's existing step frame and input styles before building new ones.

## Words

If a screen needs a paragraph, it needs another screen.

- Titles are a question or an imperative, 7 words or fewer. Aim for 4. "Name your shop." "Where do you sell?"
- At most one help line under the title, 15 words or fewer. The whole screen stays under 25.
- Draft the copy, then cut 60%. Restyling existing UI? Cut 60% of the words before touching the layout.
- Anything extra lives in one bounded line: reassurance under the CTA, a one-line card, or fine print. Never a paragraph.
- Buttons morph instead of multiplying: "Skip for now" becomes "Continue" once something is filled in.
- Busy labels are a verb with an ellipsis: "Saving…".
- AU English. No em dashes, ever. An en dash in a range ($480 – $620) is fine.
- Plain and professional, never chatty. Say the thing. Not "Not a match for your racks", not "Nothing to see here", not "Oops". If a label needs a voice, it is doing too much.
- Never restate what the heading above already said. A section called "Left out" does not need "we left this one out" on every row inside it. Delete the row copy, keep the heading.
- A row in a list is usually just the name of the thing. Reach for a second line only when it carries a fact the reader cannot see: a price, a time, a count. Never a reason, never a restatement.
- Not: "Contact information. Please provide the email address where you would like to receive updates." This: "Where should updates go?"

## Buttons

A button is a shape with a name on it. Two failures keep coming back, and both are bans.

- **Never a button that is just underlined text.** Underline is link decoration; on a touch surface it reads as emphasis, not as something to press. Every button gets a real shape: the full-width primary, or a bordered pill for a small action ("Add back", "Post it back", "What Maya said").
- **Never append a value to a label.** Not "Send offer · $450", not "Save $2,405", not "Continue with 2 connected". The label is a NAME for the action and stays put; a figure glued on grows with the data, reflows on a narrow phone, and repeats a number the screen is already showing. Put the total on the screen and let the button say what it does.
- Two or three words, ever. "Send offer". "Save". "Add back". "Pass on this lot" is the outside edge, and it is a quiet link, not a primary.
- Two shapes only: a full-width primary (inverted ink fill, generous radius, disabled at opacity-40), and quiet text for Back and skip. The quiet slot carries no underline either.
- One quiet slot, and it morphs: Remove this piece → Cancel → Keep it. Never two quiet links side by side.
- Busy labels are a verb with an ellipsis: "Saving…".

## Layout and spacing

One narrow centred column and a lot of air. Whitespace does the separating, not borders or cards.

- Content sits in a centred max-w-sm column (384px), max-w-md (448px) when the control needs it, inside a max-w-3xl page.
- Two or three type sizes per screen, never more: one large semibold title (text-2xl, 28px; up to 34px on a hero), text-sm muted body, text-xs fine print.
- Fixed rhythm: mt-2.5 (10px) title to help, mt-8 (32px) help to control, mt-10 (40px) control to CTA, space-y-4 (16px) inside groups. The px values carry the same rules into emails.
- A decision screen fits one viewport: one illustration, one title, one line, one control, one CTA. If it does not fit, remove something or split the screen. Never shrink the spacing to make room.
- Buttons: see the Buttons section. Never invent a third shape.

## Illustration and icons

One big drawing does the talking.

- Every key screen gets one large hand-built inline SVG, 150 to 220px wide, centred above the title. Never beside it, never from a stock set.
- House style: ink outlines (strokeWidth 2, round caps and joins), soft paper fills, and at most one accent colour, reusing the accent the surrounding flow already uses. A soft radial glow sits behind, with a gentle drop shadow.
- Motion is a slow float (about 6s, ease-in-out, infinite) with quiet sparkle accents. Everything respects prefers-reduced-motion with a calm static composition, and the art is always aria-hidden.
- Small icons are lucide via the size prop: 14 inside buttons, 18 to 20 in rows. An icon carries meaning or does not appear.

## Never

- Never a multi-field form when a run of screens will do.
- Never subheadings, bullet lists or paragraphs on a screen.
- Never visible step counts ("Step 3 of 16"). Dots only; keep the count sr-only.
- Never a second competing button. Morph the label instead.
- Never a button that is only underlined text. Give it a border or a fill.
- Never a value in a button label. "Send offer", not "Send offer · $450".
- Never a chatty or apologetic line. No "Oops", no "Nothing to see here", no "Not a match for your racks".
- Never repeat the heading in the rows beneath it.
- Never inline error text under a field. A disabled Continue says invalid; a toast says failed.
- Never a new colour, font or button shape. Match the neighbouring screens.
- Never an em dash, anywhere. Use a comma, colon or full stop.

## Before you ship

- [ ] One decision on this screen, one primary action
- [ ] Title 7 words or fewer; the whole screen under 25
- [ ] Fits one viewport without shrinking the spacing
- [ ] Illustration above the title, aria-hidden, reduced-motion safe
- [ ] Continue disabled until valid, Enter advances, first input autofocused
- [ ] Back and skip are quiet, no second primary
- [ ] Every button has a shape, none is underlined text
- [ ] Every button label is two or three words with no value in it
- [ ] No row repeats what its heading already said
- [ ] Looks like the screen beside it, nothing newly invented
- [ ] AU English, no em dashes
