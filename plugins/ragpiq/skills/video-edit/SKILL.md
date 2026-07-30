---
name: video-edit
description: How Ragpiq cuts and ships social video — transcript-driven editing of raw phone footage into reels, with the picture untouched (no filters, native 4K60 HDR) and a verification loop that catches clipped words, fades, and colour drift before anyone watches. Use for any "edit this video / cut a reel / make a post from these clips" task.
audience: internal
---

# video-edit — cut the story, never touch the picture

Proven end-to-end on the 2026-07-30 office walk-in reel (9 iterations with Pat).
Everything here exists because a round of feedback demanded it; don't relitigate
the rules, and don't "improve" the picture.

## The non-negotiables (Pat's standing rules)

1. **Never alter the image.** No LUT, no grade, no tone-map, no denoise-on-video,
   no sharpening, no speed ramps unless asked. Editing = cutting + audio.
2. **Native everything.** Keep source resolution (don't downscale 4K to 1080),
   source fps (60 — dropping to 30 also *amplifies* mains light flicker), source
   bit depth/colour (iPhone = HLG/BT.2020 10-bit). Deliver HDR as HDR.
3. **No fades, hard cuts only.** No dissolves, no wipes, no fade-to-black ending.
   (Inaudible 10 ms audio de-click ramps at joins are fine and expected.)
4. **One encode generation.** Cut straight from the camera originals in a single
   filter graph. Proxies are for *analysis only*, never in the delivery path.
5. **No burned-in captions, music, or sound effects.** Platform adds those
   natively (IG/TikTok music gets algorithmic preference anyway).
6. **Verify, don't assert.** Run `scripts/verify.py` before showing anything.

## Editing style

- **First 3 seconds must intrigue** — an entry, a knock, a reveal. Cold-opening
  on a payoff shot is allowed but Pat prefers curiosity from the scene itself.
- **Keep arrival/entry moments** (walk-ins, knocks, mic handovers). They're the
  human beat; don't trim them to save seconds.
- **Newest take wins** — retakes have higher filenames (IMG_4238 beats IMG_4233)
  — but confirm against the transcript: newest AND clean.
- **Don't cut setup context.** If someone shows an app flow, keep the steps that
  make it legible (cart → amount → pay), not just the money shot. Over-tightening
  reads as confusing, and Pat will send it back.
- **End on complete sentences.** If two words share a speech run with no RMS gap,
  there is no clean cut — extend to the sentence end (see `speech_runs.py`).
- **Check what screens actually show at full res** before building a beat on
  them (the "$30 payment" never actually completes on camera in the reel —
  known, accepted, but it was checked).
- Segment length target: reels 20–40 s. If the asked-for content doesn't fit,
  say so and propose a split (two reels) rather than silently trimming.

## Pipeline

Work in the session scratchpad; deliver to `~/Downloads/` (top level) plus the
`~/Downloads/ragpiq-reel-cuts/` archive. `$S` below = the `scripts/` directory
next to this SKILL.md (the skill invocation shows its installed path; the source
of truth is `ragpiq-skills/plugins/ragpiq/skills/video-edit/scripts/`).

1. **Probe everything**: `ffprobe` each clip — duration, fps, rotation,
   creation_time (orders the retakes), `color_transfer` (expect `arib-std-b67`).
2. **Read the footage as images**: `$S/sheet.sh CLIP.MOV out.jpg` (1 fps sweep),
   then denser sheets (4–8 fps) on critical zones. Read them — don't guess.
3. **Transcribe every clip**: `$S/transcribe.sh CLIP.MOV tbase` (segment level),
   `-w` for word-level on the clips you'll actually cut.
4. **Find cut points**: extract 16 kHz wav, run `$S/speech_runs.py` — cut only in
   gaps; whisper boundaries drift.
5. **Level-match audio per source** (measure, don't guess): loudness of the
   *speech region only* of each clip —
   `ffmpeg -ss A -to B -i clip.wav -af loudnorm=I=-14:print_format=json -f null -`
   → set each source's `volume=XdB` in the job to bring it to the loudest one.
   Very quiet clips (distant mic) also get `afftdn=nr=12:nf=-45` (audio-only
   denoise is fine; video denoise is not).
6. **Write the EDL job** (see `examples/office-walkin-reel.json`) and build:
   `python3 $S/edl_build.py job.json` → x265 crf 24 shareable (~50 MB / 40 s of
   4K60, SSIM within 0.005 of a camera-bitrate encode).
   `--master` → videotoolbox 60 Mbps archive (~280 MB / 40 s) when asked.
7. **Verify**: `python3 $S/verify.py OUT.mp4 --job job.json`. Read the output
   transcript line by line — this is what catches clipped words, doubled lines
   ("Pretty convenient. Pretty convenient."), a surviving fade, loudness misses,
   and colour drift (channel-mean >1.5/255 means a filter got in). Also sweep
   the output with `sheet.sh` and *look* at it.
8. **Deliver**: copy to `~/Downloads/<name>.mp4` (descriptive: cut, res, size),
   SendUserFile, and state durations/sizes plainly. Iterate — Pat gives fast,
   specific feedback; expect several rounds.

## Toolchain facts (save yourself the rediscovery)

- Whisper model is permanent at
  `~/Library/Application Support/whisper-models/ggml-base.en.bin` (141 MB).
  Never re-download; never leave models in the session scratchpad.
- Homebrew ffmpeg has **no drawtext, no libass/subtitles, no zscale/libplacebo**,
  and its `colorspace` filter rejects `arib-std-b67` — every standard HDR→SDR
  chain fails. Irrelevant in normal operation (we don't tone-map), but if SDR is
  ever explicitly requested: numpy-built 33³ `.cube` + `lut3d`, and ask first.
- SSIM comparisons: encode an aligned lossless reference from the *same trim
  command* and compare at t=0. `-ss` on the source side of the ssim filter
  misaligns frames and pins SSIM at a meaningless constant.
- iPhone HEVC is ~52 Mbps because it encodes live; offline x265 crf 24 matches
  it visually at ~10 Mbps average. Sensor noise caps SSIM ≈ 0.93 for *any*
  encoder — don't chase higher.
- The office lights beat at 100 Hz; any fps drop aliases the beat into a slower,
  more visible pulse. Another reason rule 2 exists.

## Related

- Human-facing standard: `ragpiq-ops` repo, `operations/sops/2026-07-30-video-content-standard.md`
- Brand voice for the accompanying copy: `ragpiq-ops` repo, `marketing/brand/voice/_core.md`
