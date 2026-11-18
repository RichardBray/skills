import { writeFileSync } from 'node:fs';

const INK = '#141414', ORANGE = '#fa5d19', GREEN = '#1faa59', RED = '#e5382d', PAPER = '#efe9dd';
const css = `
.hlmode{background:transparent!important;border-color:transparent!important;box-shadow:none!important}.hlmode *{color:transparent!important}.hlmode .hi{color:#fff!important}
@font-face{font-family:S;src:url(SuisseIntl-400.woff2);font-weight:400}
@font-face{font-family:S;src:url(SuisseIntl-500.woff2);font-weight:500}
@font-face{font-family:M;src:url(GeistMono-Variable.woff2)}
*{box-sizing:border-box;margin:0}
body{width:1080px;height:1920px;font-family:S,sans-serif;color:${INK};position:relative;overflow:hidden;background:${PAPER}}
#bg{position:absolute;inset:0;background:${PAPER};background-image:radial-gradient(#cdc5b3 2.2px,transparent 2.7px);background-size:38px 38px}
.abs{position:absolute}
.tabs{position:absolute;left:120px;top:166px;width:840px;height:66px;display:flex;border:4px solid ${INK};border-radius:16px;background:#fff;box-shadow:6px 6px 0 ${INK};overflow:hidden;font:600 20px M;letter-spacing:1px}
.tab{flex:1;display:flex;align-items:center;justify-content:center;border-right:3px solid ${INK}}.tab:last-child{border:none}
.tab.on{background:${ORANGE};color:#fff}.tab.done{background:${INK};color:#fff}
.card{position:absolute;background:#fff;border:4px solid ${INK};border-radius:26px;box-shadow:10px 10px 0 ${INK};overflow:hidden}
.lab{font:600 22px M;letter-spacing:1.6px;text-transform:uppercase;color:#6b6556}
.big{font-weight:500;letter-spacing:-3px;line-height:1}
.stk{position:absolute;background:${ORANGE};color:#fff;border:4px solid ${INK};border-radius:14px;font:700 40px S;padding:12px 24px;box-shadow:7px 7px 0 ${INK};white-space:nowrap;letter-spacing:-.5px}
.pill{position:absolute;display:flex;align-items:center;gap:16px;background:#fff;border:4px solid ${INK};border-radius:999px;box-shadow:6px 6px 0 ${INK};padding:12px 28px 12px 16px;font:600 24px M;letter-spacing:.5px;white-space:nowrap}
.pill img{width:48px;height:48px;border-radius:12px}
.badge{position:absolute;display:flex;align-items:center;gap:22px;background:#fff;border:4px solid ${INK};border-radius:22px;box-shadow:8px 8px 0 ${INK};padding:0 26px}
.badge img{width:78px;height:78px;border-radius:18px;flex:none}
.badge b{font:600 30px S;display:block;letter-spacing:-.5px}.badge span{font:500 22px M;color:#6b6556;display:block;margin-top:6px}
.num{font-weight:500;font-size:210px;color:${ORANGE};letter-spacing:-9px;line-height:1}
.code{background:${INK};color:#fff;border-radius:16px;font:500 32px M;padding:24px 28px;white-space:nowrap}.code i{color:${ORANGE};font-style:normal}
.chip{display:inline-block;font:600 24px M;border:3px solid ${INK};border-radius:12px;padding:10px 16px;margin:0 12px 12px 0;background:#fff;box-shadow:4px 4px 0 ${INK}}
.co{position:absolute;background:#fff;border:4px solid ${INK};border-radius:22px;box-shadow:8px 8px 0 ${INK};padding:22px 26px}
.co h3{font:500 40px S;letter-spacing:-1px}.co .amt{font:700 32px M;color:${ORANGE};margin-top:8px}.co .sub{font:500 21px M;color:#6b6556;margin-top:10px;line-height:1.35}
`;

const TABS = ['SETUP', 'ASK', 'LISTING', 'VIN', 'OFFER'];
const tabs = (a) => `<div class=tabs>${TABS.map((t, i) => `<div class="tab ${a !== null && i < a ? 'done' : ''}">${a !== null && i < a ? t : '?'}</div>`).join('')}</div>`;
const L = (id, style, cls, inner) => `<div data-layer=${id} class="${cls}" style="${style}">${inner}</div>`;
const head = (id, n, word, top = 280) => L(id, `left:120px;top:${top}px;display:flex;align-items:flex-end;gap:30px`, 'abs', `<div class=num>${n}</div><div class=big style="font-size:100px;padding-bottom:14px;letter-spacing:-4px">${word}</div>`);

const MUTED = '#6b6556';
const scenes = [];
const car = (w) => `<svg width=${w} viewBox="0 0 320 170" fill="none" stroke="${INK}" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"><path d="M18 120 V92 Q18 78 34 74 L78 66 L112 30 Q118 24 128 24 H232 Q244 24 250 32 L282 68 Q302 72 304 90 V120 Z" fill="${ORANGE}"/><path d="M122 36 H178 V68 H92 Z" fill="#bfe3ff"/><path d="M190 36 H236 L262 68 H190 Z" fill="#bfe3ff"/><path d="M18 100 H304" stroke-width="5"/><path d="M200 84 h18" stroke-width="5"/><circle cx="84" cy="124" r="26" fill="${INK}"/><circle cx="84" cy="124" r="10" fill="#efe9dd" stroke="none"/><circle cx="244" cy="124" r="26" fill="${INK}"/><circle cx="244" cy="124" r="10" fill="#efe9dd" stroke="none"/><path d="M290 86 h12" stroke="#ffd34d" stroke-width="8"/></svg>`;
const ICON = (bg, ch, fg = '#fff') => `<div style="width:64px;height:64px;border-radius:16px;background:${bg};color:${fg};border:3px solid ${INK};font:700 34px S;display:flex;align-items:center;justify-content:center;flex:none">${ch}</div>`;

scenes.push({ tab: null, layers: [
  { d: 0.15, html: L('a', 'left:120px;top:330px;width:840px;height:290px;transform:rotate(-1.5deg)', 'card', `<div style="display:flex;align-items:center;gap:40px;height:100%;padding:0 46px"><div style="width:150px;height:150px;border-radius:30px;background:linear-gradient(135deg,#ff6fa8,#fa5d19);color:#fff;font:700 100px S;display:flex;align-items:center;justify-content:center;padding-bottom:6px;flex:none">$</div><div><div class=lab>Stop paying</div><div class=big style="font-size:66px;position:relative;margin-top:10px;letter-spacing:-2.5px;white-space:nowrap">the dealer's price<i style="position:absolute;left:-12px;right:-12px;top:52%;height:14px;background:${RED};border-radius:7px;transform:rotate(-2deg)"></i></div></div></div>`) },
  { d: 2.7, html: L('b', 'left:120px;top:690px;width:840px;height:250px;transform:rotate(1deg)', 'card', `<div style="display:flex;align-items:center;gap:36px;height:100%;padding:0 40px">${car(300)}<div><div class=big style="font-size:52px;letter-spacing:-1.5px;line-height:1.05">2021 RAV4</div><div style="font:500 24px M;color:${MUTED};margin-top:10px">XLE Premium · 75,195 mi</div><div style="font:700 44px M;color:${ORANGE};margin-top:12px">$22,150</div></div></div>`) },
  { d: 3.9, html: L('d', 'left:640px;top:640px;transform:rotate(-4deg)', 'stk', 'GREAT DEAL?') },
] });

scenes.push({ tab: 0, layers: [
  { d: 0.1, html: head('head', 1, 'SETUP', 270) },
  { d: 0.4, html: L('c1', 'left:120px;top:470px;width:840px;height:300px;transform:rotate(-.8deg)', 'card', `<div style="padding:28px 36px"><div class=lab>Add the Firecrawl plugin</div><div style="display:flex;align-items:center;gap:26px;margin-top:30px"><div style="width:120px;height:120px;border-radius:26px;background:${ORANGE};display:flex;align-items:center;justify-content:center;flex:none"><img src=logo-orange.svg style="width:74px;filter:brightness(0) invert(1)"></div><div style="flex:1"><div class=big style="font-size:50px;letter-spacing:-1px">Firecrawl</div><div style="font:500 24px M;color:#6b6556;margin-top:8px">Firecrawl Alexandria · plugin for Claude</div></div><div style="background:${INK};color:#fff;font:600 32px S;padding:16px 30px;border-radius:14px">Add</div></div></div>`) },
] });

const prompt = (hl) => `<div style="padding:28px 36px"><div style="display:flex;align-items:center;gap:16px;${hl ? 'visibility:hidden' : ''}"><img src=claude.svg style="width:44px"><b style="font:600 30px S">Claude</b></div><div style="font:500 42px S;letter-spacing:-1.2px;line-height:1.25;margin-top:18px;width:700px">Use the <span class=hi style="${hl ? `background:${ORANGE};color:#fff;` : ''}padding:0 10px;border-radius:8px;-webkit-box-decoration-break:clone;box-decoration-break:clone">used car fair price and hidden history</span> skill. 2021 RAV4 near Houston.</div></div><div style="position:absolute;right:28px;bottom:24px;width:64px;height:64px;border-radius:32px;background:${INK};color:#fff;font:600 36px S;display:flex;align-items:center;justify-content:center;${hl ? 'visibility:hidden' : ''}">↑</div>`;
const sources = [['CarGurus', 'Listing + market price'], ['NHTSA', 'Recalls'], ['bid.cars', 'Auction history'], ['Kelley Blue Book', 'Trade-in value']];
scenes.push({ tab: 1, layers: [
  { d: 0.1, html: head('head', 2, 'ASK', 270) },
  { d: 0.3, html: L('b', 'left:120px;top:470px;width:840px;height:330px', 'card', prompt(false)) },
  { d: 0.35, html: L('hl', 'left:120px;top:470px;width:840px;height:330px', 'card hlmode', prompt(true)) },
  ...sources.map((c, i) => ({ d: 3.2 + i * 0.35, html: L('k' + i, `left:${120 + (i % 2) * 430}px;top:${830 + Math.floor(i / 2) * 170}px;width:410px;height:148px;transform:rotate(${[-1.2, 1, 1, -1][i]}deg)`, 'co', `<h3 style="font-size:${c[0].length > 12 ? 33 : 38}px;letter-spacing:-.8px;white-space:nowrap">${c[0]}</h3><div class=sub style="margin-top:12px;font-size:23px">${c[1]}</div>`) })),
] });

const hist = (hl) => `<div style="display:flex;align-items:center;gap:28px;height:100%;padding:0 36px">${hl ? '<div style="width:64px;flex:none"></div>' : ICON(GREEN, '✓')}<div><div class=lab style="${hl ? 'visibility:hidden' : ''}">History report</div><div class=big style="font-size:64px;letter-spacing:-2px;margin-top:10px"><span class=hi style="${hl ? `background:${GREEN};color:#fff;` : ''}padding:0 12px;border-radius:10px">0 accidents</span></div></div></div>`;
scenes.push({ tab: 2, layers: [
  { d: 0.1, html: head('head', 3, 'LISTING', 270) },
  { d: 0.5, html: L('p0', 'left:120px;top:470px;width:840px;height:300px;transform:rotate(-.7deg)', 'card', `<div style="padding:30px 40px"><div class=lab>2021 RAV4 XLE Premium · Houston</div><div style="display:flex;gap:60px;margin-top:26px"><div><div style="font:500 24px M;color:${MUTED}">ASKING</div><div class=big style="font-size:92px;margin-top:8px;color:${ORANGE}">$22,150</div></div><div><div style="font:500 24px M;color:${MUTED}">MARKET</div><div class=big style="font-size:92px;margin-top:8px">$25,163</div></div></div></div>`) },
  { d: 1.9, html: L('g', 'left:610px;top:735px;transform:rotate(4deg)', 'abs', `<div style="background:${GREEN};color:#fff;border:4px solid ${INK};border-radius:999px;box-shadow:6px 6px 0 ${INK};font:700 34px S;padding:12px 28px;white-space:nowrap">GREAT DEAL</div>`) },
  { d: 3.0, html: L('h', 'left:120px;top:840px;width:840px;height:200px;transform:rotate(.6deg)', 'card', hist(false)) },
  { d: 3.05, html: L('hl', 'left:120px;top:840px;width:840px;height:200px;transform:rotate(.6deg)', 'card hlmode', hist(true)) },
] });

scenes.push({ tab: 3, layers: [
  { d: 0.1, html: head('head', 4, 'VIN', 270) },
  { d: 0.5, html: L('a', 'left:120px;top:470px;width:840px;height:300px;transform:rotate(-.7deg)', 'card', `<div style="padding:30px 40px"><div class=lab>Auction record · by VIN</div><div class=big style="font-size:66px;letter-spacing:-2px;margin-top:16px">Insurance auction</div><div style="margin-top:28px"><span class=chip>16 JUL 2026</span><span class=chip style="background:${RED};color:#fff">COLLISION</span><span class=chip>DAMAGE: ROOF</span></div></div>`) },
  { d: 2.4, html: L('o', 'left:120px;top:800px;width:410px;height:190px;transform:rotate(-1deg)', 'co', `<div class=lab style="font-size:20px">Odometer</div><div style="font:700 30px M;margin-top:16px;line-height:1.4">75,188 mi<br><span style="color:${MUTED}">→</span> 75,195 mi</div>`) },
  { d: 3.4, html: L('r', 'left:550px;top:800px;width:410px;height:190px;transform:rotate(1deg)', 'co', `<div class=lab style="font-size:20px">Repair estimate</div><div class=big style="font-size:76px;color:${RED};margin-top:16px">$15,315</div>`) },
  { d: 4.5, html: L('c', 'left:120px;top:1020px;width:840px;transform:rotate(-.5deg)', 'abs', `<div style="display:flex;align-items:center;gap:20px;background:#fff3c4;border:4px solid ${INK};border-radius:18px;box-shadow:6px 6px 0 ${INK};padding:18px 24px">${ICON('#ffd34d', '!', INK)}<div style="font:600 30px S;letter-spacing:-.4px">Airbag recall on this model: check it's fixed</div></div>`) },
] });

scenes.push({ tab: 4, layers: [
  { d: 0.1, html: head('head', 5, 'OFFER', 270) },
  { d: 0.5, html: L('k', 'left:120px;top:470px;width:840px;height:190px;transform:rotate(-.6deg)', 'card', `<div style="display:flex;align-items:center;justify-content:space-between;height:100%;padding:0 40px"><div><div class=lab>Kelley Blue Book</div><div class=big style="font-size:44px;letter-spacing:-1.2px;margin-top:12px">Trade-in value</div></div><div class=big style="font-size:84px;color:${ORANGE}">$21,490</div></div>`) },
  { d: 1.2, html: L('m', 'left:120px;top:690px;width:840px;height:190px;transform:rotate(.6deg)', 'card', `<div style="display:flex;align-items:center;justify-content:space-between;height:100%;padding:0 40px"><div><div class=lab>Similar listings</div><div class=big style="font-size:44px;letter-spacing:-1.2px;margin-top:12px">2021 XLE Premium</div></div><div class=big style="font-size:84px">~$23.5k</div></div>`) },
  { d: 3.1, html: L('s', 'left:150px;top:930px;transform:rotate(-3deg)', 'stk', 'OFFER ≤ $21.5K OR WALK') },
] });

const DY = [160, 120, 40, 120, 120, 180];
scenes.forEach((s, i) => { if (s.tab !== null) s.layers.unshift({ d: 0.1, fixed: true, html: L('tab', `left:${125 + s.tab * 166.4}px;top:170px;width:164px;height:58px;background:${ORANGE};color:#fff;border-radius:${s.tab === 0 ? '12px 4px 4px 12px' : s.tab === 4 ? '4px 12px 12px 4px' : '4px'};display:flex;align-items:center;justify-content:center;font:600 20px M;letter-spacing:1px`, 'abs', TABS[s.tab]) }); });
scenes.forEach((s, i) => s.layers.forEach((l) => { if (l.fixed) return; l.html = l.html.replace(/top:(\d+)px/, (m, v) => `top:${+v + DY[i]}px`); }));
const pageHtml = (s) => `<!doctype html><meta charset=utf-8><style>${css}</style><body><div id=bg>${tabs(s.tab)}</div>${s.layers.map((l) => l.html).join('')}`;
scenes.forEach((s, i) => writeFileSync(`s${i}.html`, pageHtml(s)));
writeFileSync('scenes.json', JSON.stringify(scenes.map((s, i) => ({ i, layers: s.layers.map((l) => ({ id: /data-layer=(\w+)/.exec(l.html)[1], d: l.d })) }))));
console.log('scenes', scenes.length);
