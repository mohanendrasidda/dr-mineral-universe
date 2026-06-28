#!/usr/bin/env bash
# copy the teaser's source assets into teaser/public/ (Remotion serves from there)
set -e; cd "$(dirname "$0")/.."
P=teaser/public; mkdir -p "$P"
for f in central-cavern descent mines foundry ledger vault watch campus-aboveground; do cp "assets/environments/nb/$f.png" "$P/$f.png"; done
cp assets/video/ltx-samples/descent-shaft.mp4 "$P/clip-descent.mp4"
cp assets/video/ltx-samples/descent-cavern-01.mp4 "$P/clip-cavern.mp4"
cp assets/video/footage/lincoln-dusk.mp4 "$P/clip-lincoln.mp4"
cp assets/video/footage/unl-campus-aerial.mp4 "$P/clip-campus.mp4"
for c in fx-dust fx-embers fx-sparks fx-godrays fx-forest fx-molten fx-crystal fx-candle; do cp "assets/video/footage/$c.mp4" "$P/$c.mp4"; done
for c in district-mines district-foundry district-watch; do cp "assets/video/footage/$c.mp4" "$P/$c.mp4"; done
cp assets/audio/foundry-sfx.m4a "$P/foundry-sfx.m4a"
cp assets/audio/intro-score.mp3 "$P/score.mp3"
cp assets/characters/drmineral-keeper-walk.png "$P/drmineral.png"
echo "staged teaser assets into $P"
