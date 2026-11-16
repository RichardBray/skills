// usage: [SCENES="hook s1 ..."] bun render.ts <video-dir>
// Renders every [data-layer] of each page to its own PNG and measures it into rects-<scene>.json.
// The hook runs twice: the first pass measures the "N noun." text, the second sizes the black bar to it.
import { copyFileSync, existsSync, readdirSync, rmSync, writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const HERE = dirname(fileURLToPath(import.meta.url));
const arg = process.argv[2];
if (!arg || !existsSync(arg)) {
  console.error("usage: render.ts <video-dir>");
  process.exit(1);
}
const DIR = resolve(arg);
process.chdir(DIR);

const ASSETS = resolve(HERE, "assets");
for (const f of readdirSync(ASSETS)) if (!existsSync(resolve(DIR, f))) copyFileSync(resolve(ASSETS, f), resolve(DIR, f));

const session = `roundup-${process.pid}`;
const ab = (...args: string[]): string => {
  const r = Bun.spawnSync(["agent-browser", ...args], { env: { ...process.env, AGENT_BROWSER_SESSION: session } });
  return r.stdout.toString();
};
const sleep = (ms: number) => Bun.sleep(ms);

const HIDE_ALL = "document.querySelectorAll('[data-layer]').forEach(e=>e.style.visibility='hidden')";
const LIST_IDS = "JSON.stringify([...document.querySelectorAll('[data-layer]')].map(e=>e.dataset.layer))";
const showOnly = (id: string) => `document.querySelectorAll('[data-layer]').forEach(e=>e.style.visibility=e.dataset.layer=='${id}'?'visible':'hidden')`;
const MEASURE =
  "document.querySelectorAll('[data-layer]').forEach(e=>e.style.visibility='visible');JSON.stringify([...document.querySelectorAll('[data-layer]')].map(e=>{const r=e.getBoundingClientRect();return [e.dataset.layer,Math.round(r.x*10)/10,Math.round(r.y*10)/10,Math.round(r.width*10)/10,Math.round(r.height*10)/10]}))";

const shoot = async (scenes: string[]): Promise<void> => {
  for (const f of scenes) {
    ab("open", `file://${DIR}/${f}.html`);
    await sleep(900);
    ab("eval", HIDE_ALL);
    ab("screenshot", `${DIR}/${f}-base.png`);
    const ids = ab("eval", LIST_IDS).replace(/["\\]/g, "").replace(/^\[/, "").replace(/\]\s*$/, "").trim().split(",").filter(Boolean);
    for (const id of ids) {
      ab("eval", showOnly(id));
      ab("screenshot", `[data-layer=${id}]`, `${DIR}/${f}-${id}.png`);
    }
    const rects = ab("eval", MEASURE).replace(/\\/g, "").trim().replace(/^"/, "").replace(/"$/, "");
    writeFileSync(`rects-${f}.json`, `${rects}\n`);
  }
};

const core = (): void => {
  const r = Bun.spawnSync(["bun", resolve(HERE, "core.ts"), DIR], { stdout: "inherit", stderr: "inherit" });
  if (r.exitCode !== 0) process.exit(r.exitCode ?? 1);
};

rmSync("rects-hook.json", { force: true });
core();
ab("set", "viewport", "1080", "1920");
await shoot(["hook"]);
core();
const rest = (process.env.SCENES ?? "s1 s2 s3 s4 s5 end").split(/\s+/).filter((s) => s && s !== "hook");
await shoot(["hook", ...rest]);
ab("close");
console.log(readdirSync(DIR).filter((f) => f.endsWith(".png")).length);
