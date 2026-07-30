#!/usr/bin/env python3
"""Find real speech runs (and the gaps between them) in a 16 kHz mono WAV.

Whisper's word boundaries drift; this is the exact tool. Threshold adapts to the
clip: midpoint of the p20/p90 RMS levels over 50 ms windows.

Usage:  python3 speech_runs.py clip.wav [start_s end_s]
        (make the wav first:  ffmpeg -i CLIP.MOV -vn -ac 1 -ar 16000 -c:a pcm_s16le clip.wav)

Cutting rule this exists to serve: only cut inside a gap. If two words share a
run with no gap between them (e.g. "Vinted and other..."), there is NO clean cut
point — extend the segment to the end of the sentence instead.
"""
import sys, wave, array, math

p = sys.argv[1]
w = wave.open(p)
sr = w.getframerate()
lo = float(sys.argv[2]) if len(sys.argv) > 2 else 0.0
hi = float(sys.argv[3]) if len(sys.argv) > 3 else w.getnframes() / sr

w.setpos(int(lo * sr))
a = array.array("h")
a.frombytes(w.readframes(int((hi - lo) * sr)))
step = int(sr * 0.05)
rows = []
for i in range(0, len(a) - step, step):
    c = a[i:i + step]
    r = math.sqrt(sum(x * x for x in c) / len(c)) + 1e-9
    rows.append((lo + i / sr, 20 * math.log10(r / 32768)))

vals = sorted(v for _, v in rows)
p90, p20 = vals[int(len(vals) * 0.90)], vals[int(len(vals) * 0.20)]
th = (p90 + p20) / 2
print(f"# {p} {lo:.2f}-{hi:.2f}s  p90={p90:.1f} p20={p20:.1f} thresh={th:.1f} dB")

speech, st = False, None
for t, v in rows:
    if v >= th and not speech:
        speech, st = True, t
    elif v < th and speech:
        if t - st >= 0.15:
            print(f"  SPEECH {st:7.2f} -> {t:7.2f}  ({t - st:.2f}s)")
        speech = False
if speech:
    print(f"  SPEECH {st:7.2f} -> {hi:7.2f}")
