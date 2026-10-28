"""Writes the two shots-465 paper-cutout panels (full-frame plate, then top-half plate) into compositions/."""
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


def ad_card(p, i, icon, title, caps, x, top=360):
    return f"""      <div class="{p}-card {p}-ad" id="{p}-c{i}" style="left:{x}px; top:{top}px">
        <div class="{p}-torn"></div>
        <div class="{p}-ico" style="--i:url('assets/icons/lucide-{icon}.svg')"></div>
        <div class="{p}-title">{title}</div>
        <div class="{p}-caps">{caps}</div>
      </div>"""


# --- plate 1, full frame (abs 24.93-27.37): "...because nobody keeps paying for ads that are" ---
# Caption sits centred at y 900-1140 over this plate: cards above, payoff chip below.
p = "wk"
world = "\n".join([
    ad_card(p, 0, "type", "Text ad", "ran 3 days", 60),
    ad_card(p, 1, "image", "Image ad", "still running", 400),
    ad_card(p, 2, "clapperboard", "Video ad", "ran 5 days", 740),
]) + f"""
      <div class="{p}-chip" id="{p}-x0" style="left:110px; top:730px; width:180px"><div class="{p}-torn soft deep"></div><div class="{p}-lbl" style="color:#1c1815">stopped</div></div>
      <div class="{p}-chip" id="{p}-x2" style="left:790px; top:730px; width:180px"><div class="{p}-torn soft deep"></div><div class="{p}-lbl" style="color:#1c1815">stopped</div></div>
      <div class="{p}-chip" id="{p}-days" style="left:420px; top:730px; width:240px"><div class="{p}-torn soft fire"></div><div class="{p}-lbl">412 days</div></div>
      <div class="{p}-chip big" id="{p}-pay" style="left:250px; top:1290px; width:580px"><div class="{p}-torn soft fire"></div><div class="{p}-lbl">still paying = works</div></div>"""
css = f"""      .{p}-ad {{ width: 280px; height: 320px; }}
      .{p}-ad .{p}-ico {{ top: 52px; width: 110px; height: 110px; margin-left: -55px; }}
      .{p}-ad .{p}-title {{ top: 196px; }}
      .{p}-ad .{p}-caps {{ top: 256px; }}"""
js = f"""        // "because" (abs 24.86): three ads up
        card("#{p}-c0", 0.0);
        card("#{p}-c1", 0.08);
        card("#{p}-c2", 0.16);
        // "nobody keeps paying" (abs 25.14-25.72): the short runs get pulled
        pop("#{p}-x0", 0.36);
        pop("#{p}-x2", 0.44);
        tl.to(q("#{p}-c0, #{p}-x0"), {{ y: 90, rotation: -7, opacity: 0.22, duration: 0.45, ease: "power3.in" }}, 0.66);
        tl.to(q("#{p}-c2, #{p}-x2"), {{ y: 90, rotation: 6, opacity: 0.22, duration: 0.45, ease: "power3.in" }}, 0.72);
        // "paying for ads" (abs 25.72-26.38): the long runner stays
        pop("#{p}-days", 0.82);
        punch("#{p}-c1", 0.9, 1.1);
        show("#{p}-pay", 1.45);
        tl.fromTo(q("#{p}-pay"), {{ scale: 0.4, y: 20, rotation: -8 }}, {{ scale: 1, y: 0, rotation: -3, duration: 0.22, ease: "back.out(2.4)" }}, 1.45);"""
write("shots-465-works-panel", p, 1920, 960, world, css, js, cam0=(540, 960, 1.0))

# --- plate 2, top half 1080x996 (abs 27.37-29.57): "and you can copy that strategy in your own ads" ---
# Bottom ~220px stays empty: the split caption sits there.
p = "cp"
world = "\n".join([
    ad_card(p, 0, "image", "Their ad", "412 days live", 60, 170),
    ad_card(p, 1, "megaphone", "Your ad", "same playbook", 680, 170),
]) + f"""
      <div class="{p}-wire" id="{p}-w"><div class="{p}-torn soft fire"></div></div>
      <div class="{p}-head" id="{p}-h"><div class="{p}-torn soft fire"></div></div>
      <div class="{p}-chip" id="{p}-copy" style="left:420px; top:300px; width:180px"><div class="{p}-torn soft fire"></div><div class="{p}-lbl">copy</div></div>
      <div class="{p}-chip big" id="{p}-strat" style="left:300px; top:600px; width:480px"><div class="{p}-torn soft"></div><div class="{p}-lbl" style="color:#1c1815">same strategy</div></div>"""
css = f"""      .{p}-ad {{ width: 340px; height: 380px; }}
      .{p}-ad .{p}-ico {{ top: 60px; width: 130px; height: 130px; margin-left: -65px; }}
      .{p}-ad .{p}-title {{ top: 230px; font-size: 46px; }}
      .{p}-ad .{p}-caps {{ top: 298px; }}
      .{p}-wire {{ position: absolute; left: 420px; top: 384px; width: 220px; height: 12px; transform-origin: left center; opacity: 0; }}
      .{p}-head {{ position: absolute; left: 634px; top: 372px; width: 30px; height: 36px; clip-path: polygon(0 0, 100% 50%, 0 100%); opacity: 0; }}"""
js = f"""        // "and you can" (abs 27.32-27.58): the long runner from the last plate
        card("#{p}-c0", 0.02);
        // "copy" (abs 27.86)
        cam(540, 400, 1.0, 0.3);
        show("#{p}-w", 0.46);
        tl.fromTo(q("#{p}-w"), {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.28, ease: "power3.out" }}, 0.46);
        show("#{p}-h", 0.7);
        tl.fromTo(q("#{p}-h"), {{ scale: 0, x: -20 }}, {{ scale: 1, x: 0, duration: 0.24, ease: "back.out(2)" }}, 0.7);
        pop("#{p}-copy", 0.49);
        card("#{p}-c1", 0.74);
        // "strategy" (abs 28.20)
        show("#{p}-strat", 0.86);
        tl.fromTo(q("#{p}-strat"), {{ scale: 0.4, y: 20, rotation: -8 }}, {{ scale: 1, y: 0, rotation: -2, duration: 0.24, ease: "back.out(2.4)" }}, 0.86);
        // "your own ads" (abs 28.78-29.38)
        punch("#{p}-c1", 1.5, 1.1);"""
write("shots-465-copy-panel", p, 996, 420, world, css, js, cam0=(240, 360, 1.3))
print("ok")
