import { resolve } from "node:path";

// The payoff intro's deck: the topic's own icon and colours (never the Firecrawl logo), a count and three result cards.
// icon: an .svg/.png file in the video folder, inlined as a data URI (the page loads nothing from outside).
export type Intro = { icon: string; accent: string; soft: string; ink: string; pill?: string; count: number; label: string; cards: Array<[string, string, string]> };

// The custom variant's intro, drawn by `motion.ts hook` and timed from hook-words.json (Fish speech_to_text of v0).
// Shown words are matched in order to the spoken ones ("5" matches "five"; up to two spoken words may go unshown).
// burst: words slam in, a highlighter hits `mark`, emoji app tiles explode and shrink to five on the bar.
// desk: line 1 types out, line 2 slams in with `mark` coloured, a stack of cards is dealt and the first is stamped,
//   the remaining lines rise in, five tiles drop and the bar sweeps in.
// Both end on the regular "?" slot row. The harness logo (cfg.hookLogo) sits before the first shown harness name.
export type Hook = {
  style: "burst" | "desk";
  lines: string[];
  bar: string;
  mark: string;
  accent: string;
  // burst: the highlighter (default #ffe14d); desk: underline, stamp and every other tile (default #14b8a6).
  second?: string;
  // Emoji: burst 30 (the 4th, 12th, 18th, 23rd and 29th stay), desk 5 hinting at the tools in scene order.
  tiles?: string[];
  // desk: [name, detail, avatar colour]; the first is kept and stamped, the others are flicked away.
  cards?: Array<[string, string, string]>;
  stamp?: string;
};

export type Tool ={ chip: string; prompt: string; win: string };

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
  hook?: Hook;
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
