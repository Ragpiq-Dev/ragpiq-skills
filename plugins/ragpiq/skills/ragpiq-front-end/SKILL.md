---
name: ragpiq-front-end
description: How Ragpiq builds front ends. House rules for copy, spacing, layout, one-decision-at-a-time flows, and the house drawings and their animation (3D renders at product-photograph quality, one mascot for every person). Use whenever you design, build or restyle anything a user will see in a Ragpiq repo, including pages, screens, components, wizards, forms, dialogs, empty states, email templates, illustrations and animated graphics. Trigger on requests like "build the page for X", "add a screen", "create the signup flow", "redesign this", "improve the UX", "make an SVG for X", "draw an illustration" or "animate this graphic", and on any feature work that touches UI, even if the user never mentions design. Follow it ahead of generic design guidance. Skip it only for work with no user-facing surface, such as pure API, script or data changes.
---

# Ragpiq Front End

Less is more. A Ragpiq screen asks one question at a time, in as few words as possible, with air around everything and one big drawing doing the talking. These rules apply to everything a user sees, from a full flow to a single empty state or email, and they beat generic design instinct. Data-dense internal surfaces (admin tables, dashboards) keep the word and spacing discipline; the one-decision flow shape governs consignor and reseller-facing screens.

Three failures keep coming back, and each has a rule below: too many words (whatever you draft first is, so cut 70 to 80% of it), words a stranger has to decode (say it plainly), and things packed against each other (give everything air). When a screen looks wrong, it is nearly always one of these.

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
- Failures arrive as toasts, not inline field errors. After repeated failure, offer "Finish later".
- An already-completed screen shows a quiet confirmation (masked data, small edit link), not a refillable form.
- Reuse the repo's existing step frame and input styles before building new ones.

## Words

If a screen needs a paragraph, it needs another screen. Whatever you draft first is three to five times too long, and the page gets 70 to 80% fewer words than that draft.

- Cut 70 to 80% of the first draft before it goes on the page. Every sentence you want to add is one the reader has to get past to do the thing they came for. Restyling an existing screen? Cut the same share out of its words before you touch the layout. When two versions both work, the shorter one ships.
- No subheadings. A screen has one title, and nothing under it is a heading. A part of the page that wants its own heading is a second screen, a row, or nothing. Space separates the parts.
- Titles are a question or an imperative, 7 words or fewer. Aim for 4. "Name your shop." "Where do you sell?"
- At most one help line under the title, 15 words or fewer. The whole screen stays under 25.
- Plain words a stranger gets first time. Write for someone on a phone, in a hurry, who has never heard our words for things: short common words, the verb up front, one idea per sentence. If a line would need explaining to a friend, rewrite it. Not: "Awaiting settlement". This: "On its way". Not: "Handover scheduled". This: "Drop-off booked". Not: "Verify your identity". This: "Confirm it's you".
- Anything extra lives in one bounded line: reassurance under the CTA, a one-line card, or fine print. Never a paragraph.
- An explanation lives behind a quiet ⓘ, not on the page. The label stays two or three words and takes the shared InfoTip beside it (`components/ui/InfoTip.tsx` in ragpiq-frontend: a popover, not a tooltip, so it works on touch); one or two short sentences open on hover or tap, only for the people who want them. Column headers and stat labels take the ⓘ after the word: Consign ⓘ, Cash ⓘ on the check-in rates table is the shape.
- Buttons morph instead of multiplying: "Skip for now" becomes "Continue" once something is filled in.
- Busy labels are a verb with an ellipsis: "Saving…".
- AU English. A sentence ends in a full stop or a question mark and is joined to the next thought by a comma or a colon. Never an em dash. Never a semicolon: make it two sentences. Never a dot, bullet or pipe between two bits of text: not "3 items · $450", not "Melbourne | 2 km". Two facts get two lines, or sit at opposite ends of one line (name left, price right) with space between them. An en dash inside a range ($480 – $620) is the one exception.
- Plain and professional, never chatty. Say the thing. Not "Not a match for your racks", not "Nothing to see here", not "Oops". If a label needs a voice, it is doing too much.
- Never restate what the heading above already said. A section called "Left out" does not need "we left this one out" on every row inside it. Delete the row copy, keep the heading.
- A row in a list is usually just the name of the thing. Reach for a second line only when it carries a fact the reader cannot see: a price, a time, a count. Never a reason, never a restatement.
- Not: "Contact information. Please provide the email address where you would like to receive updates." This: "Where should updates go?"

## Buttons

A button is a shape with a name on it. Three failures keep coming back, and all three are bans.

- **Never a button that is just underlined text.** Underline is link decoration; on a touch surface it reads as emphasis, not as something to press. Every button gets a real shape: the full-width primary, or a bordered pill for a small action ("Add back", "Post it back", "What Maya said").
- **Never append a value to a label.** Not "Send offer · $450", not "Save $2,405", not "Continue with 2 connected". The label is a NAME for the action and stays put; a figure glued on grows with the data, reflows on a narrow phone, and repeats a number the screen is already showing. Put the total on the screen and let the button say what it does.
- **One or two words. Three is the ceiling.** "Save". "Send offer". "Add back". A third word has to earn its place ("Skip for now"), and a fourth never ships: "Continue and finish this later" is "Finish later", "Pass on this lot" is "No thanks". This binds everything pressable: primaries, pills, quiet links, menu items and chips.
- Two shapes only: a full-width primary (inverted ink fill, generous radius, disabled at opacity-40), and quiet text for Back and skip. The quiet slot carries no underline either.
- One quiet slot, and it morphs: Remove this piece → Cancel → Keep it. Never two quiet links side by side.
- Busy labels are a verb with an ellipsis: "Saving…".

## Layout and spacing

One narrow centred column and a lot of air. Whitespace does the separating, not borders or cards. Nothing is ever squashed.

- Content sits in a centred max-w-sm column (384px), max-w-md (448px) when the control needs it, inside a max-w-3xl page.
- Two or three type sizes per screen, never more: one large semibold title (text-2xl, 28px; up to 34px on a hero), text-sm muted body, text-xs fine print.
- Fixed rhythm: mt-2.5 (10px) title to help, mt-8 (32px) help to control, mt-10 (40px) control to CTA, space-y-4 (16px) inside groups. The px values carry the same rules into emails.
- Air on all four sides of everything. 16px (gap-4) is the least two siblings ever get, a pressable row or button is at least 44px tall (h-11), and text never touches the edge of its card, its row or the screen. If two things could be read as one, there is not enough space between them: separate with space, never with a line, a dot or a box.
- When a screen looks tight, cut words or remove an element. Spacing is never the thing that gives, and the tight look almost always comes from too many words.
- Squash-hunt before you call it done: screenshot at 375px and look at every gap. Two lines of text touching, a button against the edge, a card filled to its border, a row you cannot tell from the next: those are the tells.
- A decision screen fits one viewport: one illustration, one title, one line, one control, one CTA. If it does not fit, remove something or split the screen. Never shrink the spacing to make room.
- Buttons: see the Buttons section. Never invent a third shape.

## Drawings, animation and icons

One big drawing does the talking, and it is a 3D render.

- Every key screen gets one large drawing, 150 to 220px wide, centred above the title. Never beside it, never from a stock set.
- **A drawing is a 3D render, and so is its animation.** Asked for "an SVG", "an illustration", "a graphic" or "an animation" for a screen, make a render: a real object in real materials (card, cloth, leather, brass, glass), in the house palette, under soft studio light, casting its own ground shadow, at the quality of a product photograph. The flat line drawings read as clip art, and renders replaced them in October 2026.
- **Read [drawings.md](drawings.md), beside this file, before you make, change or place one.** It holds the look, the one studio that makes them (`ragpiq-mobile/tools/film-clips`), how a screen plays one without slowing a phone, and how a new one gets approved.
- Any person in any drawing is the mascot: long wavy chestnut hair, a black tank, a leather midi skirt. No other face, figure or hand, on any surface.
- One small movement per drawing, the thing the words under it are about, in a loop that meets itself. A render carries its own movement and its own shadow: never float one that moves, and never dress one up with sparkle accents.
- A drawing must not slow a phone down. One plays at a time, a phone short of memory gets a still, and there is an off switch that needs no release. In the user app (`ragpiq-mobile`) that is `clipOr` or `<ArtClip>` from `src/lib/art`, and nothing else plays a render.
- In an app, never scale a drawing above the size it was made at. A phone stretches it soft and a browser hides that, so anything that zooms or turns is checked on the simulator, not only in a browser.
- A render cannot change, so nothing that can change goes in one. Print a number or a word with the app's own text on a blank render, or play the render only where its number is true.
- A render's maroon is Ragpiq's. On a store's own site the drawing stays a line drawing, which takes the store's colour. That is the one place a new line drawing is still right.
- A line drawing that has not been redone yet (the website's own pages, the store app, emails) stays until someone asks. A new drawing there is a render. Never both styles on one screen, and when a render lands in a flow of line drawings, say so and offer to redo the rest.
- Every drawing holds still under prefers-reduced-motion, on the frame that best stands for it, and is always aria-hidden.
- Small icons are lucide via the size prop: 14 inside buttons, 18 to 20 in rows. An icon carries meaning or does not appear. An icon is a flat glyph, never a render.

## Never

- Never a multi-field form when a run of screens will do.
- Never a subheading. One title per screen, and space separates the parts.
- Never bullet lists or paragraphs on a screen.
- Never a word the reader has to decode. If it needs explaining, it is the wrong word.
- Never visible step counts ("Step 3 of 16"). Progress dots only, with the count sr-only.
- Never a second competing button. Morph the label instead.
- Never a button that is only underlined text. Give it a border or a fill.
- Never a value in a button label. "Send offer", not "Send offer · $450".
- Never four words on a button. One or two, three at most.
- Never a chatty or apologetic line. No "Oops", no "Nothing to see here", no "Not a match for your racks".
- Never repeat the heading in the rows beneath it.
- Never a squashed element. If it is tight, cut words, never spacing.
- Never inline error text under a field. A disabled Continue says invalid; a toast says failed.
- Never a new colour, font or button shape. Match the neighbouring screens.
- Never a new flat line drawing where a 3D render can go.
- Never a person in a drawing who is not the mascot.
- Never a number or a word in a 3D render that the data can change.
- Never a moving render in a float, and never two drawings moving at once.
- Never a drawing scaled up in an app. Make it at the largest size it is shown.
- Never an em dash, never a semicolon, and never a dot, bullet or pipe between two bits of text. Use a full stop, a comma, a colon, or a second line.

## Before you ship

- [ ] One decision on this screen, one primary action
- [ ] First draft cut by 70 to 80%, no subheadings anywhere
- [ ] Title 7 words or fewer, the whole screen under 25
- [ ] Every line reads first time to someone who has never used Ragpiq
- [ ] Fits one viewport without shrinking the spacing
- [ ] Nothing squashed: air on all four sides of everything, 16px minimum between siblings
- [ ] Drawing above the title is a 3D render (drawings.md), aria-hidden, still under reduced motion, and any person in it is the mascot
- [ ] A drawing that zooms, turns or plays over the camera was checked on the simulator at full size
- [ ] Continue disabled until valid, Enter advances, first input autofocused
- [ ] Back and skip are quiet, no second primary
- [ ] Every button has a shape, none is underlined text
- [ ] Every button is one or two words, three at most, with no value in it
- [ ] No row repeats what its heading already said
- [ ] No permanent explainer line an ⓘ could carry
- [ ] Looks like the screen beside it, nothing newly invented
- [ ] AU English. No em dash, no semicolon, no dot between two bits of text
