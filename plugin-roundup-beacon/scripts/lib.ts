import { resolve } from "node:path";

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
