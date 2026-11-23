import { writeFileSync, readFileSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';
import { loadCfg } from './lib.ts';

type Item = { chip: string; logo: string; name: string; sub: string; prompt: string; win: string | null; bc: 'dark' | 'heat' };
type Rect = [string, number, number, number, number];

const DIR = resolve(process.argv[2] || process.cwd());
const cfg = await loadCfg(DIR);
const base = readFileSync(new URL('./css.txt', import.meta.url), 'utf8');
const extra = cfg.css || '';
// Safe zone (Reels + TikTok): x 120-960, y 250-1440; below y 840 the right edge pulls in to x 780.
const safe = `
.slots{left:120px!important;top:160px!important;width:840px!important;height:80px!important;border-radius:24px!important}.cell{height:74px!important;font-size:50px!important}.cell img{width:54px!important;height:54px!important}.cell.active::after{height:6px!important}
.head{left:120px!important;top:304px!important;width:840px!important}
.head .s{font-size:38px!important;width:840px!important;line-height:1.25!important}
.prompt{left:120px!important;top:585px!important;width:840px!important}
.prompt.tall{height:164px!important}.prompt.tall .send{top:44px!important}.prompt.tall .ptext{font-size:30px!important}
.win{left:120px!important;top:765px!important;width:840px!important;height:683px!important;border-radius:32px!important}
.uc{left:120px!important;width:840px!important;height:200px!important;padding:0 28px!important;border-radius:32px!important}
.uct{font-size:38px!important;letter-spacing:-1px!important;max-width:470px}.ucn{font-size:24px!important;margin-top:12px!important}
.ucp{gap:14px!important}.ucp img{width:76px!important;height:76px!important;border-radius:14px}
.wrow{left:120px!important;width:840px!important;height:200px!important}
.pwall{width:260px!important;height:200px!important;border-radius:32px!important}.pwall img{width:96px!important;height:96px!important}.pwall .more{font-size:40px!important}.pwall img[src^=oriane]{width:150px!important;height:150px!important}
.block .btop{left:0!important;width:1080px!important;justify-content:center!important;top:290px!important;gap:26px!important}
.block .bn{font-size:215px!important;letter-spacing:-6px!important}
.block .blogo{left:260px!important;top:620px!important;width:560px!important;height:560px!important;border-radius:130px!important}
.block .blogo img{width:320px!important;height:320px!important}
.block{top:0!important;height:1920px!important}`;
const css = base + extra + safe;
const FC=`The knowledge library for your agent. Private data sources ${cfg.harness} can't usually reach.`;
const toolItems: Item[] = cfg.tools.map((t,i)=>({...t, logo:cfg.L[i+1]!, name:cfg.NAMES[i+1]!, sub:cfg.subs[i]!, bc:'dark' as const}));
const fcItem: Item = {chip:'Firecrawl', logo:'logo-orange.svg', name:'Firecrawl', sub:FC, prompt:cfg.fcPrompt, win:null, bc:'heat'};
const items: Item[] = [...toolItems]; items.splice((cfg.fcPos||1)-1,0,fcItem);
const L = items.map(i=>i.logo), NAMES = items.map(i=>i.name), N = L.length;
const page = (body: string) => `<!doctype html><meta charset=utf-8><style>${css}</style><body>${body}`;
const W = (840 - 6) / 5;
const chrome = (past: number) => `<div class=slots>${L.map((l,i) => i < past ? `<div class="cell past"><img src=${l}></div>` : `<div class=cell>?</div>`).join('')}</div>`;
// The end slots follow the row's inner corner (24px radius less its 3px border), or their square corners poke out past it.
const slotRadius = (i: number) => i === 0 ? '21px 0 0 21px' : i === N - 1 ? '0 21px 21px 0' : '0';
const slotLayer = (i: number) => `<div data-layer=slot class="cell active" style="position:absolute;left:${123+i*W}px;top:163px;width:${W}px;height:74px;border:none;border-radius:${slotRadius(i)};overflow:hidden"><img src=${L[i]}></div>`;
const nameSize = (n: string) => Math.round((n.length > 14 ? 92 : n.length > 10 ? 112 : 128) * .8);
const blockSize = (n: string) => Math.round((n.length>14?78:n.length>12?100:n.length>10?120:150) * .72);
const prod = (idx: number, sub: string, chip: string, text: string, blockCls: string, result: string) => page(
  chrome(idx-1) + slotLayer(idx-1) +
  `<div data-layer=head class=head><span class=t style="font-size:${nameSize(NAMES[idx-1]!)}px">${NAMES[idx-1]!}</span><span class=s>${sub}</span></div>
<div data-layer=prompt class="prompt tall"><span class=chip>@${chip}</span><span class=ptext id=pt>${text}</span><div class=send>↑</div></div>
<div data-layer=cover class=cover id=cv></div><div data-layer=cursor class=cursor id=cu></div>
${result}
<div data-layer=block class="block ${blockCls}"><div class=btop><span class=bn>${idx}</span><span class=bnm style="font-size:${blockSize(NAMES[idx-1]!)}px">${NAMES[idx-1]!}</span></div><div class=blogo><img src=${L[idx-1]!}></div></div>
<script>
document.fonts.ready.then(()=>{const t=document.getElementById('pt').getBoundingClientRect();const c=document.getElementById('cv');
c.style.left=(t.left-4)+'px';c.style.top=(t.top-6)+'px';c.style.width=(t.width+8)+'px';c.style.height=(t.height+12)+'px';
const u=document.getElementById('cu');u.style.left=(t.left-4)+'px';u.style.top=(t.top+t.height/2-25)+'px';});
</script>`);
const RT = 765, RS = 220;
const ucs: Array<[string, string, string[]]> = [['People search & profiles','107.5K',['pi-fullenrich.com.png','pi-blitz-api.ai.png','pi-enrichlayer.png']],['Email & phone finding','93.5K',['pi-anymailfinder.com.png','pi-quickenrich.io.png','apollo.io.png']],['Job postings & hiring','64.6K',['pi-www.workable.com.png','pi-www.greenhouse.com.png','pi-www.ashbyhq.com.png']]];
const fcRows = ucs.map((u,i)=>`<div data-layer=uc${i} class=uc style="top:${RT+i*RS}px"><div class=ucl><div class=uct>${u[0]}</div><div class=ucn>${u[1]} calls · last 24h</div></div><div class=ucp>${u[2].map(x=>`<img src=${x}>`).join('')}</div></div>`).join('');
const provIcons=['wikipedia.org','apollo.io','shopify.com','oriane.xyz','fiscal.ai','pi-fullenrich.com','benzinga.com','similarweb.com'];
const tile = (n: string, i: number) => `<div class=pwall style="left:${i*290}px;top:0"><img src=${n}.png></div>`;
const more = `<div class=pwall style="left:580px;top:0;background:#fa5d19;border-color:#fa5d19"><span class=more>&amp; more</span></div>`;
const wall = [0,1].map(r => `<div data-layer=wall${r} class=wrow style="top:${RT+r*RS}px">${provIcons.slice(r*3, r*3+3).map((n,i)=>tile(n,i)).join('')}</div>`).join('') + `<div data-layer=wall2 class=wrow style="top:${RT+2*RS}px">${provIcons.slice(6,8).map((n,i)=>tile(n,i)).join('')}${more}</div>`;
const hookRects: Rect[] | null = existsSync(resolve(DIR, 'rects-hook.json')) ? JSON.parse(readFileSync(resolve(DIR, 'rects-hook.json'), 'utf8')) as Rect[] : null;
const textRight = hookRects?.find(a => a[0] === 'plugins');
// A long noun ("marketing plugins") would push the bar past the safe zone's x 960: shrink the number and noun together.
const k = textRight ? Math.min(1, (960 - 33 - 146) / (92 + textRight[3])) : 1;
const fs = Math.round(102 * k), nounLeft = Math.round(146 + 92 * k), textTop = Math.round(690 + 65 * (1 - k));
const LSk = `letter-spacing:${Math.round(-4 * k * 10) / 10}px`;
const barW = textRight ? Math.round(nounLeft + textRight[3] * k + 33 - 120) : (cfg.barW || 520);
const TW = 132;
const hookTiles = [0,1,2,3,4].map(i=>`<div data-layer=t${i} style="position:absolute;left:${120+i*TW}px;top:${[960,1050,940,1030,980][i]!}px;width:${TW}px;height:190px;background:#f9f9f9"><div style="position:absolute;left:10px;top:14px;width:112px;height:112px;border-radius:28px;background:#111;box-shadow:0 14px 20px rgba(0,0,0,.30);display:flex;align-items:center;justify-content:center;color:#fff;font-size:74px;font-weight:500;line-height:1">?</div></div>`).join('');
const F = 120, LS = 'letter-spacing:-4px';
const hook = page(`${hookTiles}
<div data-layer=stop class=w style="left:136px;top:270px;font-size:${F}px;${LS}">Stop</div>
<div data-layer=using class=w style="left:422px;top:270px;font-size:${F}px;${LS}">using</div>
<img data-layer=hlogo src=${cfg.hookLogo} style="position:absolute;left:136px;top:426px;width:96px;height:96px;border-radius:${Math.round((cfg.hookRadius||30)*.8)}px;background:#f9f9f9">
<div data-layer=hname class=w style="left:250px;top:410px;font-size:${F}px;${LS}">${cfg.harness}</div>
<div data-layer=without class=w style="left:136px;top:550px;font-size:${F}px;${LS}">without</div>
<div data-layer=these class=w style="left:566px;top:550px;font-size:${F}px;${LS}">these</div>
<div data-layer=bar class=abs style="left:120px;top:679px;width:${barW}px;height:152px;background:#000;border-radius:27px"></div>
<div data-layer=three class=w style="left:146px;top:${textTop}px;font-size:${fs}px;${LSk};background:#000;color:#fff;padding-right:${Math.round(10 * k)}px;padding-bottom:${Math.round(29 * k)}px">${N}</div>
<div data-layer=plugins class=w style="left:${nounLeft}px;top:${textTop}px;font-size:${fs}px;${LSk};background:#000;color:#fff;padding:0 ${Math.round(10 * k)}px ${Math.round(29 * k)}px">${cfg.noun}.</div>`);
const epos = [[0,0],[440,0],[0,310],[440,310],[220,620]] as const;
const tiles = L.map((n,i)=>`<div class=etile style="left:${epos[i]![0]}px;top:${epos[i]![1]}px;width:400px;height:280px;border-radius:56px"><img src=${n} style="width:170px;height:170px"></div>`).join('');
const end = page(`<div data-layer=f1 class=head style="top:270px!important"><span class=t style="font-size:90px;letter-spacing:-3px;padding-bottom:24px">Follow for more</span></div>
<div data-layer=f2 class=head style="top:370px!important"><span class=t style="font-size:76px;letter-spacing:-3px;color:#fa5d19;padding-bottom:24px">plugin suggestions.</span></div>
<div data-layer=tiles class=abs style="left:120px;top:500px;width:840px;height:900px">${tiles}</div>`);
const frames: Record<string, string> = { hook };
items.forEach((it,i)=>{ frames['s'+(i+1)] = prod(i+1,it.sub,it.chip,it.prompt,it.bc,it.win||(fcRows+wall)); });
frames.end = end;
for (const [name, h] of Object.entries(frames)) writeFileSync(resolve(DIR, name + '.html'), h);
console.log('core: wrote', Object.keys(frames).length, 'pages, bar width', barW);
