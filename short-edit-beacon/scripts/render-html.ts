// Renders a page with window.__frame(t) to numbered PNGs. Usage: bun render-html.ts <page.html> <outdir> <seconds> [fps]
import { readdirSync, mkdirSync } from "node:fs";
import { homedir } from "node:os";
const [page, outDir, secs, fpsArg = "30"] = process.argv.slice(2);
const fps = Number(fpsArg), n = Math.round(Number(secs) * fps);
mkdirSync(outDir, { recursive: true });
const cache = `${homedir()}/Library/Caches/ms-playwright`;
const dir = readdirSync(cache).filter((d) => d.startsWith("chromium_headless_shell-")).sort().at(-1)!;
const sub = readdirSync(`${cache}/${dir}`).find((d) => d.startsWith("chrome-headless-shell"))!;
const port = 9334;
const proc = Bun.spawn([`${cache}/${dir}/${sub}/chrome-headless-shell`, "--headless", "--hide-scrollbars", "--allow-file-access-from-files", `--remote-debugging-port=${port}`, "about:blank"], { stderr: "ignore", stdout: "ignore" });
let targets: any[] = [];
for (let i = 0; i < 50 && !targets.length; i++) { await Bun.sleep(200); try { targets = (await (await fetch(`http://127.0.0.1:${port}/json`)).json()).filter((t: any) => t.type === "page"); } catch {} }
const ws = new WebSocket(targets[0].webSocketDebuggerUrl);
await new Promise((r) => (ws.onopen = r));
let id = 0; const pending = new Map<number, (v: any) => void>();
ws.onmessage = (e) => { const m = JSON.parse(String(e.data)); if (m.id && pending.has(m.id)) { pending.get(m.id)!(m.result); pending.delete(m.id); } };
const send = (method: string, params: any = {}) => new Promise<any>((r) => { const i = ++id; pending.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
await send("Emulation.setDeviceMetricsOverride", { width: 1080, height: 1920, deviceScaleFactor: 1, mobile: false });
await send("Page.enable");
await send("Page.navigate", { url: `file://${page}` });
await Bun.sleep(1500);
for (let f = 0; f < n; f++) {
  await send("Runtime.evaluate", { expression: `window.__frame(${f / fps})` });
  const { data } = await send("Page.captureScreenshot", { format: "png" });
  await Bun.write(`${outDir}/f${String(f).padStart(4, "0")}.png`, Buffer.from(data, "base64"));
}
ws.close(); proc.kill();
console.log(n, "frames");
