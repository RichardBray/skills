// Phone screenshot (400 CSS px at 2x) with cookie banners removed before capture.
// Usage: bun shot-clean.ts <out.png> <url> [height]
import { readdirSync } from "node:fs";
import { homedir } from "node:os";

const [out, url, h = "1400"] = process.argv.slice(2);
const cache = `${homedir()}/Library/Caches/ms-playwright`;
const dir = readdirSync(cache).filter((d) => d.startsWith("chromium_headless_shell-")).sort().at(-1)!;
const sub = readdirSync(`${cache}/${dir}`).find((d) => d.startsWith("chrome-headless-shell"))!;
const bin = `${cache}/${dir}/${sub}/chrome-headless-shell`;
const ua = "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1";
const port = 9333;
const proc = Bun.spawn([bin, "--headless", "--disable-gpu", "--hide-scrollbars", `--remote-debugging-port=${port}`, "about:blank"], { stderr: "ignore", stdout: "ignore" });
let targets: any[] = [];
for (let i = 0; i < 50 && !targets.length; i++) {
  await Bun.sleep(200);
  try { targets = (await (await fetch(`http://127.0.0.1:${port}/json`)).json()).filter((t: any) => t.type === "page"); } catch {}
}
const ws = new WebSocket(targets[0].webSocketDebuggerUrl);
await new Promise((r) => (ws.onopen = r));
let id = 0;
const pending = new Map<number, (v: any) => void>();
ws.onmessage = (e) => { const m = JSON.parse(String(e.data)); if (m.id && pending.has(m.id)) { pending.get(m.id)!(m.result); pending.delete(m.id); } };
const send = (method: string, params: any = {}) => new Promise<any>((r) => { const i = ++id; pending.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });

await send("Emulation.setDeviceMetricsOverride", { width: 400, height: Number(h), deviceScaleFactor: 2, mobile: true });
await send("Emulation.setUserAgentOverride", { userAgent: ua });
await send("Page.enable");
await send("Page.navigate", { url });
await Bun.sleep(9000);
await send("Runtime.evaluate", { expression: `
  for (const s of ['#onetrust-consent-sdk','#onetrust-banner-sdk','.onetrust-pc-dark-filter','[id*="sp_message"]','[class*="cookie"]','[id*="cookie"]','[class*="consent"]','[id*="consent"]','#truste-consent-track'])
    document.querySelectorAll(s).forEach(e => e.remove());
  for (const e of document.querySelectorAll('body *')) {
    const cs = getComputedStyle(e); if (cs.position !== 'fixed' && cs.position !== 'sticky') continue;
    const r = e.getBoundingClientRect();
    if (r.width * r.height > innerWidth * innerHeight * 0.6 || /cookie/i.test(e.textContent || '')) e.remove();
  }
  for (const e of [document.documentElement, document.body]) { e.style.overflow='auto'; e.style.position='static'; e.classList.remove('ot-overflow-hidden'); }
  window.scrollTo(0,0);` });
await Bun.sleep(800);
const { data } = await send("Page.captureScreenshot", { format: "png" });
await Bun.write(out, Buffer.from(data, "base64"));
ws.close();
proc.kill();
console.log(out);
