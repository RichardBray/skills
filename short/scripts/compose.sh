#!/bin/sh
# Compose a short: frames + voiceover + music + sfx -> short.mp4 (1080x1920, 30fps).
# usage: compose.sh <short-dir> [--sub 2]
# Needs in <short-dir>: frames/, voiceover.(wav|mp3|m4a), scene_times.json; optional music.mp3, sfx.wav.
set -e
d=$(cd "$1" && pwd); sub=2; [ "$2" = "--sub" ] && sub=$3
vo=$(ls "$d"/voiceover.* 2>/dev/null | head -1); [ -n "$vo" ] || { echo "no voiceover.* in $d"; exit 1; }
dur=$(python3 -c "import json;print(json.load(open('$d/scene_times.json'))[-1][2])")
fps=$((30 * sub))
ffmpeg -y -loglevel error -framerate $fps -pattern_type glob -i "$d/frames/f_*.png" \
  -vf "tmix=frames=$sub,select='eq(mod(n\,$sub)\,$((sub - 1)))',setpts=N/30/TB" -c:v libx264 -crf 14 -preset medium -pix_fmt yuv420p -r 30 "$d/video_only.mp4"
in="-i $vo"; fc="[0:a]loudnorm=I=-14:TP=-1.5,apad=whole_dur=$dur,atrim=0:$dur,asplit[vo][vo2]"; n=1; mix="[vo2]"
if [ -f "$d/music.mp3" ]; then
  in="$in -i $d/music.mp3"
  fc="$fc;[$n:a]atrim=0:$dur,afade=t=out:st=$(python3 -c "print(max(0,$dur-2.0))"):d=2,loudnorm=I=-27:TP=-3[m0];[m0][vo]sidechaincompress=threshold=0.03:ratio=5:attack=20:release=300[m]"; mix="$mix[m]"; n=$((n + 1))
fi
if [ -f "$d/sfx.wav" ]; then
  in="$in -i $d/sfx.wav"; fc="$fc;[$n:a]atrim=0:$dur,volume=-7dB[s]"; mix="$mix[s]"; n=$((n + 1))
fi
inputs=$(echo "$mix" | grep -o '\[' | wc -l)
ffmpeg -y -loglevel error $in -filter_complex "$fc;${mix}amix=inputs=$inputs:normalize=0,alimiter=limit=0.89[a]" -map "[a]" -ar 44100 "$d/mix.wav"
ffmpeg -y -loglevel error -i "$d/video_only.mp4" -i "$d/mix.wav" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest -movflags +faststart "$d/short.mp4"
echo "$d/short.mp4  $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$d/short.mp4")s  audio $(ffmpeg -hide_banner -nostats -i "$d/mix.wav" -af ebur128 -f null - 2>&1 | grep -E '^\s+I:' | tr -s ' ')LUFS"
