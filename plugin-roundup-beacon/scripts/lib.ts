import { resolve } from "node:path";

// The payoff intro's deck: the topic's own icon and colours (never the Firecrawl logo), a count and three result cards.
// icon: an .svg/.png file in the video folder, inlined as a data URI (the page loads nothing from outside).
export type Intro = { icon: string; accent: string; soft: string; ink: string; pill?: string; count: number; label: string; cards: Array<[string, string, string]> };

export type Tool = { chip: string; prompt: string; win: string };

export type Cfg = {
  fcPos: number;
  hookRadius?: number;
  css?: string;
  L: string[];
  NAMES: string[];
  harness: string;
  hookLogo: string;
  noun: string;
  barW?: number;
  fcPrompt: string;
  subs: string[];
  tools: Tool[];
  say?: Record<string, string>;
  // "payoff": the hook opens on a 3D deck of result cards (`intro`, drawn by motion.ts) instead of the "?" tiles.
  // "custom": the whole hook is a hand-made motion graphic over a blank page; none of the standard hook layers are built.
  variant?: "control" | "payoff" | "custom";
  // The spoken (and shown) hook, replacing "Stop using <harness> without these five <noun>." Fish tags allowed.
  hookLine?: string;
  intro?: Intro;
};

export async function loadCfg(dir: string): Promise<Cfg> {
  const mod = (await import(resolve(dir, "cfg.ts"))) as { default: Cfg };
  return mod.default;
}

// Returns the value after --name, `true` for a bare flag, undefined when absent.
export function opt(argv: string[], name: string): string | true | undefined {
  const i = argv.indexOf(`--${name}`);
  if (i < 0) return undefined;
  const next = argv[i + 1];
  return next && !next.startsWith("--") ? next : true;
}

export const r3 = (n: number): number => Math.round(n * 1000) / 1000;
