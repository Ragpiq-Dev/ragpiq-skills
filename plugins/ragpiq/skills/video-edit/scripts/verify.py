#!/usr/bin/env python3
"""Verify a built video BEFORE showing it to anyone. Catches what eyes on contact
sheets miss: clipped words, doubled lines, loudness misses, accidental fades,
and colour drift from the camera original.

Usage:
    python3 verify.py OUT.mp4                      # specs + loudness + fade check + transcript
    python3 verify.py OUT.mp4 --job job.json       # + pixel-diff vs raw source (authenticity)
"""
import json, os, subprocess, sys, tempfile

WHISPER_MODEL = os.path.expanduser(
    "~/Library/Application Support/whisper-models/ggml-base.en.bin")


def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def main():
    out = sys.argv[1]
    job = None
    if "--job" in sys.argv:
        job = json.load(open(sys.argv[sys.argv.index("--job") + 1]))
    tmp = tempfile.mkdtemp(prefix="vidverify_")

    # 1 — specs
    r = sh(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
            "stream=width,height,r_frame_rate,pix_fmt,color_transfer",
            "-show_entries", "format=duration,size", "-of", "default=nw=1", out])
    print("== specs ==\n" + r.stdout.strip())

    # 2 — loudness. Target ≈ -14 LUFS integrated; quiet non-speech openings pull it
    # 1-3 dB lower — that's normal for dialogue-led reels (platforms renormalize).
    # Worry only if it lands outside roughly -18..-12, or TP > -0.5.
    r = sh(["ffmpeg", "-hide_banner", "-i", out, "-af",
            "loudnorm=I=-14:print_format=json", "-f", "null", "-"])
    tail = r.stderr[r.stderr.rfind("{"):r.stderr.rfind("}") + 1]
    if tail:
        j = json.loads(tail)
        print(f"== loudness ==  I={j['input_i']} LUFS  TP={j['input_tp']} dB")

    # 3 — no-fade check: mean luma of the last 0.5 s must not ramp toward black
    r = sh(["ffmpeg", "-v", "info", "-sseof", "-0.5", "-i", out, "-vf",
            "scale=200:-2,signalstats,metadata=print:key=lavfi.signalstats.YAVG:file=-",
            "-f", "null", "-"])
    ys = [float(l.split("=")[1]) for l in r.stdout.splitlines() if "YAVG" in l]
    if ys:
        drop = (max(ys) - ys[-1]) / max(ys) * 100
        verdict = "OK (no fade)" if drop < 15 else f"⚠ FADE? last frame {drop:.0f}% darker than peak"
        print(f"== ending ==  luma {ys[0]:.0f} -> {ys[-1]:.0f}  {verdict}")

    # 4 — transcript of the OUTPUT (the check that catches clipped/doubled lines)
    if os.path.exists(WHISPER_MODEL):
        wav = os.path.join(tmp, "a.wav")
        sh(["ffmpeg", "-v", "error", "-y", "-i", out, "-vn", "-ac", "1", "-ar", "16000",
            "-c:a", "pcm_s16le", wav])
        sh(["whisper-cli", "-m", WHISPER_MODEL, "-f", wav, "-oj", "-of",
            os.path.join(tmp, "t"), "--print-progress", "false"])
        tj = os.path.join(tmp, "t.json")
        if os.path.exists(tj):
            print("== transcript of output (read it — check ends of sentences!) ==")
            for s in json.load(open(tj))["transcription"]:
                t = s["text"].strip()
                if t:
                    print(f"  {s['timestamps']['from'][3:-4]}-{s['timestamps']['to'][3:-4]}  {t}")
    else:
        print(f"⚠ whisper model missing at {WHISPER_MODEL} — transcript check skipped")

    # 5 — authenticity: pixel-diff mid-segment-2 frame vs its raw source frame
    if job:
        segs, srcs = job["segments"], job["sources"]
        acc = 0.0
        for i, (idx, a, b) in enumerate(segs):
            if i == 1:
                mid_out, mid_src, src = acc + (b - a) / 2, (a + b) / 2, srcs[idx]["path"]
                break
            acc += b - a
        fa, fb = os.path.join(tmp, "a.png"), os.path.join(tmp, "b.png")
        crop = "crop=in_w/2:in_h/2:in_w/4:in_h/4"
        sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{mid_out:.3f}", "-i", out,
            "-frames:v", "1", "-vf", crop, "-pix_fmt", "rgb24", fa])
        sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{mid_src:.3f}", "-i", src,
            "-frames:v", "1", "-vf", crop, "-pix_fmt", "rgb24", fb])
        import numpy as np
        from PIL import Image
        A = np.asarray(Image.open(fa), dtype=float)
        B = np.asarray(Image.open(fb), dtype=float)
        dm = abs(A.mean((0, 1)) - B.mean((0, 1))).max()
        print(f"== authenticity ==  channel-mean drift {dm:.2f}/255 "
              f"({'OK — no grade' if dm < 1.5 else '⚠ COLOUR SHIFTED — a filter got in'})  "
              f"mean|diff| {np.abs(A - B).mean():.2f}/255 (grain/codec noise)")


if __name__ == "__main__":
    main()
