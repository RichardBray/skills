"""Writes the coffee-shop-location paper-cutout panels (1080x960, top half) into compositions/."""
ROOT = "/Users/robray/fc/firecrawl-transition/compositions"

BASE_CSS = """
      @font-face {{ font-family: "Suisse Intl"; src: url("assets/SuisseIntl-Regular.otf") format("opentype"); }}
      @font-face {{ font-family: "Suisse Intl Medium"; src: url("assets/SuisseIntl-Medium.otf") format("opentype"); }}
      [data-composition-id="{cid}"] {{ position: relative; width: 1080px; height: 960px; overflow: hidden;
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
        const VX = 540, VY = 400;
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


def write(name, p, meta, world, css, js, cam0=(540, 400, 1.0)):
    cid = name
    cx0, cy0, s0 = cam0
    html = (f'<template id="{cid}-template">\n  <div data-composition-id="{cid}" data-width="1080" data-height="960">\n'
            + DEFS.format(p=p)
            + f'    <div id="{p}-world">\n{world}\n    </div>\n    <style>\n'
            + BASE_CSS.format(cid=cid, p=p) + css
            + '\n    </style>\n    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>\n    <script>\n'
            + JS_HEAD.format(cid=cid, p=p, cx0=cx0, cy0=cy0, s0=s0) + js
            + f'\n        window.__timelines["{cid}"] = tl;\n      }})();\n    </script>\n  </div>\n</template>\n')
    open(f"{ROOT}/{name}.html", "w").write(html)


PERSON = "assets/icons/lucide-user.svg"

# --- P1 (abs 0.00-3.90): "Around 3500 people use this subway stop every morning between 8 and 9"
p = "sb"
walkers = []
# deterministic crowd: alternating sides, fixed lanes and start times
for i in range(16):
    side = i % 2
    t0 = 0.15 + i * 0.2
    y = [500, 560, 530, 590][i % 4]
    walkers.append((i, side, t0, y))
world = f"""      <div class="{p}-card" id="{p}-sign"><div class="{p}-torn ink"></div><div class="{p}-signtxt">Bedford Av</div><div class="{p}-bullet"><div class="{p}-torn soft deep"></div><span>L</span></div></div>
      <div class="{p}-card" id="{p}-count"><div class="{p}-torn fire"></div><div class="{p}-num" id="{p}-num">0</div><div class="{p}-caps">people</div></div>
      <div class="{p}-card" id="{p}-stairs"><div class="{p}-torn deep"></div><div class="{p}-ico" style="--i:url('assets/icons/lucide-train-front.svg')"></div></div>
""" + "\n".join(f'      <div class="{p}-walker" id="{p}-p{i}" style="top:{y}px"><div class="{p}-torn soft"></div><div class="{p}-ico" style="--i:url(\'{PERSON}\')"></div></div>' for i, side, t0, y in walkers) + f"""
      <div class="{p}-chip" id="{p}-morn" style="width:330px"><div class="{p}-torn soft"></div><div class="{p}-lbl" style="color:#1c1815">every morning</div></div>
      <div class="{p}-chip" id="{p}-time" style="width:230px"><div class="{p}-torn soft fire"></div><div class="{p}-lbl">8-9 AM</div></div>"""
css = f"""      #{p}-sign {{ left: 250px; top: 80px; width: 580px; height: 130px; }}
      .{p}-signtxt {{ position: absolute; left: 44px; top: 0; height: 130px; display: flex; align-items: center; font-family: "Suisse Intl Medium"; font-size: 58px; color: #f2ece0; letter-spacing: -0.01em; }}
      .{p}-bullet {{ position: absolute; right: 40px; top: 25px; width: 80px; height: 80px; }}
      .{p}-bullet .{p}-torn {{ border-radius: 50%; background: #a7a9ac; }}
      .{p}-bullet span {{ position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; font-family: "Suisse Intl Medium"; font-size: 50px; color: #fff; }}
      #{p}-count {{ left: 330px; top: 250px; width: 420px; height: 170px; }}
      .{p}-num {{ position: absolute; left: 0; right: 0; top: 14px; text-align: center; font-family: "Suisse Intl Medium"; font-size: 104px; line-height: 1; color: #fff6ef; letter-spacing: -0.03em; }}
      .{p}-caps {{ position: absolute; left: 0; right: 0; top: 122px; text-align: center; font-family: "Suisse Intl Medium"; font-size: 22px; letter-spacing: 0.17em; text-transform: uppercase; color: #fff6ef; opacity: 0.85; }}
      #{p}-stairs {{ left: 445px; top: 480px; width: 190px; height: 190px; }}
      #{p}-stairs .{p}-ico {{ top: 40px; width: 110px; height: 110px; margin-left: -55px; }}
      .{p}-walker {{ position: absolute; left: 0; width: 76px; height: 76px; opacity: 0; }}
      .{p}-walker .{p}-torn {{ border-radius: 50%; }}
      .{p}-walker .{p}-ico {{ top: 14px; width: 48px; height: 48px; margin-left: -24px; }}
      #{p}-morn {{ left: 20px; top: 300px; }}
      #{p}-time {{ left: 790px; top: 300px; }}"""
js = f"""        card("#{p}-sign", 0.04);
        card("#{p}-stairs", 0.12);
        // "3500 people" (abs 0.26-1.02): fire card, number counts up
        card("#{p}-count", 0.24);
        const cnt = {{ v: 0 }};
        const numEl = () => document.querySelector(R + "#{p}-num") || document.getElementById("{p}-num");
        tl.fromTo(cnt, {{ v: 0 }}, {{ v: 3500, duration: 1.0, ease: "power2.out", immediateRender: false,
          onUpdate: () => {{ const el = numEl(); if (el) el.textContent = (Math.round(cnt.v / 50) * 50).toLocaleString("en-US"); }} }}, 0.3);
        punch("#{p}-count", 1.32, 1.12);
        cam(540, 400, 1.0, 1.0);
""" + "\n".join(
    f"""        show("#{p}-p{i}", {t0:.2f});
        tl.fromTo(q("#{p}-p{i}"), {{ x: {-100 if side == 0 else 1104} }}, {{ x: {430 if side == 0 else 574}, duration: 1.3, ease: "none" }}, {t0:.2f});
        tl.to(q("#{p}-p{i}"), {{ opacity: 0, scale: 0.5, duration: 0.2 }}, {t0 + 1.12:.2f});""" for i, side, t0, y in walkers) + f"""
        // "subway stop" (abs 1.90)
        punch("#{p}-stairs", 1.9, 1.14);
        pop("#{p}-morn", 2.38);
        pop("#{p}-time", 2.92);
        punch("#{p}-time", 3.3, 1.2);"""
write("coffee-subway-panel", p, None, world, css, js, cam0=(540, 290, 1.3))

# --- P2 (abs 5.633-9.80): "every one of those people could be a potential customer for a small business like a coffee shop"
p = "cu"
XS = [180, 360, 540, 720, 900]
world = "\n".join(f'      <div class="{p}-card {p}-pp" id="{p}-p{i}" style="left:{x - 60}px"><div class="{p}-torn"></div><div class="{p}-torn fire {p}-hot"></div><div class="{p}-ico" style="--i:url(\'{PERSON}\')"></div></div>' for i, x in enumerate(XS)) + "\n" + "\n".join(
    f'      <div class="{p}-drop" id="{p}-d{i}" style="left:{x - 6}px"><div class="{p}-torn soft fire"></div></div>' for i, x in enumerate(XS)) + f"""
      <div class="{p}-chip" id="{p}-cust" style="width:480px"><div class="{p}-torn soft fire"></div><div class="{p}-lbl">potential customers</div></div>
      <div id="{p}-bus"><div class="{p}-torn soft fire"></div></div>
      <div id="{p}-trunk"><div class="{p}-torn soft fire"></div></div>
      <div id="{p}-head"><div class="{p}-torn soft fire"></div></div>
      <div class="{p}-card" id="{p}-shop"><div class="{p}-torn"></div><div class="{p}-ico" id="{p}-store" style="--i:url('assets/icons/lucide-store.svg')"></div><div class="{p}-title" id="{p}-t1">Small business</div><div id="{p}-alt"><div class="{p}-ico" id="{p}-cup" style="--i:url('assets/icons/lucide-coffee.svg')"></div><div class="{p}-title" id="{p}-t2">Coffee shop</div></div></div>"""
css = f"""      .{p}-pp {{ top: 150px; width: 120px; height: 120px; }}
      .{p}-pp .{p}-torn {{ border-radius: 50%; }}
      .{p}-hot {{ opacity: 0; }}
      .{p}-pp .{p}-ico {{ top: 26px; width: 68px; height: 68px; margin-left: -34px; }}
      #{p}-cust {{ left: 300px; top: 50px; }}
      .{p}-drop {{ position: absolute; top: 280px; width: 12px; height: 80px; transform-origin: center top; opacity: 0; }}
      #{p}-bus {{ position: absolute; left: 174px; top: 356px; width: 738px; height: 12px; transform-origin: center center; opacity: 0; }}
      #{p}-trunk {{ position: absolute; left: 534px; top: 362px; width: 12px; height: 56px; transform-origin: center top; opacity: 0; }}
      #{p}-head {{ position: absolute; left: 522px; top: 414px; width: 36px; height: 30px; clip-path: polygon(0 0, 100% 0, 50% 100%); opacity: 0; }}
      #{p}-shop {{ left: 370px; top: 455px; width: 340px; height: 270px; }}
      #{p}-shop .{p}-ico {{ top: 40px; width: 120px; height: 120px; margin-left: -60px; }}
      #{p}-alt {{ position: absolute; inset: 0; opacity: 0; }}
      #{p}-shop .{p}-title {{ top: 190px; font-size: 40px; }}
"""
js = f"""        // "every one of those people" (abs 5.84-6.44)
""" + "\n".join(f'        card("#{p}-p{i}", {0.08 + i * 0.12:.2f});' for i in range(5)) + f"""
        // "potential customer" (abs 7.32): each person lights up
""" + "\n".join(f'        tl.to(q("#{p}-p{i} .{p}-hot"), {{ opacity: 1, duration: 0.18 }}, {1.66 + i * 0.08:.2f}); punch("#{p}-p{i}", {1.66 + i * 0.08:.2f}, 1.15);' for i in range(5)) + f"""
        pop("#{p}-cust", 1.72);
        // "small business" (abs 8.40): they all wire into one shop
        cam(540, 410, 1.0, 2.2);
""" + "\n".join(f"""        show("#{p}-d{i}", {2.5 + i * 0.04:.2f});
        tl.fromTo(q("#{p}-d{i}"), {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.22, ease: "power3.out" }}, {2.5 + i * 0.04:.2f});""" for i in range(5)) + f"""
        show("#{p}-bus", 2.7);
        tl.fromTo(q("#{p}-bus"), {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.25, ease: "power3.out" }}, 2.7);
        show("#{p}-trunk", 2.86);
        tl.fromTo(q("#{p}-trunk"), {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.18, ease: "power3.out" }}, 2.86);
        show("#{p}-head", 3.0);
        tl.fromTo(q("#{p}-head"), {{ scale: 0, y: -16 }}, {{ scale: 1, y: 0, duration: 0.24, ease: "back.out(2)" }}, 3.0);
        card("#{p}-shop", 2.74);
        // "coffee shop" (abs 9.40): the store turns into a coffee shop
        tl.to(q("#{p}-store, #{p}-t1"), {{ opacity: 0, duration: 0.12 }}, 3.74);
        tl.set(q("#{p}-alt"), {{ opacity: 1 }}, 3.76);
        tl.fromTo(q("#{p}-cup"), {{ scale: 0.4, rotation: -14 }}, {{ scale: 1, rotation: 0, duration: 0.36, ease: "back.out(2.4)" }}, 3.76);
        punch("#{p}-shop", 3.78, 1.08);"""
write("coffee-customers-panel", p, None, world, css, js, cam0=(540, 210, 1.2))

# --- P4 (abs 37.167-40.967): "detailed information on your competitors to put your business ahead"
p = "ah"
BARS = [(140, 300, "4.7★"), (360, 380, "30K/mo"), (580, 250, "4.2★")]
BASE = 700
world = f"""      <div id="{p}-base"><div class="{p}-torn soft deep"></div></div>
""" + "\n".join(f"""      <div class="{p}-bar {p}-comp" id="{p}-b{i}" style="left:{x}px;top:{BASE - h}px;height:{h}px"><div class="{p}-torn deep"></div>
        <div class="{p}-line" id="{p}-l{i}a" style="top:40px;width:110px"><div class="{p}-torn soft"></div></div>
        <div class="{p}-line" id="{p}-l{i}b" style="top:78px;width:80px"><div class="{p}-torn soft"></div></div>
        <div class="{p}-line" id="{p}-l{i}c" style="top:116px;width:100px"><div class="{p}-torn soft"></div></div></div>
      <div class="{p}-disc {p}-comp" id="{p}-s{i}" style="left:{x + 25}px;top:{BASE - h - 130}px"><div class="{p}-torn"></div><div class="{p}-ico" style="--i:url('assets/icons/lucide-store.svg')"></div></div>
      <div class="{p}-chip {p}-comp" id="{p}-c{i}" style="width:{70 + 24 * len(st)}px;left:{x + 85 - (35 + 12 * len(st))}px;top:{BASE - 90}px"><div class="{p}-torn soft"></div><div class="{p}-lbl" style="color:#1c1815">{st}</div></div>""" for i, (x, h, st) in enumerate(BARS)) + f"""
      <div class="{p}-chip dark {p}-comp" id="{p}-comps" style="width:360px"><div class="{p}-torn soft"></div><div class="{p}-lbl" style="color:#1c1815">competitors</div></div>
      <div class="{p}-bar" id="{p}-you" style="left:800px;top:{BASE - 520}px;height:520px"><div class="{p}-torn fire"></div></div>
      <div class="{p}-disc" id="{p}-cup" style="left:825px;top:{BASE - 520 - 130}px"><div class="{p}-torn"></div><div class="{p}-ico" style="--i:url('assets/icons/lucide-coffee.svg')"></div></div>
      <div class="{p}-chip" id="{p}-ahead" style="width:250px"><div class="{p}-torn soft"></div><div class="{p}-arrow" style="--i:url('assets/icons/lucide-arrow-up.svg')"></div><div class="{p}-lbl" style="color:#1c1815">ahead</div></div>"""
css = f"""      #{p}-base {{ position: absolute; left: 90px; top: {BASE}px; width: 900px; height: 12px; transform-origin: left center; opacity: 0; }}
      .{p}-bar {{ position: absolute; width: 170px; transform-origin: center bottom; opacity: 0; }}
      .{p}-line {{ position: absolute; left: 30px; height: 16px; transform-origin: left center; opacity: 0; }}
      .{p}-disc {{ position: absolute; width: 120px; height: 120px; opacity: 0; }}
      .{p}-disc .{p}-torn {{ border-radius: 50%; }}
      .{p}-disc .{p}-ico {{ top: 28px; width: 64px; height: 64px; margin-left: -32px; }}
      #{p}-comps {{ left: 210px; top: 70px; }}
      #{p}-ahead {{ left: 530px; top: 140px; gap: 10px; }}
      .{p}-arrow {{ position: relative; width: 30px; height: 30px; background: #1c1815; -webkit-mask: no-repeat center/contain var(--i); mask: no-repeat center/contain var(--i); }}"""
js = f"""        show("#{p}-base", 0.02);
        tl.fromTo(q("#{p}-base"), {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.4, ease: "expo.out" }}, 0.02);
""" + "\n".join(f"""        show("#{p}-b{i}", {0.08 + i * 0.12:.2f});
        tl.fromTo(q("#{p}-b{i}"), {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.45, ease: "back.out(1.4)" }}, {0.08 + i * 0.12:.2f});
        pop("#{p}-s{i}", {0.3 + i * 0.12:.2f});""" for i in range(3)) + f"""
        // "detailed information" (abs 37.96): each competitor fills with data
""" + "\n".join(f"""        ["a", "b", "c"].forEach((k, j) => {{ show("#{p}-l{i}" + k, {0.78 + i * 0.1:.2f} + j * 0.1); tl.fromTo(q("#{p}-l{i}" + k), {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.2, ease: "power2.out" }}, {0.78 + i * 0.1:.2f} + j * 0.1); }});
        pop("#{p}-c{i}", {1.15 + i * 0.12:.2f});""" for i in range(3)) + f"""
        // "your competitors" (abs 39.04-39.20)
        pop("#{p}-comps", 1.95);
        // "put your business ahead" (abs 39.98-40.60)
        cam(565, 420, 0.98, 2.3);
        tl.to(q(".{p}-comp"), {{ opacity: 0.4, duration: 0.3, ease: "sine.inOut" }}, 2.8);
        show("#{p}-you", 2.8);
        tl.fromTo(q("#{p}-you"), {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.55, ease: "back.out(1.3)" }}, 2.8);
        show("#{p}-cup", 2.8);
        tl.fromTo(q("#{p}-cup"), {{ y: 520, scale: 0.6 }}, {{ y: 0, scale: 1, duration: 0.55, ease: "back.out(1.3)" }}, 2.8);
        pop("#{p}-ahead", 3.4);
        punch("#{p}-cup", 3.42, 1.2);"""
write("coffee-ahead-panel", p, None, world, css, js, cam0=(360, 450, 1.25))
print("ok")
