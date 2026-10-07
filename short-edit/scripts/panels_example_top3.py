"""Writes the five top-3 paper-cutout panels (1080x960, top half) into compositions/."""
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
      .{p}-topbar {{ position: absolute; top: 40px; left: 60px; right: 60px; display: flex; align-items: center; gap: 22px; }}
      .{p}-rule {{ flex: 1; height: 3px; background: #f2ece0; opacity: 0.22; transform-origin: left center; }}
      .{p}-meta {{ font-family: "Suisse Intl Medium"; font-size: 22px; letter-spacing: 0.22em; text-transform: uppercase; color: #a7906f; white-space: nowrap; }}
      .{p}-regmark {{ width: 24px; height: 24px; border: 3px solid #f2ece0; opacity: 0.4; border-radius: 50%; }}
      #{p}-world {{ position: absolute; inset: 0; transform-origin: 0 0; }}
      .{p}-card {{ position: absolute; opacity: 0; }}
      .{p}-ico {{ position: absolute; left: 50%; background: #1c1815; -webkit-mask: no-repeat center/contain var(--i); mask: no-repeat center/contain var(--i); }}
      .{p}-logo {{ position: absolute; left: 50%; object-fit: contain; }}
      .{p}-title {{ position: absolute; left: 0; right: 0; text-align: center; font-family: "Suisse Intl Medium"; font-size: 42px; letter-spacing: -0.01em; white-space: nowrap; }}
      .{p}-chip {{ position: absolute; display: flex; align-items: center; justify-content: center; padding: 0 18px; height: 54px; opacity: 0; }}
      .{p}-lbl {{ position: relative; font-family: "Suisse Intl Medium"; font-size: 23px; letter-spacing: 0.16em; text-transform: uppercase; color: #fff6ef; white-space: nowrap; }}
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
    <div class="{p}-topbar"><div class="{p}-regmark"></div><div class="{p}-meta">{meta}</div><div class="{p}-rule"></div></div>
"""

JS_HEAD = """      (function () {{
        window.__timelines = window.__timelines || {{}};
        const tl = gsap.timeline({{ paused: true }});
        const R = '[data-composition-id="{cid}"] ';
        const q = (s) => s.split(",").map((x) => R + x.trim()).join(", ");
        tl.fromTo(q(".{p}-regmark"), {{ scale: 0, rotation: -90 }}, {{ scale: 1, rotation: 0, duration: 0.4, ease: "back.out(2)" }}, 0.02);
        tl.fromTo(q(".{p}-meta"), {{ opacity: 0, y: -16 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "sine.out" }}, 0.05);
        tl.fromTo(q(".{p}-rule"), {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.6, ease: "expo.out" }}, 0.1);
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
            + DEFS.format(p=p, meta=meta)
            + f'    <div id="{p}-world">\n{world}\n    </div>\n    <style>\n'
            + BASE_CSS.format(cid=cid, p=p) + css
            + '\n    </style>\n    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>\n    <script>\n'
            + JS_HEAD.format(cid=cid, p=p, cx0=cx0, cy0=cy0, s0=s0) + js
            + f'\n        window.__timelines["{cid}"] = tl;\n      }})();\n    </script>\n  </div>\n</template>\n')
    open(f"{ROOT}/{name}.html", "w").write(html)


# --- rank panels: "Number N is X" ---------------------------------------
RANKS = [
    ("top-3-rank-1", "r1", "1", "Firecrawl", "assets/firecrawl-flame-knockout.svg", 0.70),
    ("top-3-rank-2", "r2", "2", "Canva", "assets/icons/canva.svg", 0.74),
    ("top-3-rank-3", "r3", "3", "Gmail", "assets/icons/gmail.svg", 0.60),
]
for name, p, num, label, logo, t_name in RANKS:
    world = f"""      <div class="{p}-card" id="{p}-num"><div class="{p}-torn fire"></div><div class="{p}-n">{num}</div></div>
      <div class="{p}-card" id="{p}-pick"><div class="{p}-torn"></div><img class="{p}-logo" src="{logo}" alt="{label}"><div class="{p}-title">{label}</div></div>
      <div class="{p}-chip dark" id="{p}-tag" style="width:180px"><div class="{p}-torn soft ink"></div><div class="{p}-lbl">plugin</div></div>"""
    css = f"""      #{p}-num {{ left: 110px; top: 170px; width: 360px; height: 420px; }}
      .{p}-n {{ position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; font-family: "Suisse Intl Medium"; font-size: 330px; line-height: 1; color: #1c1815; letter-spacing: -0.04em; }}
      #{p}-pick {{ left: 540px; top: 190px; width: 400px; height: 380px; }}
      #{p}-pick .{p}-logo {{ top: 60px; width: 170px; height: 170px; margin-left: -85px; }}
      #{p}-pick .{p}-title {{ top: 268px; font-size: 52px; }}
      #{p}-tag {{ left: 760px; top: 160px; }}"""
    js = f"""        show("#{p}-num", 0.04);
        tl.fromTo(q("#{p}-num > .{p}-torn"), {{ scale: 0.2, rotation: -20 }}, {{ scale: 1, rotation: -4, duration: 0.42, ease: "back.out(2)" }}, 0.04);
        tl.fromTo(q("#{p}-num .{p}-n"), {{ scale: 0.3, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.4, ease: "back.out(2.2)" }}, 0.12);
        card("#{p}-pick", {t_name - 0.3:.2f});
        pop("#{p}-tag", {t_name:.2f});"""
    write(name, p, "Top 3 ChatGPT plugins", world, css, js, cam0=(540, 380, 1.08))

# --- G2: sources wired into ChatGPT, then limited web search -------------
p = "sd"
srcs = [("shopify", "assets/icons/shopify.svg", "Shopify", 110), ("apollo", "assets/leadgen/logos/apollo-mark.svg", "Apollo", 300),
        ("benz", "assets/icons/benzinga-wordmark.png", "Benzinga", 490)]
world = f"""      <div class="{p}-card" id="{p}-gpt"><div class="{p}-torn"></div><div class="{p}-ico" style="--i:url('assets/icons/openai.svg')"></div><div class="{p}-title">ChatGPT</div></div>
""" + "\n".join(
    f"""      <div class="{p}-card {p}-src" id="{p}-{k}"><div class="{p}-torn"></div><img class="{p}-logo" src="{src}" alt="{lab}"></div>
      <div class="{p}-wire" id="{p}-w{i}" style="top:{y + 69}px"><div class="{p}-torn soft fire"></div></div>
      <div class="{p}-head" id="{p}-h{i}" style="top:{y + 57}px"><div class="{p}-torn soft fire"></div></div>
      <div class="{p}-bit" id="{p}-b{i}" style="top:{y + 59}px"><div class="{p}-torn soft"></div></div>"""
    for i, (k, src, lab, y) in enumerate(srcs)) + f"""
      <div class="{p}-chip" id="{p}-rt" style="width:210px"><div class="{p}-torn soft fire"></div><div class="{p}-lbl">real-time</div></div>
      <div class="{p}-chip" id="{p}-acc" style="width:200px"><div class="{p}-torn soft fire"></div><div class="{p}-lbl">accurate</div></div>
      <div class="{p}-card" id="{p}-web"><div class="{p}-torn deep"></div><div class="{p}-ico" style="--i:url('assets/icons/lucide-search.svg')"></div><div class="{p}-title">Web search</div></div>
      <div class="{p}-wire dash" id="{p}-wweb"><div class="{p}-torn soft"></div></div>
      <div class="{p}-chip dark" id="{p}-lim" style="width:180px"><div class="{p}-torn soft ink"></div><div class="{p}-lbl">limited</div></div>
      <div class="{p}-chip dark" id="{p}-guess" style="width:170px"><div class="{p}-torn soft ink"></div><div class="{p}-lbl">guess?</div></div>"""
css = f"""      #{p}-gpt {{ left: 70px; top: 230px; width: 300px; height: 330px; }}
      #{p}-gpt .{p}-ico {{ top: 60px; width: 130px; height: 130px; margin-left: -65px; }}
      #{p}-gpt .{p}-title {{ top: 230px; }}
      .{p}-src {{ left: 720px; width: 290px; height: 150px; }}
      #{p}-shopify {{ top: 110px; }} #{p}-apollo {{ top: 300px; }} #{p}-benz {{ top: 490px; }}
      .{p}-src .{p}-logo {{ top: 35px; height: 80px; width: 220px; margin-left: -110px; }}
      #{p}-benz .{p}-logo {{ top: 52px; height: 46px; }}
      .{p}-wire {{ position: absolute; left: 404px; width: 300px; height: 12px; transform-origin: right center; opacity: 0; }}
      .{p}-head {{ position: absolute; left: 378px; width: 30px; height: 36px; clip-path: polygon(100% 0, 0 50%, 100% 100%); opacity: 0; }}
      .{p}-bit {{ position: absolute; left: 650px; width: 34px; height: 32px; opacity: 0; }}
      #{p}-rt {{ left: 440px; top: 100px; }}
      #{p}-acc {{ left: 445px; top: 620px; }}
      #{p}-web {{ left: 720px; top: 250px; width: 290px; height: 290px; }}
      #{p}-web .{p}-ico {{ top: 50px; width: 110px; height: 110px; margin-left: -55px; }}
      #{p}-web .{p}-title {{ top: 190px; font-size: 40px; }}
      #{p}-wweb {{ top: 389px; }}
      #{p}-lim {{ left: 775px; top: 180px; }}
      #{p}-guess {{ left: 780px; top: 560px; }}"""
js = f"""        // "So ChatGPT pulls" (abs 12.10-12.98)
        card("#{p}-gpt", 0.12);
        punch("#{p}-gpt .{p}-ico", 0.38);
        cam(540, 400, 1.0, 0.75);
        ["#{p}-shopify", "#{p}-apollo", "#{p}-benz"].forEach((s, i) => card(s, 0.85 + i * 0.12));
        [0, 1, 2].forEach((i) => {{
          show("#{p}-w" + i, 1.1 + i * 0.1);
          tl.fromTo(q("#{p}-w" + i), {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.3, ease: "power3.out" }}, 1.1 + i * 0.1);
          show("#{p}-h" + i, 1.34 + i * 0.1);
          tl.fromTo(q("#{p}-h" + i), {{ scale: 0, x: 20 }}, {{ scale: 1, x: 0, duration: 0.26, ease: "back.out(2)" }}, 1.34 + i * 0.1);
        }});
        // "real-time, accurate" (abs 13.48, 14.64)
        pop("#{p}-rt", 1.41);
        pop("#{p}-acc", 2.57);
        // "directly from these sources" (abs 15.02-16.42): data bits travel along the wires
        [0, 1, 2].forEach((i) => {{
          show("#{p}-b" + i, 2.95 + i * 0.14);
          tl.fromTo(q("#{p}-b" + i), {{ x: 0 }}, {{ x: -230, duration: 0.9, ease: "power2.inOut" }}, 2.95 + i * 0.14);
          tl.to(q("#{p}-b" + i), {{ opacity: 0, duration: 0.15 }}, 3.85 + i * 0.14);
        }});
        punch("#{p}-gpt", 4.0, 1.08);
        // "instead of using its limited web search to guess" (abs 16.62-18.64)
        tl.to(q(".{p}-src, .{p}-wire:not(.dash), .{p}-head, #{p}-rt, #{p}-acc"), {{ opacity: 0.1, duration: 0.4, ease: "sine.inOut" }}, 4.5);
        card("#{p}-web", 4.75);
        show("#{p}-wweb", 5.05);
        tl.fromTo(q("#{p}-wweb"), {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.35, ease: "power3.out" }}, 5.05);
        pop("#{p}-lim", 5.5);
        cam(540, 400, 1.1, 6.2);
        pop("#{p}-guess", 6.57);
        punch("#{p}-guess", 6.95, 1.3);"""
write("top-3-sources-panel", p, "Why it beats web search", world, css, js, cam0=(220, 395, 1.45))

# --- G5: trained to write in my style -------------------------------------
p = "st"
lines = "\n".join(f'        <div class="{p}-line" id="{p}-l{i}" style="top:{150 + i * 46}px;width:{w}px"><div class="{p}-torn soft deep"></div></div>'
                  for i, w in enumerate([300, 340, 260, 320, 200]))
world = f"""      <div class="{p}-card" id="{p}-gpt"><div class="{p}-torn"></div><div class="{p}-ico" style="--i:url('assets/icons/openai.svg')"></div><div class="{p}-title">ChatGPT</div></div>
      <div class="{p}-wire" id="{p}-w"><div class="{p}-torn soft fire"></div></div>
      <div class="{p}-head" id="{p}-h"><div class="{p}-torn soft fire"></div></div>
      <div class="{p}-card" id="{p}-mail"><div class="{p}-torn"></div><img class="{p}-logo" src="assets/icons/gmail.svg" alt="Gmail"><div class="{p}-sub">Draft</div>
{lines}
      </div>
      <div class="{p}-chip" id="{p}-style" style="width:220px"><div class="{p}-torn soft fire"></div><div class="{p}-lbl">my style</div></div>
      <div class="{p}-stamp" id="{p}-me"><div class="{p}-torn ink"></div><div class="{p}-ico" style="--i:url('assets/icons/lucide-user.svg')"></div></div>
      <div class="{p}-chip" id="{p}-like" style="width:260px"><div class="{p}-torn soft"></div><div class="{p}-lbl" style="color:#1c1815">sounds like me</div></div>"""
css = f"""      #{p}-gpt {{ left: 60px; top: 240px; width: 280px; height: 320px; }}
      #{p}-gpt .{p}-ico {{ top: 56px; width: 120px; height: 120px; margin-left: -60px; }}
      #{p}-gpt .{p}-title {{ top: 220px; font-size: 40px; }}
      .{p}-wire {{ position: absolute; left: 350px; top: 394px; width: 120px; height: 12px; transform-origin: left center; opacity: 0; }}
      .{p}-head {{ position: absolute; left: 464px; top: 382px; width: 30px; height: 36px; clip-path: polygon(0 0, 100% 50%, 0 100%); opacity: 0; }}
      #{p}-mail {{ left: 510px; top: 150px; width: 470px; height: 470px; }}
      #{p}-mail .{p}-logo {{ left: 40px; top: 40px; width: 70px; height: 70px; }}
      .{p}-sub {{ position: absolute; left: 130px; top: 54px; font-family: "Suisse Intl Medium"; font-size: 36px; }}
      .{p}-line {{ position: absolute; left: 50px; height: 22px; transform-origin: left center; opacity: 0; }}
      .{p}-line .{p}-torn {{ background: #cdbfa6; }}
      #{p}-style {{ left: 540px; top: 640px; }}
      .{p}-stamp {{ position: absolute; left: 860px; top: 520px; width: 130px; height: 130px; opacity: 0; }}
      .{p}-stamp .{p}-torn {{ border-radius: 50%; }}
      .{p}-stamp .{p}-ico {{ top: 30px; width: 70px; height: 70px; margin-left: -35px; background: #f2ece0; }}
      #{p}-like {{ left: 780px; top: 680px; }}"""
js = f"""        // "I've trained ChatGPT" (abs 43.82-44.22)
        card("#{p}-gpt", 0.1);
        card("#{p}-mail", 0.4);
        show("#{p}-w", 0.62);
        tl.fromTo(q("#{p}-w"), {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.3, ease: "power3.out" }}, 0.62);
        show("#{p}-h", 0.86);
        tl.fromTo(q("#{p}-h"), {{ scale: 0, x: -20 }}, {{ scale: 1, x: 0, duration: 0.26, ease: "back.out(2)" }}, 0.86);
        // "to write in my style" (abs 44.84-45.60): the draft writes itself line by line
        [0, 1, 2, 3, 4].forEach((i) => {{
          show("#{p}-l" + i, 1.14 + i * 0.16);
          tl.fromTo(q("#{p}-l" + i), {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.22, ease: "power2.out" }}, 1.14 + i * 0.16);
        }});
        pop("#{p}-style", 1.64);
        // "so they always sound like me" (abs 45.84-46.88)
        show("#{p}-me", 2.4);
        tl.fromTo(q("#{p}-me"), {{ scale: 2.2, rotation: -30 }}, {{ scale: 1, rotation: -8, duration: 0.24, ease: "power4.in" }}, 2.4);
        punch("#{p}-mail", 2.64, 1.05);
        pop("#{p}-like", 2.85);"""
write("top-3-style-panel", p, "Trained on my emails", world, css, js, cam0=(540, 400, 1.0))
print("ok")
