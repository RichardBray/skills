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

const TABS = ['SETUP', 'ASK', 'FORM', 'CARDS', 'CALL'];
const tabs = (a) => `<div class=tabs>${TABS.map((t, i) => `<div class="tab ${a !== null && i < a ? 'done' : ''}">${a !== null && i < a ? t : '?'}</div>`).join('')}</div>`;
const L = (id, style, cls, inner) => `<div data-layer=${id} class="${cls}" style="${style}">${inner}</div>`;
const head = (id, n, word, top = 280) => L(id, `left:120px;top:${top}px;display:flex;align-items:flex-end;gap:30px`, 'abs', `<div class=num>${n}</div><div class=big style="font-size:100px;padding-bottom:14px;letter-spacing:-4px">${word}</div>`);

const MUTED = '#6b6556';
const scenes = [];
const grokIcon = (s) => `<div style="width:${s}px;height:${s}px;border-radius:${s / 4}px;background:${INK};color:#fff;font:700 ${s * 0.6}px S;display:flex;align-items:center;justify-content:center;flex:none">G</div>`;
const prompt = (hl) => `<div style="padding:28px 36px"><div style="display:flex;align-items:center;gap:16px;${hl ? 'visibility:hidden' : ''}">${grokIcon(44)}<b style="font:600 30px S">Grok</b></div><div style="font:500 42px S;letter-spacing:-1.2px;line-height:1.25;margin-top:18px;width:720px">Use the <span class=hi style="${hl ? `background:${ORANGE};color:#fff;` : ''}padding:0 10px;border-radius:8px;-webkit-box-decoration-break:clone;box-decoration-break:clone">sports card buy-low screen</span> skill on Trevor Lawrence.</div></div><div style="position:absolute;right:28px;bottom:24px;width:64px;height:64px;border-radius:32px;background:${INK};color:#fff;font:600 36px S;display:flex;align-items:center;justify-content:center;${hl ? 'visibility:hidden' : ''}">↑</div>`;
const tradingCard = `<div style="width:150px;height:200px;border:4px solid ${INK};border-radius:14px;background:linear-gradient(160deg,#ff6fa8,#fa5d19);display:flex;flex-direction:column;justify-content:flex-end;padding:10px;flex:none;box-shadow:5px 5px 0 ${INK}"><div style="background:#fff;border:3px solid ${INK};border-radius:6px;font:700 15px M;text-align:center;padding:4px 0">ROOKIE</div></div>`;

scenes.push({ tab: null, layers: [
  { d: 0.15, html: L('a', 'left:120px;top:330px;width:840px;height:290px;transform:rotate(-1.5deg)', 'card', `<div style="display:flex;align-items:center;gap:40px;height:100%;padding:0 46px"><div style="width:150px;height:150px;border-radius:30px;background:linear-gradient(135deg,#ff6fa8,#fa5d19);color:#fff;font:700 100px S;display:flex;align-items:center;justify-content:center;padding-bottom:6px;flex:none">$</div><div><div class=lab>Stop buying cards</div><div class=big style="font-size:66px;position:relative;margin-top:10px;letter-spacing:-2.5px;white-space:nowrap">after the hype<i style="position:absolute;left:-12px;right:-12px;top:52%;height:14px;background:${RED};border-radius:7px;transform:rotate(-2deg)"></i></div></div></div>`) },
  { d: 2.35, html: L('b', 'left:120px;top:680px;width:840px;height:260px;transform:rotate(1deg)', 'card', `<div style="display:flex;align-items:center;gap:40px;height:100%;padding:0 44px">${tradingCard}<div><div class=big style="font-size:56px;letter-spacing:-1.6px;line-height:1.05">Trevor Lawrence</div><div style="font:500 26px M;color:${MUTED};margin-top:12px">2021 rookie card</div></div></div>`) },
  { d: 3.8, html: L('d', 'left:690px;top:640px;transform:rotate(-4deg)', 'stk', 'TOO EARLY?') },
] });

scenes.push({ tab: 0, layers: [
  { d: 0.1, html: head('head', 1, 'SETUP', 270) },
  { d: 0.4, html: L('c1', 'left:120px;top:470px;width:840px;height:300px;transform:rotate(-.8deg)', 'card', `<div style="padding:28px 36px"><div class=lab>Add the Firecrawl app</div><div style="display:flex;align-items:center;gap:26px;margin-top:30px"><div style="width:120px;height:120px;border-radius:26px;background:${ORANGE};display:flex;align-items:center;justify-content:center;flex:none"><img src=logo-orange.svg style="width:74px;filter:brightness(0) invert(1)"></div><div style="flex:1"><div class=big style="font-size:50px;letter-spacing:-1px">Firecrawl</div><div style="font:500 24px M;color:#6b6556;margin-top:8px">Firecrawl Alexandria · app for Grok</div></div><div style="background:${INK};color:#fff;font:600 32px S;padding:16px 30px;border-radius:14px">Add</div></div></div>`) },
] });

const sources = [['ESPN', 'Stats, injuries'], ['PSA', 'Price guide'], ['Steel City', 'Sealed boxes']];
scenes.push({ tab: 1, layers: [
  { d: 0.1, html: head('head', 2, 'ASK', 270) },
  { d: 0.3, html: L('b', 'left:120px;top:470px;width:840px;height:330px', 'card', prompt(false)) },
  { d: 0.35, html: L('hl', 'left:120px;top:470px;width:840px;height:330px', 'card hlmode', prompt(true)) },
  ...sources.map((c, i) => ({ d: 5.2 + i * 0.3, html: L('k' + i, `left:${120 + i * 285}px;top:830px;width:270px;height:148px;transform:rotate(${[-1.2, 1, -1][i]}deg)`, 'co', `<h3 style="font-size:36px;letter-spacing:-.8px;white-space:nowrap">${c[0]}</h3><div class=sub style="margin-top:12px;font-size:22px">${c[1]}</div>`) })),
] });

const rating = (hl) => `<div style="padding:28px 38px"><div class=lab style="${hl ? 'visibility:hidden' : ''}">Passer rating · 2026</div><div class=big style="font-size:110px;margin-top:14px"><span class=hi style="${hl ? `background:${GREEN};color:#fff;` : ''}padding:0 14px;border-radius:12px">112.8</span></div><div style="font:600 28px M;color:${MUTED};margin-top:14px;${hl ? 'visibility:hidden' : ''}">2025: 91.0</div></div>`;
scenes.push({ tab: 2, layers: [
  { d: 0.1, html: head('head', 3, 'FORM', 270) },
  { d: 0.4, html: L('r', 'left:120px;top:470px;width:840px;height:300px;transform:rotate(-.7deg)', 'card', rating(false)) },
  { d: 0.45, html: L('hl', 'left:120px;top:470px;width:840px;height:300px;transform:rotate(-.7deg)', 'card hlmode', rating(true)) },
  { d: 2.15, html: L('t', 'left:120px;top:800px;width:840px;height:170px;transform:rotate(.7deg)', 'card', `<div style="display:flex;align-items:center;justify-content:space-between;height:100%;padding:0 38px"><div><div class=big style="font-size:58px;letter-spacing:-1.6px">21 TD in 9 games</div><div style="font:600 24px M;color:${MUTED};margin-top:10px">2025: 29 TD in 17 games</div></div></div>`) },
  { d: 4.31, html: L('h', 'left:150px;top:1000px;transform:rotate(-2deg)', 'abs', `<div style="background:${GREEN};color:#fff;border:4px solid ${INK};border-radius:999px;box-shadow:6px 6px 0 ${INK};font:700 30px S;padding:12px 28px;white-space:nowrap">✓ ACTIVE · NO INJURY LISTED</div>`) },
] });

scenes.push({ tab: 3, layers: [
  { d: 0.1, html: head('head', 4, 'CARDS', 270) },
  { d: 0.4, html: L('c', 'left:120px;top:470px;width:840px;height:330px;transform:rotate(-.6deg)', 'card', `<div style="display:flex;gap:36px;padding:34px 38px">${tradingCard}<div><div class=lab>2021 Donruss Rated Rookie</div><div style="display:flex;gap:44px;margin-top:20px"><div><div style="font:600 22px M;color:${MUTED}">PSA 9</div><div class=big style="font-size:84px;color:${ORANGE};margin-top:6px">$60</div></div><div><div style="font:600 22px M;color:${MUTED}">PSA 10</div><div class=big style="font-size:84px;margin-top:6px">$175</div></div></div><div style="display:inline-block;margin-top:20px;background:#e8e2d4;border:3px solid ${INK};border-radius:999px;font:700 22px M;padding:6px 16px">GUIDE · NO CHANGE</div></div></div>`) },
  { d: 2.6, html: L('x', 'left:150px;top:840px;transform:rotate(-1.5deg)', 'abs', `<div style="background:#fff3c4;border:4px solid ${INK};border-radius:16px;box-shadow:6px 6px 0 ${INK};font:600 28px S;padding:14px 24px;white-space:nowrap">2021 hobby boxes: sold out</div>`) },
] });

const calls = [['BUY', 'Lawrence', '$60 PSA 9 · form way up', GREEN], ['HOLD', 'Burrow', 'Guide already marked up', '#9a927f'], ['AVOID', 'Herbert', '11 INT this season', RED]];
scenes.push({ tab: 4, layers: [
  { d: 0.1, html: head('head', 5, 'CALL', 270) },
  ...calls.map((c, i) => ({ d: [0.2, 1.41, 2.4][i], html: L('b' + i, `left:120px;top:${470 + i * 150}px;width:840px;height:130px;transform:rotate(${[-.6, .6, -.6][i]}deg)`, 'card', `<div style="display:flex;align-items:center;height:100%;padding:0 28px;gap:24px"><div style="width:150px;text-align:center;background:${c[3]};color:#fff;border:3px solid ${INK};border-radius:12px;font:700 30px S;padding:8px 0;flex:none">${c[0]}</div><div><div class=big style="font-size:44px;letter-spacing:-1.2px">${c[1]}</div><div style="font:500 22px M;color:${MUTED};margin-top:6px">${c[2]}</div></div></div>`) })),
  { d: 2.6, html: L('n', 'left:130px;top:940px', 'abs', `<div style="font:500 22px M;color:${MUTED}">Guide values, not sales. Not financial advice.</div>`) },
] });

const DY = [160, 120, 40, 120, 120, 180];
scenes.forEach((s, i) => { if (s.tab !== null) s.layers.unshift({ d: 0.1, fixed: true, html: L('tab', `left:${125 + s.tab * 166.4}px;top:170px;width:164px;height:58px;background:${ORANGE};color:#fff;border-radius:${s.tab === 0 ? '12px 4px 4px 12px' : s.tab === 4 ? '4px 12px 12px 4px' : '4px'};display:flex;align-items:center;justify-content:center;font:600 20px M;letter-spacing:1px`, 'abs', TABS[s.tab]) }); });
scenes.forEach((s, i) => s.layers.forEach((l) => { if (l.fixed) return; l.html = l.html.replace(/top:(\d+)px/, (m, v) => `top:${+v + DY[i]}px`); }));
const pageHtml = (s) => `<!doctype html><meta charset=utf-8><style>${css}</style><body><div id=bg>${tabs(s.tab)}</div>${s.layers.map((l) => l.html).join('')}`;
scenes.forEach((s, i) => writeFileSync(`s${i}.html`, pageHtml(s)));
writeFileSync('scenes.json', JSON.stringify(scenes.map((s, i) => ({ i, layers: s.layers.map((l) => ({ id: /data-layer=(\w+)/.exec(l.html)[1], d: l.d })) }))));
console.log('scenes', scenes.length);
