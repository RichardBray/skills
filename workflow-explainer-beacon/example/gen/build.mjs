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

const TABS = ['SETUP', 'ASK', 'COUNT', 'FIND', 'PITCH'];
const tabs = (a) => `<div class=tabs>${TABS.map((t, i) => `<div class="tab ${a !== null && i < a ? 'done' : ''}">${a !== null && i < a ? t : '?'}</div>`).join('')}</div>`;
const L = (id, style, cls, inner) => `<div data-layer=${id} class="${cls}" style="${style}">${inner}</div>`;
const head = (id, n, word, top = 280) => L(id, `left:120px;top:${top}px;display:flex;align-items:flex-end;gap:30px`, 'abs', `<div class=num>${n}</div><div class=big style="font-size:100px;padding-bottom:14px;letter-spacing:-4px">${word}</div>`);

const promptCard = (hl) => `<div style="padding:28px 36px"><div style="display:flex;align-items:center;gap:16px;${hl ? 'visibility:hidden' : ''}"><img src=claude.svg style="width:44px"><b style="font:600 30px S">Claude</b></div><div style="font:500 44px S;letter-spacing:-1.2px;line-height:1.2;margin-top:20px;width:700px">Use the <span class=hi style="${hl ? `background:${ORANGE};color:#fff;` : ''}padding:0 10px;border-radius:8px">freshly funded hiring shortlist</span> skill. Find AI startups that just raised.</div></div><div style="position:absolute;right:28px;bottom:24px;width:64px;height:64px;border-radius:32px;background:${INK};color:#fff;font:600 36px S;display:flex;align-items:center;justify-content:center;${hl ? 'visibility:hidden' : ''}">↑</div>`;
const scenes = [];
const cos = [['Wabi', '$55M'], ['Dreamteam AI', '$53M'], ['Different Labs', '$48M'], ['Mount Thor', '$45M']];

scenes.push({ tab: null, layers: [
  { d: 0.15, html: L('a', 'left:120px;top:330px;width:840px;height:290px;transform:rotate(-1.5deg)', 'card', `<div style="display:flex;align-items:center;gap:40px;height:100%;padding:0 46px"><div style="width:150px;height:150px;border-radius:30px;background:#0a66c2;color:#fff;font:700 104px S;display:flex;align-items:center;justify-content:center;letter-spacing:-4px;padding-bottom:10px">in</div><div><div class=lab>Stop using</div><div class=big style="font-size:124px;position:relative;margin-top:8px">LinkedIn<i style="position:absolute;left:-12px;right:-12px;top:52%;height:16px;background:${RED};border-radius:8px;transform:rotate(-3deg)"></i></div></div></div>`) },
  { d: 2.8, html: L('b', 'left:120px;top:690px;width:840px;height:250px;transform:rotate(1deg)', 'card', `<div style="display:flex;align-items:center;gap:36px;height:100%;padding:0 44px"><div style="width:130px;height:130px;border-radius:28px;background:${ORANGE};display:flex;align-items:center;justify-content:center;flex:none"><img src=claude.svg style="width:84px;filter:brightness(0) invert(1)"></div><div class=big style="font-size:64px;letter-spacing:-2px;line-height:1.08">Claude finds it <span style="color:${ORANGE}">before it's posted.</span></div></div>`) },
  { d: 5.0, html: L('d', 'left:700px;top:640px;transform:rotate(-4deg)', 'stk', '5 STEPS') },
] });

scenes.push({ tab: 0, layers: [
  { d: 0.1, html: head('head', 1, 'SETUP', 270) },
  { d: 0.4, html: L('c1', 'left:120px;top:470px;width:840px;height:300px;transform:rotate(-.8deg)', 'card', `<div style="padding:28px 36px"><div class=lab>Add the Firecrawl plugin</div><div style="display:flex;align-items:center;gap:26px;margin-top:30px"><div style="width:120px;height:120px;border-radius:26px;background:${ORANGE};display:flex;align-items:center;justify-content:center;flex:none"><img src=logo-orange.svg style="width:74px;filter:brightness(0) invert(1)"></div><div style="flex:1"><div class=big style="font-size:50px;letter-spacing:-1px">Firecrawl</div><div style="font:500 24px M;color:#6b6556;margin-top:8px">Firecrawl Alexandria · plugin for Claude</div></div><div style="background:${INK};color:#fff;font:600 32px S;padding:16px 30px;border-radius:14px">Add</div></div></div>`) },
] });

scenes.push({ tab: 1, layers: [
  { d: 0.1, html: head('head', 2, 'ASK', 270) },
  { d: 0.3, html: L('b', 'left:120px;top:470px;width:840px;height:300px', 'card', promptCard(false)) },
  { d: 0.35, html: L('hl', 'left:120px;top:470px;width:840px;height:300px', 'card hlmode', promptCard(true)) },
  ...cos.map((c, i) => ({ d: 4.0 + i * 0.3, html: L('k' + i, `left:${120 + (i % 2) * 430}px;top:${800 + Math.floor(i / 2) * 200}px;width:410px;height:178px;transform:rotate(${[-1.2, 1, 1, -1][i]}deg)`, 'co', `<h3 style="font-size:46px">${c[0]}</h3><div class=amt style="font-size:48px;margin-top:10px">${c[1]}</div>`) })),
] });

scenes.push({ tab: 2, layers: [
  { d: 0.1, html: head('head', 3, 'COUNT', 270) },
  { d: 0.3, html: L('t', 'left:120px;top:470px;width:840px;height:340px', 'card', `${cos.map((c, i) => `<div style="position:absolute;left:0;right:0;top:${i * 85}px;height:85px;${i ? `border-top:3px solid ${INK};` : ''}display:flex;align-items:center;padding:0 34px;font:500 40px S;letter-spacing:-.5px"><div style="flex:1">${c[0]}</div><div style="width:190px;font:700 34px M;color:${ORANGE}">${c[1]}</div><div style="width:110px"></div></div>`).join('')}`) },
  ...cos.map((c, i) => ({ d: 1.0 + i * 0.3, html: L('z' + i, `left:826px;top:${486 + i * 85}px;width:92px;height:62px;transform:rotate(${[-3, 2, -2, 3][i]}deg)`, 'abs', `<div style="width:100%;height:100%;background:${RED};border:4px solid ${INK};border-radius:12px;color:#fff;font:700 42px S;display:flex;align-items:center;justify-content:center;box-shadow:4px 4px 0 ${INK}">0</div>`) })),
  { d: 2.9, html: L('g', 'left:120px;top:880px;width:660px;height:150px;transform:rotate(-1.2deg)', 'abs', `<div style="width:100%;height:100%;background:${GREEN};border:4px solid ${INK};border-radius:22px;box-shadow:8px 8px 0 ${INK};color:#fff;display:flex;align-items:center;justify-content:center"><div class=big style="font-size:96px;letter-spacing:-3px">YOUR GAP</div></div>`) },
] });

const people = [['Zed', 'Co-Founder', 'Z', ORANGE], ['Abhinav', 'Co-Founder & CTO', 'A', INK], ['Joonas', 'Founding Designer', 'J', GREEN]];
scenes.push({ tab: 3, layers: [
  { d: 0.1, html: head('head', 4, 'FIND', 270) },
  ...people.map((p, i) => ({ d: 1.7 + i * 0.5, html: L('h' + i, `left:${120 + i * 285}px;top:470px;width:270px;height:330px;transform:rotate(${[-1.5, 1, -1][i]}deg)`, 'card', `<div style="padding:30px 24px"><div style="width:120px;height:120px;border-radius:60px;background:${p[3]};color:#fff;font:600 62px S;display:flex;align-items:center;justify-content:center">${p[2]}</div><div class=big style="font-size:50px;margin-top:26px;letter-spacing:-1.5px">${p[0]}</div><div style="font:500 24px M;color:#6b6556;margin-top:12px;line-height:1.3">${p[1]}</div></div>`) })),
] });

const rank = [['1', 'Wabi', '$55M'], ['2', 'Dreamteam AI', '$53M'], ['3', 'Different Labs', '$48M']];
scenes.push({ tab: 4, layers: [
  { d: 0.1, html: head('head', 5, 'SHORTLIST', 270) },
  ...rank.map((r, i) => ({ d: 0.5 + i * 0.6, html: L('r' + i, `left:120px;top:${470 + i * 150}px;width:840px;height:126px;transform:rotate(${[-.6, .6, -.6][i]}deg)`, 'card', `<div style="display:flex;align-items:center;height:100%;padding:0 34px;gap:28px"><div class=big style="font-size:84px;color:${ORANGE};width:70px;letter-spacing:-3px">${r[0]}</div><div class=big style="flex:1;font-size:48px;letter-spacing:-1px">${r[1]}</div><div style="font:700 38px M;color:${ORANGE}">${r[2]}</div></div>`) })),
  { d: 2.85, html: L('s', 'left:120px;top:960px;transform:rotate(-3deg)', 'stk', 'FOLLOW FOR MORE') },
] });

const DY = [160, 120, 40, 220, 170, 280];
scenes.forEach((s, i) => { if (s.tab !== null) s.layers.unshift({ d: 0.1, fixed: true, html: L('tab', `left:${125 + s.tab * 166.4}px;top:170px;width:164px;height:58px;background:${ORANGE};color:#fff;border-radius:${s.tab === 0 ? '12px 4px 4px 12px' : s.tab === 4 ? '4px 12px 12px 4px' : '4px'};display:flex;align-items:center;justify-content:center;font:600 20px M;letter-spacing:1px`, 'abs', TABS[s.tab]) }); });
scenes.forEach((s, i) => s.layers.forEach((l) => { if (l.fixed) return; l.html = l.html.replace(/top:(\d+)px/, (m, v) => `top:${+v + DY[i]}px`); }));
const pageHtml = (s) => `<!doctype html><meta charset=utf-8><style>${css}</style><body><div id=bg>${tabs(s.tab)}</div>${s.layers.map((l) => l.html).join('')}`;
scenes.forEach((s, i) => writeFileSync(`s${i}.html`, pageHtml(s)));
writeFileSync('scenes.json', JSON.stringify(scenes.map((s, i) => ({ i, layers: s.layers.map((l) => ({ id: /data-layer=(\w+)/.exec(l.html)[1], d: l.d })) }))));
console.log('scenes', scenes.length);
