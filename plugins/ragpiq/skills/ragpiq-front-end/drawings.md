# Ragpiq drawings

How Ragpiq draws, since October 2026. Read this before you make, change or place a drawing or an animated graphic, in any Ragpiq repo.

## The standard

A drawing is a 3D render. Gwynn's brief on 3 October 2026 was "really good, clean, and professional": the ink-outline drawings read as clip art, and a soft-shaded flat redraw was not enough either. The first render (a satin dress on a hanger, turning) set the bar, and every drawing in the user app followed it.

So when someone asks for "an SVG", "an illustration", "a graphic", "a picture of a person" or "an animation" for a screen, they are asking for a render at this standard, whatever word they use. A logo, an icon, a chart or a diagram is not a drawing and stays what it is.

Three things hold on every surface:

1. The look below.
2. Every person is the mascot.
3. A drawing must not make an app slower or less stable, on an older phone above all. One that looks better and plays worse is not finished.

## The look

- A real object you could pick up: card with a grain, cloth with a sheen, leather, polished brass, dark glass. Edges are softened so they catch the light. It stands on the ground and casts a soft shadow there, and parts that overlap shadow each other.
- Product-photograph calm. One object or one small group, centred, filling about two thirds to three quarters of the frame. Nothing cut off at an edge, the shadow inside the frame. The camera never moves.
- One light for every drawing: a soft warm key from the upper left, a gentle fill from the right, a rim light from behind, a little room reflection. Never light one drawing on its own, or the set stops looking like one family.
- The palette and nothing else: maroon, cream, paper white, warm stone, brass, ink. One maroon hero per drawing, the rest quiet. A parcel is brown card (chosen over cream on 4 October 2026: it says "parcel" at a glance). Cobalt only for a tiny indicator light that truly needs it.
- A see-through background. The screen puts a soft glow behind the drawing.
- It shows what the words under it say, and never a number or a promise those words do not make. The clock on "We price every piece" has no "24 hrs" on it, because the words promise a price within the hour.
- It has to read at the size it is drawn: usually 210 by 150 points, 136 by 102 in a pop-up. Fewer, bigger, chunkier things. A detail that turns to mush at real size comes out.
- One object, one build. The same swing tag, tick, coin, pin, clock, parcel and speech bubble appear in every drawing that needs one.
- Type inside a render is Poppins.
- Never ink outlines, flat cartoon fills, a glow or sparkles or stars inside the render, particles, lens flares, or a maker's logo on a phone.
- Every drawing comes out of the one studio, built from formulas, which is why the light, the materials and the mascot match. A picture from anywhere else (a stock model, a generated image) will not match the set.

### The mascot

- One mascot for every person, chosen on 3 October 2026: fair skin, long chestnut hair in loose waves with a centre part, a black tank, a black leather midi skirt, grey knee socks, black pointed heels. The face is closed smiling eyes, a small smile and a blush, with no nose and no brows.
- Wherever a screen shows a person, a figure, a face or a hand, it is the mascot: the seller, a friend, a driver, a buyer, a store's staff.
- A drawing that needs several people uses the mascot's own build with another head of hair and another top (the three friends on the invite sheet). Never a new figure.
- At small sizes draw the mascot from the hip up, so the face is big enough to read. Head to toe only when the drawing is large or the pose needs the legs.
- Never a gendered word for the mascot, or for anyone, in copy, comments or names a person can read. Write "the mascot".
- A small functional glyph (a 16px account icon, an avatar placeholder) is an icon, not a drawing of a person. Ask before swapping one.
- The first figure, with a black bob, is retired. Do not bring it back.

## Movement

- One small, calm beat per drawing: the thing the words under it are about. A tag swings, a tick presses in, a coin drops into a wallet, a clock hand goes round.
- A loop of 4 or 6 whole seconds. Every motion's period divides the loop, or eases back to where it started, so the last frame meets the first.
- A story that only goes one way never loops by running backwards. Fade it where it ends, or bring the next one in.
- Keep the moving area small and everything else perfectly still. The file is frames times how much of the picture changes, and so is the work a phone does. A whole object spinning or a big soft thing pulsing is expensive.
- Nothing moves the whole drawing. No float, no bob, no drifting camera. The render has its own movement and its own shadow, and moving a layer on every frame costs a phone more than playing the clip does.
- Choose the rest frame on purpose: the moment that best stands for the drawing. It is what shows when nothing may move.

## The studio

There is one studio, in the user app's repo: `ragpiq-mobile/tools/film-clips`. Every drawing for every app is made there, so they share one light, one kit and one mascot. Never copy the models into another repo: two copies of the mascot become two mascots. Its README has the commands. This is the map.

- No app carries a 3D engine. A drawing is modelled in three.js from formulas (no imported models), rendered ahead of time in a hidden browser, and shipped as image files.
- `stage3d.js` is the studio: the renderer, the lights, the ground shadow and the clock. Every scene is a pure function of the time in its loop, which lets the recorder step it frame by frame and makes every loop exact.
- `kit3d.js` is the shared kit: the palette, the materials, and the objects many drawings share. `mascot3d.js` is the mascot. Look at `kit.html` before building an object, and put a new shared object in the kit.
- `scenes/<family>.js` holds the drawings by family: tags, parcels, money, maps, places, talk, garments, small, how, lead. Each exports `SCENES`: an id, the box the screen draws it in, the loop length, and one `mount` per version.
- `scene.html?m=<family>&id=<id>` shows one drawing at its real size.
- `sheet.mjs <family>` photographs each drawing at four moments and at real size onto one sheet. Judge the real-size column hardest. A drawing is rarely right before its third sheet.
- `art-table.mjs` lists every drawing that ships. `record.mjs` films them as see-through frames and `encode.py` turns the frames into files.
- `review/` builds the page a set is approved on (see "Getting one approved").
- The recorder borrows its browser (Playwright) from the website's checkout. Adding a package to an app changes `package.json`, which forks its over-the-air runtime.

What ships, per drawing, is three files: the loop (an animated WebP with a see-through background), its first frame (what shows before it plays, so starting never jumps), and its still (the rest frame).

The settings are decisions, not defaults: 20 frames a second, 2.5 times the size in points (3 times for the small ones in a pop-up), quality 70 with alpha 85. Twice the size was visibly soft on a phone. It is an animated image and not a video because a video player takes over the phone's audio session, which the camera screen needs next, and a video has no see-through background.

Everything named here reached `ragpiq-mobile` in October 2026. A checkout with no `src/lib/art` is older than that work: update it. If `dev` itself does not have it yet, stop and ask before building anything.

## Making a new one

1. Read the words on the screen and the box the drawing sits in. The drawing says what the words say.
2. Build it in the studio, in the family it belongs to, from the kit. One version, or two where there is a real choice.
3. Sheet it, judge the real-size column, fix it, and sheet it again until it is right.
4. Show it on localhost and get a yes.
5. Add it to the table, record, encode, and place it with `clipOr` or `<ArtClip>`.
6. Look at the built screen at phone width, run the tests that hold the sizes, and measure it on the simulator if its loop or its box is bigger than usual.

## Playing a drawing

Measured on an iPhone simulator on 4 October 2026. The line drawings held 10 to 18 percent of a processor core for as long as they were on screen. A render holds 8 to 20 percent for its first three or four seconds and then about 2 percent, as long as these rules are kept. Android and real phones were not measured: measure there before trusting the numbers.

1. One plays at a time, the one in front. A drawing on a slide that is not showing, on a screen under the one in front, or under an open sheet or pop-up shows its first frame and waits.
2. Never the phone's own decoder for an animated WebP. On iOS it starts again from the first frame for every frame it shows, so a long clip can hold most of a core. Use the image library's decoder (`useAppleWebpCodec={false}` on `expo-image`) and turn off downscaling (`allowDownscaling={false}`), which otherwise resizes every frame.
3. Never move it. No float, no bob, no transform that changes on every frame.
4. A still, not the loop, under reduced motion, on a phone with 3 GB of memory or less, and when the off switch is on.
5. Keep an off switch that needs no release. In the user app it is the PostHog flag `art-stills`.
6. Memory is frames times width times height times 4 bytes, held while it plays and released when it leaves: 80 frames at 525 by 375 pixels is 63 MB. A longer loop, more frames a second or a bigger box all cost memory. Keep loops short and boxes modest.
7. The download is a budget, held by a test. The user app's 62 drawings are about 15 MB.

In the user app all of this lives in one place, `src/lib/art`:

- `export const MyArt = clipOr(MyArtLine, () => ({ id: "my-art", width: 210, height: 150 }))` where there is a line drawing to keep for a store's site, or `<ArtClip id="my-art" width={210} height={150} />` where there is not.
- A sheet or a pop-up wraps what it shows in `ArtOverlay`, and a paged sheet tells each slide whether it is the one on show with `ArtOnShow`. That is all a new kind of overlay has to do.
- Never draw a clip with a bare image component.

Only the user app's code plays renders so far (its web export included). The first drawing in another codebase brings these rules with it:

- The store app is the same kind of app, with the same image and device packages already installed. Bring `src/lib/art` across. Do not rewrite it.
- A website page takes the loop in a plain `<img>`, the still under `prefers-reduced-motion`, and one moving drawing in view at a time.
- An email takes the still, as a PNG.

## What a render cannot do

- It cannot change. Nothing the data can change goes in one: a price, a discount, a name, a count. Print it with the screen's own text on a blank render (the "keep it listed" tag), or play the render only where its number is true (the gift card clip plays only where the card says $50). A number the copy fixes, like the $100 floor on the price tag, can be in the render, and changing that number then means rendering again.
- It cannot take a store's colour. Its maroon is Ragpiq's. A drawing that can appear on a store's own site keeps a line drawing for that case.
- It cannot be made on the phone. Never add a 3D engine to an app.

## Getting one approved

- A new look gets one drawing approved first. The rest follow only after that.
- Mock it up before building it in. A drawing is looked at on localhost, at real size, before any app code changes. The built screen is looked at on localhost again before it goes to staging.
- A set is reviewed once, not batch by batch. Build every drawing, with two versions only where there is a real choice, and give one review page: today's drawing beside the new one at the size it has on a phone, a pick per drawing with your own pick marked, the few decisions that cover many drawings at the top, and one button that accepts every pick. `tools/film-clips/review` builds that page. Build into the app only after the picks.
- Say what it costs, in numbers, without being asked: processor and memory before and after on the simulator, the megabytes added to the download, the app's size beside the other marketplace apps, and what was not measured.

## The line drawing

A line drawing is still right in one place: a store's own site, where the drawing has to take the store's colour. It is also what every drawing that has not been redone still is (the website's own pages, the store app, emails).

- A hand-built inline SVG: ink outlines (stroke 2, round caps and joins), soft paper fills, and one accent colour, the one the flow around it uses. A soft radial glow behind it and a slow float (about 6s, ease-in-out). Still under reduced motion, and aria-hidden.
- Any person in it is a still of the 3D mascot, never a drawn figure.
- Never a new one where a render can go, and never both styles on one screen. When a render lands in a flow of line drawings, say so and offer to redo the rest of the flow.
