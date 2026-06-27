#!/usr/bin/env bash
# re-download the free cinematic stock clips into assets/video/footage/ (CC0 / Mixkit-Free / Pexels — commercial-OK)
set -e; cd "$(dirname "$0")/.."; D=assets/video/footage; mkdir -p "$D"
UA="Mozilla/5.0"
dl(){ curl -sL -A "$UA" -o "$D/$2.mp4" "$1"; echo "  $2 <- $1"; }
dl "https://assets.mixkit.co/videos/46147/46147-720.mp4"  fx-godrays
dl "https://assets.mixkit.co/videos/9754/9754-720.mp4"    fx-cave-entrance
dl "https://assets.mixkit.co/videos/50943/50943-1080.mp4" fx-mist
dl "https://assets.mixkit.co/videos/3009/3009-1080.mp4"   fx-forest
dl "https://assets.mixkit.co/videos/20906/20906-720.mp4"  fx-molten
dl "https://assets.mixkit.co/videos/48299/48299-720.mp4"  fx-embers
dl "https://assets.mixkit.co/videos/3463/3463-720.mp4"    fx-sparks
dl "https://videos.pexels.com/video-files/5561385/5561385-uhd_2560_1440_25fps.mp4" fx-dust
dl "https://www.pexels.com/download/video/7793218/"       fx-crystal
dl "https://www.pexels.com/download/video/14744358/"      fx-candle
echo "done."
