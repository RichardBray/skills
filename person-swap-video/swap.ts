#!/usr/bin/env bun
// Person swap on Replicate: bun swap.ts --video src.mp4 --image face.jpg --prompt "..." --out out.mp4 [--resolution 768p] [--audio voice.mp3] [--room]
import { basename } from "node:path";

const MODEL = "prunaai/p-video-2-pro-replace";
const PRICE_PER_SECOND: Record<string, number> = { "480p": 0.025, "768p": 0.05, "1080p": 0.06, "2k": 0.07, "4k": 0.09 };
// Cloudflare in front of Replicate answers the default runtime User-Agent with a 403 (error 1010).
const UA = "curl/8.7.1";

const args = new Map<string, string>();
const argv = process.argv.slice(2);
for (let i = 0; i < argv.length; i++) {
  if (!argv[i].startsWith("--")) continue;
  const next = argv[i + 1];
  args.set(argv[i].slice(2), next && !next.startsWith("--") ? argv[++i] : "true");
}

const token = process.env.REPLICATE_API_TOKEN;
const video = args.get("video");
const image = args.get("image");
const out = args.get("out");
if (!token || !video || !image || !out) {
  console.error("needs REPLICATE_API_TOKEN, --video, --image, --out");
  process.exit(1);
}
const resolution = args.get("resolution") ?? "768p";
const prompt = args.get("prompt") ?? "Replace the person in the video with the person in the reference image, keeping their face and hair exactly. Copy the motion, timing, gestures and mouth movements from the video exactly.";
const auth = { Authorization: `Bearer ${token}`, "User-Agent": UA };

async function upload(path: string): Promise<string> {
  const form = new FormData();
  form.append("content", Bun.file(path), basename(path));
  const res = await fetch("https://api.replicate.com/v1/files", { method: "POST", headers: auth, body: form });
  if (!res.ok) throw new Error(`upload ${path}: ${res.status} ${await res.text()}`);
  return ((await res.json()) as any).urls.get;
}

const [videoUrl, imageUrl] = await Promise.all([upload(video), upload(image)]);
const body = JSON.stringify({ input: { video: videoUrl, images: [imageUrl], instruction_prompt: prompt, resolution, save_audio: true } });

// Create exactly once. A failed poll or download must never create a second prediction: each one is billed.
let prediction: any;
for (let attempt = 0; attempt < 8; attempt++) {
  const res = await fetch(`https://api.replicate.com/v1/models/${MODEL}/predictions`, {
    method: "POST",
    headers: { ...auth, "Content-Type": "application/json" },
    body,
  });
  if (res.status === 429) {
    // Accounts under $5 of credit get 6 creates a minute with a burst of 1.
    await Bun.sleep(12_000);
    continue;
  }
  if (!res.ok) throw new Error(`create: ${res.status} ${await res.text()}`);
  prediction = await res.json();
  break;
}
if (!prediction) throw new Error("create: still rate limited after 8 tries");
console.log("prediction", prediction.id);

while (["starting", "processing"].includes(prediction.status)) {
  await Bun.sleep(10_000);
  prediction = await (await fetch(prediction.urls.get, { headers: auth })).json();
}
if (prediction.status !== "succeeded") throw new Error(`prediction ${prediction.id} ${prediction.status}: ${prediction.error}`);

const seconds = prediction.metrics?.video_output_duration_seconds ?? 0;
console.log(`output ${seconds}s at ${resolution}, about $${(seconds * (PRICE_PER_SECOND[resolution] ?? 0)).toFixed(2)}`);

const outputUrl = Array.isArray(prediction.output) ? prediction.output[0] : prediction.output;
// The delivery host rejects an Authorization header, so this request carries only the User-Agent.
const file = await fetch(outputUrl, { headers: { "User-Agent": UA } });
if (!file.ok) throw new Error(`download ${prediction.id}: ${file.status}; the output is still at ${outputUrl} for about an hour, do not rerun`);
await Bun.write(out, file);

const audio = args.get("audio");
if (audio) {
  const room = "highpass=f=90,equalizer=f=5500:t=h:w=2000:g=-3,lowpass=f=10000,aecho=0.85:0.9:18|31|47:0.22|0.14|0.08,loudnorm=I=-16:TP=-1.5:LRA=9";
  const muxed = out.replace(/\.mp4$/, "") + "_audio.mp4";
  const ffmpeg = ["ffmpeg", "-v", "error", "-y", "-i", out, "-i", audio, "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k"];
  if (args.has("room")) ffmpeg.push("-af", room);
  ffmpeg.push("-shortest", muxed);
  const code = await Bun.spawn(ffmpeg, { stdout: "inherit", stderr: "inherit" }).exited;
  if (code !== 0) throw new Error(`ffmpeg exited ${code}`);
  console.log("with audio:", muxed);
}
console.log("saved", out);
