#!/usr/bin/env python3
"""Build a Ragpiq video from an EDL job file — authentic picture, one encode generation.

Usage:
    python3 edl_build.py job.json                 # shareable output (x265 crf 24)
    python3 edl_build.py job.json --master        # camera-bitrate archive (videotoolbox 60M)

Job file (JSON):
{
  "sources": [
    {"path": "/Users/patro/Downloads/IMG_4233.MOV", "afilter": "highpass=f=75,volume=7.0dB"},
    {"path": "/Users/patro/Downloads/IMG_4236.MOV", "afilter": "highpass=f=75,volume=4.4dB"}
  ],
  "segments": [[0, 3.30, 7.80], [1, 0.45, 5.90]],      // [sourceIdx, inSec, outSec]
  "out": "OUT_reel.mp4"
}

Hard-coded on purpose (Pat's standing rules, 2026-07-30 — do not add options for these):
  * cuts straight from the originals — NO proxies, NO scaling, NO fps change, NO LUT/grade
  * hard cuts only, NO video fades anywhere (10 ms audio de-click ramps only)
  * colour/fps/resolution tags propagated from source 0 exactly as shot
Audio (approved): per-source level match via "afilter", loudnorm -14 LUFS master, limiter.
"""
import json, subprocess, sys


def probe(path, entries, stream="v:0"):
    """Return requested stream fields as a dict (ffprobe emits them in ITS order,
    never trust positional output)."""
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", stream,
                        "-show_entries", f"stream={entries}", "-of", "default=nw=1", path],
                       capture_output=True, text=True)
    d = {}
    for line in r.stdout.strip().split("\n"):
        if "=" in line:
            k, v = line.split("=", 1)
            d[k] = "" if v in ("unknown", "N/A") else v
    return d


def main():
    job = json.load(open(sys.argv[1]))
    master = "--master" in sys.argv
    srcs, segs, out = job["sources"], job["segments"], job["out"]

    meta = probe(srcs[0]["path"],
                 "r_frame_rate,color_primaries,color_transfer,color_space,pix_fmt")
    fps = meta.get("r_frame_rate", "30")                     # e.g. "60/1"
    prim = meta.get("color_primaries", "")
    trc = meta.get("color_transfer", "")
    space = meta.get("color_space", "")
    pixfmt = meta.get("pix_fmt", "")
    ten_bit = "10" in pixfmt

    R = 0.010
    fc, vs, as_, total = [], [], [], 0.0
    for i, (idx, a, b) in enumerate(segs):
        d = b - a
        af = srcs[idx].get("afilter", "highpass=f=75")
        fc.append(f"[{idx}:v]trim=start={a}:end={b},setpts=PTS-STARTPTS,fps={fps},settb=AVTB[v{i}]")
        fc.append(f"[{idx}:a]atrim=start={a}:end={b},asetpts=PTS-STARTPTS,{af},"
                  f"afade=t=in:st=0:d={R},afade=t=out:st={d - R:.4f}:d={R},"
                  f"aresample=48000,aformat=channel_layouts=mono,asettb=AVTB[a{i}]")
        vs.append(f"[v{i}]"); as_.append(f"[a{i}]"); total += d

    fc.append("".join(x + y for x, y in zip(vs, as_)) +
              f"concat=n={len(segs)}:v=1:a=1[vout][acat]")
    fc.append("[acat]loudnorm=I=-14:TP=-1.5:LRA=11,alimiter=limit=0.95,"
              "aformat=channel_layouts=stereo:sample_rates=48000[aout]")

    cmd = ["ffmpeg", "-v", "error", "-y"]
    for s in srcs:
        cmd += ["-i", s["path"]]
    cmd += ["-filter_complex", ";".join(fc), "-map", "[vout]", "-map", "[aout]"]

    if master:
        cmd += ["-c:v", "hevc_videotoolbox", "-b:v", "60M",
                "-pix_fmt", "p010le" if ten_bit else "nv12", "-tag:v", "hvc1"]
        if ten_bit:
            cmd += ["-profile:v", "main10"]
    else:
        cmd += ["-c:v", "libx265", "-crf", "24", "-preset", "fast",
                "-pix_fmt", "yuv420p10le" if ten_bit else "yuv420p", "-tag:v", "hvc1"]
        x265 = "log-level=error"
        if prim and trc and space:
            x265 = f"colorprim={prim}:transfer={trc}:colormatrix={space}:" + x265
        cmd += ["-x265-params", x265]

    if prim:  cmd += ["-color_primaries", prim]
    if trc:   cmd += ["-color_trc", trc]
    if space: cmd += ["-colorspace", space]
    cmd += ["-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out]

    print(f"{len(segs)} segments -> {out}  ({'master 60M' if master else 'share x265 crf24'}, "
          f"fps={fps}, {pixfmt}, {trc or 'no colour tags'})  predicted {total:.2f}s")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print(r.stderr[-3000:]); sys.exit(1)
    print("done")


if __name__ == "__main__":
    main()
