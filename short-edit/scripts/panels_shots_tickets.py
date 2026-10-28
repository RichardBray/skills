"""Writes the two shots-tickets paper-cutout panel (full-frame plate) into compositions/."""
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
      .{p}-title {{ position: absolute; left: 0; right: 0; text-align: center; font-family: "Suisse Intl Medium"; font-size: 42px; letter-spacing: -0.01em; white-space: nowrap; }}
      .{p}-caps {{ position: absolute; left: 0; right: 0; text-align: center; font-family: "Suisse Intl Medium"; font-size: 21px; letter-spacing: 0.17em; text-transform: uppercase; color: #8a7257; white-space: nowrap; }}
      .{p}-chip {{ position: absolute; display: flex; align-items: center; justify-content: center; padding: 0 18px; height: 60px; opacity: 0; }}
      .{p}-chip.big {{ height: 92px; }}
      .{p}-lbl {{ position: relative; font-family: "Suisse Intl Medium"; font-size: 26px; letter-spacing: 0.16em; text-transform: uppercase; color: #fff6ef; white-space: nowrap; }}
      .{p}-chip.big .{p}-lbl {{ font-size: 38px; letter-spacing: 0.14em; }}
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
          tl.fromTo(q(sel + " > .{p}-torn"), {{ opacity: 0, y: 60, rotation: -2 }}, {{ opacity: 1, y: 0, rotation: 0, duration: 0.4, ease: "back.out(1.5)" }}, t);
          tl.fromTo(q(sel + " .{p}-ico"), {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.4, ease: "back.out(1.8)" }}, t + 0.08);
          tl.fromTo(q(sel + " .{p}-title, " + sel + " .{p}-caps"), {{ opacity: 0, y: 24 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "expo.out" }}, t + 0.12);
        }}
        function pop(sel, t) {{
          show(sel, t);
          tl.fromTo(q(sel), {{ scale: 0.5, y: 16 }}, {{ scale: 1, y: 0, duration: 0.35, ease: "back.out(2)" }}, t);
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


def write(name, p, h, vy, world, css, js, cam0):
    cx0, cy0, s0 = cam0
    html = (f'<template id="{name}-template">\n  <div data-composition-id="{name}" data-width="1080" data-height="{h}">\n'
            + DEFS.format(p=p)
            + f'    <div id="{p}-world">\n{world}\n    </div>\n    <style>\n'
            + BASE_CSS.format(cid=name, p=p, h=h) + css
            + '\n    </style>\n    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>\n    <script>\n'
            + JS_HEAD.format(cid=name, p=p, vy=vy, cx0=cx0, cy0=cy0, s0=s0) + js
            + f'\n        window.__timelines["{name}"] = tl;\n      }})();\n    </script>\n  </div>\n</template>\n')
    open(f"{ROOT}/{name}.html", "w").write(html)


# --- full-frame plate (abs 2.90-5.70): "can be more expensive or cheaper depending on the day" ---
# Caption sits centred at y 900-1140 over this plate: ticket above, day bars below.
p = "tk"
DAYS = [("M", 300, ""), ("T", 280, ""), ("W", 320, ""), ("T", 340, ""), ("F", 150, " cheap"), ("S", 170, " cheap"), ("S", 360, "")]
bars = "\n".join(
    f"""      <div class="{p}-bar{c}" id="{p}-b{i}" style="left:{105 + i * 130}px; height:{h}px"><div class="{p}-torn soft {'fire' if c else 'deep'}"></div></div>
      <div class="{p}-day" id="{p}-d{i}" style="left:{105 + i * 130}px">{d}</div>"""
    for i, (d, h, c) in enumerate(DAYS))
world = f"""      <div class="{p}-card" id="{p}-tix">
        <div class="{p}-torn"></div>
        <div class="{p}-ico" style="--i:url('assets/icons/lucide-ticket.svg')"></div>
        <div class="{p}-name">Game ticket</div>
        <div class="{p}-sub">same seat</div>
        <div class="{p}-price" id="{p}-p0">$148</div>
        <div class="{p}-price up" id="{p}-p1">$212</div>
        <div class="{p}-price" id="{p}-p2">$96</div>
      </div>
      <div class="{p}-chip" id="{p}-up" style="left:720px; top:250px; width:170px"><div class="{p}-torn soft fire"></div><div class="{p}-lbl">+$64</div></div>
      <div class="{p}-chip" id="{p}-down" style="left:720px; top:250px; width:170px"><div class="{p}-torn soft"></div><div class="{p}-lbl" style="color:#1c1815">-$52</div></div>
{bars}"""
css = f"""      #{p}-tix {{ left: 170px; top: 320px; width: 740px; height: 400px; }}
      #{p}-tix .{p}-ico {{ left: 70px; top: 70px; width: 130px; height: 130px; margin-left: 0; }}
      .{p}-name {{ position: absolute; left: 240px; top: 76px; font-family: "Suisse Intl Medium"; font-size: 46px; letter-spacing: -0.01em; white-space: nowrap; }}
      .{p}-sub {{ position: absolute; left: 242px; top: 142px; font-family: "Suisse Intl Medium"; font-size: 21px; letter-spacing: 0.17em; text-transform: uppercase; color: #8a7257; white-space: nowrap; }}
      .{p}-price {{ position: absolute; left: 236px; top: 196px; font-family: "Suisse Intl Medium"; font-size: 140px; line-height: 1; letter-spacing: -0.03em; color: #1c1815; opacity: 0; }}
      .{p}-price.up {{ color: #fa5d19; }}
      .{p}-bar, .{p}-bar.cheap {{ position: absolute; bottom: 220px; width: 90px; transform-origin: 50% 100%; opacity: 0; }}
      .{p}-day {{ position: absolute; top: 1716px; width: 90px; text-align: center; font-family: "Suisse Intl Medium"; font-size: 34px; letter-spacing: 0.1em; color: #a7906f; opacity: 0; }}"""
js = f"""        // "can be" (abs 2.96-3.22): the ticket, at its normal price
        card("#{p}-tix", 0.02);
        tl.fromTo(q("#{p}-p0"), {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "expo.out" }}, 0.16);
        // "more expensive" (abs 3.38-3.58)
        tl.to(q("#{p}-p0"), {{ opacity: 0, y: -30, duration: 0.14, ease: "power2.in" }}, 0.5);
        tl.fromTo(q("#{p}-p1"), {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "back.out(2)" }}, 0.6);
        pop("#{p}-up", 0.62);
        // "or cheaper" (abs 4.06-4.50)
        tl.to(q("#{p}-p1"), {{ opacity: 0, y: 30, duration: 0.14, ease: "power2.in" }}, 1.4);
        tl.to(q("#{p}-up"), {{ opacity: 0, duration: 0.14 }}, 1.4);
        tl.fromTo(q("#{p}-p2"), {{ opacity: 0, y: -40 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "back.out(2)" }}, 1.5);
        pop("#{p}-down", 1.52);
        // "depending on the day" (abs 4.50-5.40): Fri/Sat sit lowest, as the chart later in the video shows
        [0, 1, 2, 3, 4, 5, 6].forEach((i) => {{
          show("#{p}-b" + i + ", #{p}-d" + i, 1.8 + i * 0.06);
          tl.fromTo(q("#{p}-b" + i), {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.36, ease: "back.out(1.6)" }}, 1.8 + i * 0.06);
        }});
        punch("#{p}-b4, #{p}-b5", 2.46, 1.12);"""
write("shots-tickets-panel", p, 1920, 960, world, css, js, cam0=(540, 960, 1.0))
print("ok")
