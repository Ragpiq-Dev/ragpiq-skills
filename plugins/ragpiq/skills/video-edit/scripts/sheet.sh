#!/bin/bash
# Contact sheet of any clip, for reading footage as an image grid.
#   ./sheet.sh CLIP.MOV out.jpg           -> 1 fps, 5x5 tiles (each tile = 1 s)
#   ./sheet.sh CLIP.MOV out.jpg 6 6x3     -> 6 fps over a critical zone (pair with -ss/-t below)
# Extra ffmpeg input args pass through:  ./sheet.sh CLIP.MOV out.jpg 4 6x3 "-ss 12 -t 4"
set -euo pipefail
SRC="$1"; OUT="$2"; FPS="${3:-1}"; TILE="${4:-5x5}"; EXTRA="${5:-}"
# shellcheck disable=SC2086
ffmpeg -v error -y $EXTRA -i "$SRC" -vf "fps=$FPS,scale=240:-2,tile=$TILE" -frames:v 3 "${OUT%.jpg}_%02d.jpg"
ls "${OUT%.jpg}"_*.jpg
