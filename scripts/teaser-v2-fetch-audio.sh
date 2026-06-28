#!/usr/bin/env bash
# re-fetch the V2 teaser audio (free, no login): Kevin MacLeod "The Descent" (CC-BY) + Mixkit SFX (Mixkit Free, no attribution)
set -e; cd "$(dirname "$0")/.."; A=assets/teaser-v2/audio; mkdir -p "$A/sfx"
curl -sL -o "$A/the-descent.mp3" "https://incompetech.com/music/royalty-free/mp3-royaltyfree/The%20Descent.mp3"
for pair in wind:1153 rain:2404 thunder:1296 leaves:2427 drips:3179 drone:2745 gear:885 riser:632 shimmer:871 hammer:833 crowd:444 coin:1999 impact:788 shortriser:790 forgehammer:836; do
  n="${pair%:*}"; id="${pair#*:}"; curl -sL -o "$A/sfx/sfx-$n.mp3" "https://assets.mixkit.co/active_storage/sfx/$id/$id-preview.mp3"
done
echo "fetched music + sfx. Re-run scripts/teaser-stage... or copy into teaser/public/ as needed."
