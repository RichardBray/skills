"""Writes the trades paper-cutout panels into compositions/ (split plates 1080x960, full plates 1080x1920)."""
ROOT = "/Users/robray/fc/firecrawl-transition/compositions"

BASE_CSS = """
      @font-face {{ font-family: "Suisse Intl"; src: url("assets/SuisseIntl-Regular.otf") format("opentype"); }}
      @font-face {{ font-family: "Suisse Intl Medium"; src: url("assets/SuisseIntl-Medium.otf") format("opentype"); }}
      [data-composition-id="{cid}"] {{ position: relative; width: 1080px; height: {h}px; overflow: hidden;
        font-family: "Suisse Intl", system-ui, sans-serif; color: #1c1815; background: #0a0908; }}
      [data-composition-id="{cid}"] * {{ box-sizing: border-box; }}
      .{p}-ground {{ position: absolute; inset: 0; background: #0a0908; }}
      .{p}-glow {{ position: absolute; inset: 0; background: radial-gradient(76% 60% at 50% 46%, rgba(250,93,25,0.16), rgba(250,93,25,0.03) 54%, transparent 76%); }}
      .{p}-fibre {{ position: absolute; inset: -80px; opacity: 0.30; mix-blend-mode: screen;
        background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='260' height='260'><filter id='f'><feTurbulence type='fractalNoise' baseFrequency='0.62' numOctaves='4' seed='7'/><feColorMatrix type='saturate' values='0'/></filter><rect width='260' height='260' filter='url(%23f)' opacity='0.5'/></svg>"); }}
      .{p}-torn {{ position: absolute; inset: 0; background: #f2ece0; filter: url(#{p}-tear); }}
      .{p}-torn.soft {{ filter: url(#{p}-tear-soft); }}
      .{p}-torn.deep {{ background: #cdbfa6; }}
      .{p}-torn.fire {{ background: #fa5d19; }}
      .{p}-torn.ink {{ background: #1c1815; }}
      #{p}-world {{ position: absolute; inset: 0; transform-origin: 0 0; }}
      .{p}-card {{ position: absolute; opacity: 0; }}
      .{p}-ico {{ position: absolute; left: 50%; background: #1c1815; -webkit-mask: no-repeat center/contain var(--i); mask: no-repeat center/contain var(--i); }}
      .{p}-logo {{ position: absolute; left: 50%; object-fit: contain; }}
      .{p}-title {{ position: absolute; left: 0; right: 0; text-align: center; font-family: "Suisse Intl Medium"; font-size: 42px; letter-spacing: -0.01em; white-space: nowrap; }}
      .{p}-chip {{ position: absolute; display: flex; align-items: center; justify-content: center; padding: 0 18px; height: 64px; opacity: 0; }}
      .{p}-lbl {{ position: relative; font-family: "Suisse Intl Medium"; font-size: 29px; letter-spacing: 0.14em; text-transform: uppercase; color: #fff6ef; white-space: nowrap; }}
      .{p}-chip.dark .{p}-lbl {{ color: #f2ece0; }}
"""

DEFS = """    <svg width="0" height="0" style="position:absolute" aria-hidden="true">
      <defs>
        <filter id="{p}-tear" x="-14%" y="-14%" width="128%" height="128%">
          <feTurbulence type="fractalNoise" baseFrequency="0.016 0.04" numOctaves="4" seed="11" result="n" />
          <feDisplacementMap in="SourceGraphic" in2="n" scale="17" xChannelSelector="R" yChannelSelector="G" />
        </filter>
        <filter id="{p}-tear-soft" x="-18%" y="-18%" width="136%" height="136%">
          <feTurbulence type="fractalNoise" baseFrequency="0.03 0.07" numOctaves="3" seed="4" result="n" />
          <feDisplacementMap in="SourceGraphic" in2="n" scale="9" xChannelSelector="R" yChannelSelector="G" />
        </filter>
        <filter id="{p}-mblur" x="-20%" y="-20%" width="140%" height="140%" color-interpolation-filters="sRGB"><feGaussianBlur id="{p}-mb" stdDeviation="0 0" /></filter>
      </defs>
    </svg>
    <div class="{p}-ground"></div>
    <div class="{p}-glow"></div>
    <div class="{p}-fibre"></div>
"""

JS_HEAD = """      (function () {{
        window.__timelines = window.__timelines || {{}};
        const tl = gsap.timeline({{ paused: true }});
        const R = '[data-composition-id="{cid}"] ';
        const q = (s) => s.split(",").map((x) => R + x.trim()).join(", ");
        function show(sel, t) {{ tl.set(q(sel), {{ opacity: 1 }}, t); }}
        function card(sel, t) {{
          show(sel, t);
          tl.fromTo(q(sel + " > .{p}-torn"), {{ opacity: 0, y: 60, rotation: -2 }}, {{ opacity: 1, y: 0, rotation: 0, duration: 0.42, ease: "back.out(1.5)" }}, t);
          tl.fromTo(q(sel + " .{p}-ico, " + sel + " .{p}-logo"), {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.42, ease: "back.out(1.8)" }}, t + 0.08);
          tl.fromTo(q(sel + " .{p}-title"), {{ opacity: 0, y: 24 }}, {{ opacity: 1, y: 0, duration: 0.36, ease: "expo.out" }}, t + 0.14);
        }}
        function pop(sel, t) {{
          show(sel, t);
          tl.fromTo(q(sel), {{ scale: 0.5, y: 16 }}, {{ scale: 1, y: 0, duration: 0.36, ease: "back.out(2)" }}, t);
        }}
        function punch(sel, t, s) {{
          tl.to(q(sel), {{ scale: s || 1.15, duration: 0.16, ease: "power2.out" }}, t);
          tl.to(q(sel), {{ scale: 1, duration: 0.5, ease: "elastic.out(1, 0.45)" }}, t + 0.16);
        }}
        const VX = 540, VY = {vy};
        const camState = {{ x: VX - {cx0} * {s0}, y: VY - {cy0} * {s0}, S: {s0} }};
        const mbProxy = {{ k: 0 }};
        tl.set(q("#{p}-world"), {{ scale: camState.S, x: camState.x, y: camState.y }}, 0);
        function cam(cx, cy, S, t) {{
          const nx = VX - cx * S, ny = VY - cy * S;
          const bx = Math.min(14, Math.abs(nx - camState.x) * 0.02 + Math.abs(S - camState.S) * 6);
          const by = Math.min(14, Math.abs(ny - camState.y) * 0.02 + Math.abs(S - camState.S) * 6);
          Object.assign(camState, {{ x: nx, y: ny, S }});
          tl.to(q("#{p}-world"), {{ scale: S, x: nx, y: ny, duration: 0.6, ease: "expo.inOut" }}, t);
          const apply = () => {{ const el = document.querySelector(R + "#{p}-mb") || document.getElementById("{p}-mb"); if (el) el.setAttribute("stdDeviation", (bx * mbProxy.k).toFixed(2) + " " + (by * mbProxy.k).toFixed(2)); }};
          tl.set(q("#{p}-world"), {{ filter: "url(#{p}-mblur)" }}, t);
          tl.fromTo(mbProxy, {{ k: 0 }}, {{ k: 1, duration: 0.3, ease: "sine.in", onUpdate: apply, immediateRender: false }}, t);
          tl.to(mbProxy, {{ k: 0, duration: 0.3, ease: "sine.out", onUpdate: apply }}, t + 0.3);
          tl.set(q("#{p}-world"), {{ filter: "none" }}, t + 0.61);
        }}
"""


def write(name, p, world, css, js, cam0, h=960, vy=380, outside=""):
    cid = name
    cx0, cy0, s0 = cam0
    html = (f'<template id="{cid}-template">\n  <div data-composition-id="{cid}" data-width="1080" data-height="{h}">\n'
            + DEFS.format(p=p)
            + f'    <div id="{p}-world">\n{world}\n    </div>\n{outside}\n    <style>\n'
            + BASE_CSS.format(cid=cid, p=p, h=h) + css
            + '\n    </style>\n    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>\n    <script>\n'
            + JS_HEAD.format(cid=cid, p=p, cx0=cx0, cy0=cy0, s0=s0, vy=vy) + js
            + f'\n        window.__timelines["{cid}"] = tl;\n      }})();\n    </script>\n  </div>\n</template>\n')
    open(f"{ROOT}/{name}.html", "w").write(html)


def L(name):
    return f"assets/icons/lucide-{name}.svg"


def card(p, cid, x, y, w, h, icon=None, title=None, tone="", isz=110, itop=None, ttop=None, extra="", ifill=None):
    itop = itop if itop is not None else (h - isz) // 2 - (34 if title else 0)
    ttop = ttop if ttop is not None else itop + isz + 22
    ic = (f'<div class="{p}-ico" style="--i:url(\'{icon}\');top:{itop}px;width:{isz}px;height:{isz}px;margin-left:-{isz // 2}px'
          + (f';background:{ifill}' if ifill else "") + '"></div>') if icon else ""
    tt = f'<div class="{p}-title" style="top:{ttop}px">{title}</div>' if title else ""
    return (f'      <div class="{p}-card" id="{p}-{cid}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px">'
            f'<div class="{p}-torn {tone}"></div>{ic}{tt}{extra}</div>')


def chip(p, cid, x, y, w, label, tone="fire", icon=None):
    txt = "" if tone == "fire" else ' style="color:#1c1815"'
    ic = f'<div class="{p}-cico" style="--i:url(\'{icon}\')"></div>' if icon else ""
    return (f'      <div class="{p}-chip" id="{p}-{cid}" style="left:{x}px;top:{y}px;width:{w}px;gap:12px">'
            f'<div class="{p}-torn soft {tone}"></div>{ic}<div class="{p}-lbl"{txt}>{label}</div></div>')


def chip_css(p):
    return (f"      .{p}-cico {{ position: relative; width: 34px; height: 34px; background: #1c1815; -webkit-mask: no-repeat center/contain var(--i); mask: no-repeat center/contain var(--i); }}\n"
            f"      .{p}-chip.big {{ height: 84px; }} .{p}-chip.big .{p}-lbl {{ font-size: 38px; }}\n")


FLAME = "assets/firecrawl-flame-knockout.svg"

# --- A (abs 4.41-6.57, split): "so it makes better trades while you sleep"
p = "ts"
BARS = [(0, 130, 1), (1, 90, 0), (2, 170, 1), (3, 140, 0), (4, 220, 1), (5, 260, 1)]
bars = "".join(f'<div class="{p}-bar" id="{p}-b{i}" style="left:{40 + i * 52}px;height:{h}px;top:{330 - h}px"><div class="{p}-torn soft {"fire" if up else "deep"}"></div></div>' for i, h, up in BARS)
world = "\n".join([
    card(p, "chart", 120, 150, 420, 420, title="Trades", ttop=350, extra=bars),
    card(p, "moon", 600, 190, 340, 340, icon=L("moon"), title="Overnight", tone="", isz=120),
    chip(p, "buy", 230, 610, 200, "buy", "fire", L("trending-up")),
    chip(p, "zz", 690, 80, 160, "zzz", "cream" if False else "", None),
])
css = chip_css(p) + f"""      .{p}-bar {{ position: absolute; width: 36px; transform-origin: center bottom; opacity: 0; }}
      #{p}-moon .{p}-ico {{ background: #1c1815; }}"""
js = f"""        card("#{p}-chart", 0.03);
""" + "\n".join(f"""        show("#{p}-b{i}", {0.2 + i * 0.09:.2f});
        tl.fromTo(q("#{p}-b{i}"), {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.3, ease: "back.out(1.6)" }}, {0.2 + i * 0.09:.2f});""" for i in range(6)) + f"""
        // "better trades" (abs 4.98-5.42)
        pop("#{p}-buy", 0.98);
        punch("#{p}-chart", 1.0, 1.08);
        // "while you sleep" (abs 5.74-6.24)
        cam(540, 380, 1.0, 0.75);
        card("#{p}-moon", 1.3);
        pop("#{p}-zz", 1.8);
        tl.fromTo(q("#{p}-moon .{p}-ico"), {{ rotation: -30 }}, {{ rotation: 0, duration: 0.6, ease: "back.out(2)" }}, 1.36);
        tl.to(q("#{p}-chart"), {{ opacity: 0.55, duration: 0.3 }}, 1.6);"""
write("trades-sleep-panel", p, world, css, js, cam0=(330, 380, 1.3))

# --- B (abs 10.85-13.27, full): "Giving Claude data it wouldn't normally have access to"
p = "ta"
lockdisc = (f'<div class="{p}-lock" id="{p}-lock"><div class="{p}-torn soft ink"></div>'
            f'<div class="{p}-ico" id="{p}-lk" style="--i:url(\'{L("lock")}\');top:22px;width:56px;height:56px;margin-left:-28px;background:#f2ece0"></div>'
            f'<div class="{p}-ico" id="{p}-lo" style="--i:url(\'{L("lock-open")}\');top:22px;width:56px;height:56px;margin-left:-28px;background:#f2ece0;opacity:0"></div></div>')
world = "\n".join([
    card(p, "claude", 90, 380, 330, 320, icon="assets/icons/claude.svg", title="Claude", isz=130, ifill="#d97757"),
    card(p, "data", 660, 380, 330, 320, icon=L("database"), title="Data", tone="deep", isz=120, extra=lockdisc),
    f'      <div id="{p}-wire"><div class="{p}-torn soft deep"></div><div class="{p}-torn soft fire" id="{p}-wfire"></div></div>',
    f'      <div id="{p}-flame"><img src="{FLAME}" alt=""></div>',
])
outside = "\n".join([
    chip(p, "no", 380, 1300, 320, "no access", ""),
    chip(p, "yes", 330, 1300, 420, "full access", "fire", FLAME),
])
css = chip_css(p) + f"""      .{p}-lock {{ position: absolute; right: -30px; top: -30px; width: 100px; height: 100px; }}
      .{p}-lock .{p}-torn {{ border-radius: 50%; }}
      #{p}-wire {{ position: absolute; left: 430px; top: 534px; width: 220px; height: 14px; transform-origin: left center; opacity: 0; }}
      #{p}-wfire {{ transform-origin: right center; transform: scaleX(0); }}
      #{p}-flame {{ position: absolute; left: 500px; top: 470px; width: 80px; height: 80px; opacity: 0; }}
      #{p}-flame img {{ width: 100%; height: 100%; object-fit: contain; }}
      #{p}-yes .{p}-cico {{ display: none; }}"""
js = f"""        card("#{p}-claude", 0.03);
        // "data" (abs 11.36)
        card("#{p}-data", 0.45);
        cam(540, 540, 1.0, 0.4);
        show("#{p}-wire", 0.7);
        tl.fromTo(q("#{p}-wire"), {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.3, ease: "power3.out" }}, 0.7);
        // "wouldn't normally" (abs 11.98)
        pop("#{p}-no", 1.1);
        punch("#{p}-lock", 1.15, 1.25);
        // "access" (abs 12.60): lock opens, the wire lights up
        tl.to(q("#{p}-lk"), {{ opacity: 0, duration: 0.08 }}, 1.72);
        tl.set(q("#{p}-lo"), {{ opacity: 1 }}, 1.74);
        punch("#{p}-lock", 1.74, 1.3);
        tl.to(q("#{p}-wfire"), {{ scaleX: 1, duration: 0.3, ease: "power3.out" }}, 1.74);
        show("#{p}-flame", 1.84);
        tl.fromTo(q("#{p}-flame"), {{ scale: 0, y: 20 }}, {{ scale: 1, y: 0, duration: 0.36, ease: "back.out(2.2)" }}, 1.84);
        tl.to(q("#{p}-no"), {{ opacity: 0, duration: 0.1 }}, 1.72);
        pop("#{p}-yes", 1.76);
        punch("#{p}-claude", 2.0, 1.08);"""
write("trades-access-panel", p, world, css, js, cam0=(255, 540, 1.35), h=1920, vy=540, outside=outside)

# --- C (abs 13.25-16.23, split): "like which CEOs recently sold their own stock"
p = "tc"
shares = "\n".join(card(p, f"s{i}", 470 + i * 26, 230 + i * 26, 200, 240, icon=L("chart-candlestick"), isz=90, tone="deep" if i < 2 else "") for i in range(3))
world = "\n".join([
    card(p, "ceo", 90, 190, 320, 380, icon=L("user"), title="CEO", isz=150, extra=f'<div class="{p}-tie"><div class="{p}-torn soft fire"></div></div>'),
    shares,
    card(p, "down", 640, 220, 330, 340, icon=L("trending-down"), title="Stock", isz=150, ifill="#fa5d19"),
    chip(p, "sold", 690, 120, 230, "sold", "fire"),
    chip(p, "own", 650, 600, 310, "own stock", ""),
])
css = chip_css(p) + f"""      .{p}-tie {{ position: absolute; left: 50%; margin-left: -14px; top: 210px; width: 28px; height: 46px; clip-path: polygon(50% 0, 100% 30%, 50% 100%, 0 30%); }}"""
js = f"""        card("#{p}-ceo", 0.03);
        // "CEOs" (abs 13.90)
        punch("#{p}-ceo", 0.62, 1.1);
""" + "\n".join(f'        card("#{p}-s{i}", {0.75 + i * 0.12:.2f});' for i in range(3)) + f"""
        cam(540, 380, 1.0, 0.6);
        // "sold" (abs 15.12): shares slide off, the price drops
""" + "\n".join(f'        tl.to(q("#{p}-s{i}"), {{ x: 520, opacity: 0, duration: 0.45, ease: "power3.in" }}, {1.72 + (2 - i) * 0.06:.2f});' for i in range(3)) + f"""
        pop("#{p}-sold", 1.85);
        card("#{p}-down", 2.0);
        // "own stock" (abs 15.64-16.08)
        pop("#{p}-own", 2.38);
        punch("#{p}-down", 2.8, 1.12);"""
write("trades-ceo-panel", p, world, css, js, cam0=(250, 380, 1.4))

# --- D (abs 16.21-18.23, full): "who's placing huge options bets"
p = "to"
coins = "\n".join(f'      <div class="{p}-coin" id="{p}-c{i}" style="left:{730}px;top:{620 - i * 46}px"><div class="{p}-torn soft fire"></div></div>' for i in range(7))
world = "\n".join([
    card(p, "bet", 170, 360, 420, 340, icon=L("coins"), title="Options", isz=140),
    coins,
])
outside = "\n".join([
    chip(p, "calls", 250, 1300, 260, "calls", "fire", L("trending-up")),
    chip(p, "puts", 570, 1300, 260, "puts", "", L("trending-down")),
    chip(p, "huge", 380, 1410, 320, "huge bet", ""),
])
css = chip_css(p) + f"""      .{p}-coin {{ position: absolute; width: 190px; height: 64px; opacity: 0; }}
      .{p}-coin .{p}-torn {{ border-radius: 50%; box-shadow: 0 6px 0 #8a3a12; }}
      #{p}-calls .{p}-cico {{ background: #fff6ef; }}"""
js = f"""        card("#{p}-bet", 0.03);
        // "huge" (abs 16.88): a coin tower stacks up
        cam(540, 520, 1.0, 0.45);
""" + "\n".join(f"""        show("#{p}-c{i}", {0.6 + i * 0.07:.2f});
        tl.fromTo(q("#{p}-c{i}"), {{ y: -260 }}, {{ y: 0, duration: 0.28, ease: "bounce.out" }}, {0.6 + i * 0.07:.2f});""" for i in range(7)) + f"""
        pop("#{p}-huge", 0.72);
        // "options" (abs 17.34)
        pop("#{p}-calls", 1.12);
        pop("#{p}-puts", 1.24);
        punch("#{p}-bet", 1.15, 1.12);
        // "bets" (abs 18.06)
        punch("#{p}-calls", 1.84, 1.18);"""
write("trades-options-panel", p, world, css, js, cam0=(380, 530, 1.3), h=1920, vy=540, outside=outside)

# --- E (abs 18.21-21.03, split): "and what management actually said on the last earning call"
p = "te"
lines = "".join(f'<div class="{p}-ln" id="{p}-l{i}" style="top:{110 + i * 52}px;width:{w}px"><div class="{p}-torn soft {"fire" if i == 1 else "deep"}"></div></div>' for i, w in enumerate([330, 380, 260, 310]))
waves = "\n".join(f'      <div class="{p}-wv" id="{p}-w{i}" style="left:{140 + i * 44}px"><div class="{p}-torn soft fire"></div></div>' for i in range(18))
world = "\n".join([
    card(p, "exec", 90, 130, 300, 360, icon=L("user"), title="Management", isz=140),
    card(p, "quote", 440, 130, 520, 360, extra=f'<div class="{p}-qm">“</div>{lines}'),
    waves,
    chip(p, "call", 330, 640, 420, "earnings call", "fire", L("phone")),
])
css = chip_css(p) + f"""      .{p}-ln {{ position: absolute; left: 110px; height: 22px; transform-origin: left center; opacity: 0; }}
      .{p}-qm {{ position: absolute; left: 30px; top: 0; font-family: Georgia, serif; font-size: 160px; line-height: 1; color: #fa5d19; }}
      .{p}-wv {{ position: absolute; top: 540px; width: 22px; height: 80px; transform-origin: center center; opacity: 0; }}
      #{p}-call .{p}-cico {{ background: #fff6ef; }}
      #{p}-exec .{p}-title {{ font-size: 36px; }}"""
amps = [0.3, 0.7, 0.45, 1.0, 0.6, 0.85, 0.35, 0.9, 0.55, 0.75, 0.4, 1.0, 0.5, 0.8, 0.3, 0.65, 0.95, 0.4]
js = f"""        card("#{p}-exec", 0.03);
        // "management" (abs 18.82)
        punch("#{p}-exec", 0.6, 1.1);
        // "actually said" (abs 19.10-19.66)
        cam(525, 380, 1.0, 0.75);
        card("#{p}-quote", 1.05);
""" + "\n".join(f"""        show("#{p}-l{i}", {1.3 + i * 0.12:.2f});
        tl.fromTo(q("#{p}-l{i}"), {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.25, ease: "power2.out" }}, {1.3 + i * 0.12:.2f});""" for i in range(4)) + f"""
        // "last earning call" (abs 20.20-20.80): the call audio plays
""" + "\n".join(f"""        show("#{p}-w{i}", {1.9 + i * 0.02:.2f});
        tl.fromTo(q("#{p}-w{i}"), {{ scaleY: 0.1 }}, {{ scaleY: {amps[i]}, duration: 0.2, ease: "power2.out" }}, {1.9 + i * 0.02:.2f});
        tl.to(q("#{p}-w{i}"), {{ scaleY: {amps[(i + 7) % 18]}, duration: 0.18, ease: "sine.inOut", repeat: 2, yoyo: true }}, {2.12 + i * 0.02:.2f});""" for i in range(18)) + f"""
        pop("#{p}-call", 2.3);
        punch("#{p}-call", 2.6, 1.15);"""
write("trades-call-panel", p, world, css, js, cam0=(240, 330, 1.4))

# --- F (abs 21.01-23.67, split, black plate): "So before I buy any stock, like Nvidia, I can say"
p = "tn"
tiles = "\n".join(card(p, f"k{i}", 110 + i * 300, 210, 260, 280, icon=L(ic), isz=110, tone="deep") for i, ic in enumerate(["chart-line", "chart-candlestick", "trending-up"]))
world = "\n".join([
    tiles,
    card(p, "nv", 300, 160, 480, 400, icon="assets/icons/nvidia.svg", title="Nvidia", isz=170, ifill="#76b900"),
    chip(p, "buy", 400, 610, 280, "buy?", "fire"),
])
css = chip_css(p) + f"""      #{p}-nv .{p}-title {{ font-size: 52px; }}"""
js = "\n".join(f'        card("#{p}-k{i}", {0.15 + i * 0.1:.2f});' for i in range(3)) + f"""
        // "buy any stock" (abs 21.70-22.12)
        pop("#{p}-buy", 0.68);
        // "Nvidia" (abs 22.58)
        tl.to(q("#{p}-k0, #{p}-k1, #{p}-k2"), {{ opacity: 0.2, scale: 0.9, duration: 0.3 }}, 1.5);
        card("#{p}-nv", 1.52);
        cam(540, 380, 1.15, 1.6);
        punch("#{p}-buy", 2.1, 1.18);"""
write("trades-nvidia-panel", p, world, css, js, cam0=(540, 380, 1.0))
print("ok")
