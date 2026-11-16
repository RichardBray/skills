---
name: person-swap-video
metadata:
  version: "0.1.0"
description: "Put a different person into a recorded video, keeping the original camera, motion, timing and mouth movements, then swap in a new voice track. Runs prunaai/p-video-2-pro-replace on Replicate with one identity image, and optionally upscales with prunaai/p-video-upscale. Use when someone asks to swap, replace or recast the person in a video with a character or a photo (for example 'put Maya in this video', 'replace me with this woman', 'redo this take with the new voice'). The scene stays the source video's scene: a different room, a different framing or a talking head made from a still image is not this skill."
---

# person-swap-video

Takes a source video and one portrait and returns the same video with the portrait's person in it. The camera, framing, background, timing, gestures and lip movements come from the source, so the source performance carries the result. Output is as long as the source (1 to 120 s) and keeps its aspect ratio.

## What you need

- `REPLICATE_API_TOKEN` in the environment. Never write it into a file or a prompt.
- Bun and ffmpeg on the path.
- A source video of someone performing the line in the room and framing the final video should have. The model does not change the room, so record the source where the result should be.
- One identity image: a clear, well-lit portrait of the character, already wearing the outfit the video should show. Make the outfit in the image, not only in the prompt.
- Optional: a voice file (mp3 or wav) that has the same timing as the source audio. The lips follow the source audio, so a replacement voice has to match it word for word.

## Flow

### Phase 1: Look before you spend

1. Pull one frame from the source: `ffmpeg -ss 3 -i src.mov -frames:v 1 frame.jpg`, and look at it. Note who is in it, the room, the aspect ratio and the length.
2. Check the length. Up to 120 s runs in one pass; do not split it, because separate takes drift at the join.
3. Work out the cost: seconds times the rate, in whole seconds.

| Resolution | Per second | Notes |
|---|---|---|
| 480p | $0.025 | drafts |
| 768p | $0.05 | the default, native |
| 1080p | $0.06 | generated at 768p and upscaled |
| 2k | $0.07 | upscaled |
| 4k | $0.09 | upscaled |

**Check:** you know the room, the length and the cost, and the identity image has the right outfit.

### Phase 2: Run the swap

```sh
bun swap.ts --video src.mp4 --image face.jpg --resolution 768p \
  --prompt "Replace the person in the video with the woman in the reference image, keeping her face and hair exactly. She wears <outfit>. Copy the motion, timing, gestures and mouth movements from the video exactly. <anything held in hand, or: Her hands stay low and out of frame.> Natural window light, realistic skin, no filters." \
  --out swap.mp4
```

- Describe only what is in the source and the identity image. Naming an object the image does not show (a microphone, say) makes the model invent one.
- Use a short, cheap clip at `--resolution 480p` to test a new identity image before a full run.
- The script creates the prediction once. It retries only on a 429 (rate limit) and never re-creates a prediction after a failed poll or download, because every prediction is billed. If a download fails, the output stays at the printed URL for about an hour.

**Check:** `swap.mp4` exists, the script printed the seconds and cost, and you have watched it: face, hair, outfit, hands and mouth sync.

### Phase 3: Voice (optional)

Add `--audio voice.mp3` to the same command to lay a replacement voice over the result without re-encoding the video, or run ffmpeg yourself:

```sh
ffmpeg -i swap.mp4 -i voice.mp3 -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 192k -shortest out.mp4
```

For a less crisp, roomier voice that fits a kitchen or living room, add `--room`. It applies this chain to the voice only: a gentle high cut, short reflections and loudness levelling.

```
highpass=f=90,equalizer=f=5500:t=h:w=2000:g=-3,lowpass=f=10000,aecho=0.85:0.9:18|31|47:0.22|0.14|0.08,loudnorm=I=-16:TP=-1.5:LRA=9
```

This is a rough room, not a real reverb. Tune the echo gains (the last three numbers) if it is too wet or too dry.

**Check:** the voice file and the video are the same length to within a frame, and you have listened to the result.

### Phase 4: Upscale (optional)

Run `prunaai/p-video-upscale` with `target: "1080p"` on the finished file. It keeps the audio, keeps the aspect ratio and the frame rate, and costs $0.02 a second at 1080p (2k $0.04, 4k $0.08). Because the aspect ratio is kept, a 480×832 source comes out 1094×1896, not 1080×1920; crop about 14 px from each side with ffmpeg and scale to 1080×1920 for a Reel.

Do not upscale with the swap model's own 1080p setting if the take is already approved: that re-runs the swap and the result changes.

**Check:** the output size, frame rate and audio are as expected.

## Replicate pitfalls

- A 403 with `error code: 1010` is Cloudflare rejecting the default User-Agent. Send a curl-style one.
- An account under $5 of credit is limited to 6 creates a minute with a burst of 1. Run requests one after another, never in parallel.
- The output host rejects an `Authorization` header, so download without it.
- Pass files by uploading to `https://api.replicate.com/v1/files` and using the returned `urls.get`, or as base64 data URIs for small images.
- Search the model's schema and price page before calling it; do not guess field names.

## What does not work

- `bytedance/seedance-2.5`: it takes a reference video and several images, but its real-person filter rejects a photoreal face, including an AI-generated one (`InputImageSensitiveContentDetected.PrivacyInformation`). A face from Seedream on the same BytePlus ModelArk account, an authorized real-person asset or a preset digital character are the documented ways through. Seedance 2.5 on Replicate also caps clips and reference video at 30 s and 720p.
- `alibaba/wan-3`: text and first-frame image to video only, no driving video.
- `prunaai/p-video-2-pro-avatar`: makes a talking head from a still and audio. The movement is invented, not copied from a real performance, and looked less natural than the swap.
- Changing the room or the aspect ratio: the swap keeps the source scene.

## Pointers

- Model and prices: https://replicate.com/prunaai/p-video-2-pro-replace and https://replicate.com/prunaai/p-video-upscale
- The script: `swap.ts` in this folder. Tested end to end on a 2 s clip at 480p, including the voice swap and `--room`.
