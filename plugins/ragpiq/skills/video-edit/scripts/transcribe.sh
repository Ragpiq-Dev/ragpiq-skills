#!/bin/bash
# Transcribe any clip with whisper. JSON lands next to OUTBASE.
#   ./transcribe.sh CLIP.MOV outbase        -> outbase.json (segment timestamps)
#   ./transcribe.sh CLIP.MOV outbase -w     -> word-level timestamps (-ml 1)
# Model lives permanently at the path below — never re-download it.
set -euo pipefail
MODEL="$HOME/Library/Application Support/whisper-models/ggml-base.en.bin"
SRC="$1"; OUT="$2"; WORDS="${3:-}"
[ -f "$MODEL" ] || { echo "whisper model missing: $MODEL (huggingface.co/ggerganov/whisper.cpp, ggml-base.en.bin, 141 MB)"; exit 1; }
WAV="$(mktemp -t wtx).wav"
ffmpeg -v error -y -i "$SRC" -vn -ac 1 -ar 16000 -c:a pcm_s16le "$WAV"
if [ "$WORDS" = "-w" ]; then
  whisper-cli -m "$MODEL" -f "$WAV" -ml 1 -oj -of "$OUT" --print-progress false >/dev/null
else
  whisper-cli -m "$MODEL" -f "$WAV" -oj -of "$OUT" --print-progress false >/dev/null
fi
rm -f "$WAV"
echo "wrote $OUT.json"
