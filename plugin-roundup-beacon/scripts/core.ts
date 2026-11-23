import { writeFileSync, readFileSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';
import { loadCfg } from './lib.ts';

type Item = { chip: string; logo: string; name: string; sub: string; prompt: string; win: string | null; bc: 'dark' | 'heat' };
type Rect = [string, number, number, number, number];

const DIR = resolve(process.argv[2] || process.cwd());
const cfg = await loadCfg(DIR);
const base = readFileSync(new URL('./css.txt', import.meta.url), 'utf8');
const extra = cfg.css || '';
const css = base + extra + '.prompt.tall .ptext{font-size:32px}.block{top:0!important;height:1920px!important}.block .btop{top:160px!important}.block .blogo{top:760px!important}';
const FC='The knowledge library for your agent. Live data on people, emails, jobs and more.';
const toolItems: Item[] = cfg.tools.map((t,i)=>({...t, logo:cfg.L[i+1]!, name:cfg.NAMES[i+1]!, sub:cfg.subs[i]!, bc:'dark' as const}));
const fcItem: Item = {chip:'Firecrawl', logo:'logo-orange.svg', name:'Firecrawl', sub:FC, prompt:cfg.fcPrompt, win:null, bc:'heat'};
const items: Item[] = [...toolItems]; items.splice((cfg.fcPos||1)-1,0,fcItem);
const L = items.map(i=>i.logo), NAMES = items.map(i=>i.name), N = L.length;
const page = (body: string) => `<!doctype html><meta charset=utf-8><style>${css}</style><body>${body}`;
const W = 978 / N;
const chrome = (past: number) => `<div class=slots>${L.map((l,i) => i < past ? `<div class="cell past"><img src=${l}></div>` : `<div class=cell>?</div>`).join('')}</div>`;
const slotLayer = (i: number) => `<div data-layer=slot class="cell active" style="position:absolute;left:${51+i*W}px;top:1653px;width:${W}px;height:134px;border:none"><img src=${L[i]}></div>`;
const nameSize = (n: string) => n.length > 14 ? 92 : n.length > 10 ? 112 : 128;
const prod = (idx: number, sub: string, chip: string, text: string, blockCls: string, result: string) => page(
  chrome(idx-1) + slotLayer(idx-1) +
  `<div data-layer=head class=head><span class=t style="font-size:${nameSize(NAMES[idx-1]!)}px">${NAMES[idx-1]!}</span><span class=s>${sub}</span></div>
<div data-layer=prompt class="prompt tall"><span class=chip>@${chip}</span><span class=ptext id=pt>${text}</span><div class=send>↑</div></div>
<div data-layer=cover class=cover id=cv></div><div data-layer=cursor class=cursor id=cu></div>
${result}
<div data-layer=block class="block ${blockCls}"><div class=btop><span class=bn>${idx}</span><span class=bnm style="font-size:${NAMES[idx-1]!.length>14?78:NAMES[idx-1]!.length>12?100:NAMES[idx-1]!.length>10?120:150}px">${NAMES[idx-1]!}</span></div><div class=blogo><img src=${L[idx-1]!}></div></div>
<script>
document.fonts.ready.then(()=>{const t=document.getElementById('pt').getBoundingClientRect();const c=document.getElementById('cv');
c.style.left=(t.left-4)+'px';c.style.top=(t.top-6)+'px';c.style.width=(t.width+8)+'px';c.style.height=(t.height+12)+'px';
const u=document.getElementById('cu');u.style.left=(t.left-4)+'px';u.style.top=(t.top+t.height/2-25)+'px';});
</script>`);
const ucs: Array<[string, string, string[]]> = [['People search & profiles','107.5K',['pi-fullenrich.com.png','pi-blitz-api.ai.png','pi-enrichlayer.png']],['Email & phone finding','93.5K',['pi-anymailfinder.com.png','pi-quickenrich.io.png','apollo.io.png']],['Job postings & hiring','64.6K',['pi-www.workable.com.png','pi-www.greenhouse.com.png','pi-www.ashbyhq.com.png']]];
const fcRows = ucs.map((u,i)=>`<div data-layer=uc${i} class=uc style="top:${860+i*258}px"><div class=ucl><div class=uct>${u[0]}</div><div class=ucn>${u[1]} calls · last 24h</div></div><div class=ucp>${u[2].map(x=>`<img src=${x}>`).join('')}</div></div>`).join('');
const provIcons=['www.sec.gov','apollo.io','shopify.com','wikipedia.org','tiingo.com','www.recreation.gov','benzinga.com','www.federalreserve.gov'];
const tile = (n: string, i: number) => `<div class=pwall style="left:${i*344}px;top:0"><img src=${n}.png></div>`;
const more = `<div class=pwall style="left:688px;top:0;background:#fa5d19;border-color:#fa5d19"><span class=more>&amp; more</span></div>`;
const wall = [0,1].map(r => `<div data-layer=wall${r} class=wrow style="top:${820+r*268}px">${provIcons.slice(r*3, r*3+3).map((n,i)=>tile(n,i)).join('')}</div>`).join('') + `<div data-layer=wall2 class=wrow style="top:${820+2*268}px">${provIcons.slice(6,8).map((n,i)=>tile(n,i)).join('')}${more}</div>`;
const hookRects: Rect[] | null = existsSync(resolve(DIR, 'rects-hook.json')) ? JSON.parse(readFileSync(resolve(DIR, 'rects-hook.json'), 'utf8')) as Rect[] : null;
const textRight = hookRects?.find(a => a[0] === 'plugins');
const numRect = hookRects?.find(a => a[0] === 'three');
// A long noun ("marketing plugins") overflows the frame at 128px: shrink the number and noun together so the bar ends inside it.
const k = textRight ? Math.min(1, 787 / textRight[3]) : 1;
const fs = Math.round(128 * k), nounLeft = Math.round(84 + ((numRect?.[3] ?? 84.3) + 31.7) * k), textTop = Math.round(665 + 82 * (1 - k));
const barW = textRight ? Math.round(nounLeft + textRight[3] * k + 41 - 52) : (cfg.barW || 690);
const hookTiles = [0,1,2,3,4].map(i=>`<div data-layer=t${i} style="position:absolute;left:${48+i*W}px;top:${[1000,1110,980,1090,1020][i]!}px;width:${W}px;height:240px;background:#f9f9f9"><div style="position:absolute;left:18px;top:20px;width:160px;height:160px;border-radius:40px;background:#111;box-shadow:0 20px 28px rgba(0,0,0,.30);display:flex;align-items:center;justify-content:center;color:#fff;font-size:104px;font-weight:500;line-height:1">?</div></div>`).join('');
const hook = page(`${hookTiles}
<div data-layer=stop class=w style="left:72px;top:140px;font-size:150px">Stop</div>
<div data-layer=using class=w style="left:430px;top:140px;font-size:150px">using</div>
<img data-layer=hlogo src=${cfg.hookLogo} style="position:absolute;left:72px;top:335px;width:120px;height:120px;border-radius:${cfg.hookRadius||30}px;background:#f9f9f9">
<div data-layer=hname class=w style="left:215px;top:315px;font-size:150px">${cfg.harness}</div>
<div data-layer=without class=w style="left:72px;top:490px;font-size:150px">without</div>
<div data-layer=these class=w style="left:610px;top:490px;font-size:150px">these</div>
<div data-layer=bar class=abs style="left:52px;top:651px;width:${barW}px;height:190px;background:#000;border-radius:34px"></div>
<div data-layer=three class=w style="left:84px;top:${textTop}px;font-size:${fs}px;letter-spacing:${Math.round(-5 * k * 10) / 10}px;background:#000;color:#fff;padding-right:${Math.round(12 * k)}px;padding-bottom:${Math.round(36 * k)}px">${N}</div>
<div data-layer=plugins class=w style="left:${nounLeft}px;top:${textTop}px;font-size:${fs}px;letter-spacing:${Math.round(-5 * k * 10) / 10}px;background:#000;color:#fff;padding:0 ${Math.round(12 * k)}px ${Math.round(36 * k)}px">${cfg.noun}.</div>`);
const tiles = L.map((n,i)=>`<div class=etile style="left:${i*196.4}px;top:0;width:176px;height:176px;border-radius:40px"><img src=${n} style="width:100px;height:100px"></div>`).join('');
const end = page(`${chrome(5)}
<div data-layer=f1 class=head style="top:150px"><span class=t style="font-size:112px;letter-spacing:-4px;padding-bottom:30px">Follow for more</span></div>
<div data-layer=f2 class=head style="top:290px"><span class=t style="font-size:112px;letter-spacing:-4px;color:#fa5d19;padding-bottom:30px">plugin suggestions.</span></div>
<div data-layer=tiles class=abs style="left:48px;top:760px;width:984px;height:180px">${tiles}</div>`);
const frames: Record<string, string> = { hook };
items.forEach((it,i)=>{ frames['s'+(i+1)] = prod(i+1,it.sub,it.chip,it.prompt,it.bc,it.win||(fcRows+wall)); });
frames.end = end;
for (const [k, h] of Object.entries(frames)) writeFileSync(resolve(DIR, k + '.html'), h);
console.log('core: wrote', Object.keys(frames).length, 'pages, bar width', barW);
