#!/usr/bin/env python3
"""Generate a captioned short composition from a JSON config. See ../SKILL.md for the schema.

usage: gen_captions.py <config.json>   (run from the project root)
"""
import html, json, re, sys

cfg = json.load(open(sys.argv[1]))
DUR = cfg["duration"]
SPLITS = cfg.get("splits", [])
SPLIT_Y = cfg.get("split_y", 850)
BOUNDS = sorted({b for s in SPLITS for b in s})
d = json.load(open(cfg["transcript"]))
words = [dict(w=x["word"], s=x["start"], e=x["end"]) for x in d["words"]]


def norm(t):
    return re.sub(r"[^\w']", "", t).lower()


groups, wi = [], 0
for ph in cfg["phrases"].split("|"):
    toks = ph.split()
    g = words[wi:wi + len(toks)]
    if [norm(x["w"]) for x in g] != [norm(t) for t in toks]:
        sys.exit(f"phrase/transcript mismatch at word {wi}: phrase {toks} vs transcript {[x['w'] for x in g]}")
    groups.append((ph.strip(), g))
    wi += len(toks)
if wi != len(words):
    sys.exit(f"phrases cover {wi} words but transcript has {len(words)}; leftover: {[w['w'] for w in words[wi:]]}")


def split_overlap(a, b):
    return sum(max(0, min(b, y) - max(a, x)) for x, y in SPLITS)


def display(text):
    text = re.sub(r"[.,!?;:]", "", text)
    for k, v in cfg.get("display", {}).items():
        text = re.sub(rf"(?<![\w$]){re.escape(k)}(?![\w])", v, text)
    return text


caps = []
for n, (ph, g) in enumerate(groups):
    start = max(0, g[0]["s"] - 0.04)
    nxt = groups[n + 1][1][0]["s"] - 0.04 if n + 1 < len(groups) else g[-1]["e"] + 0.15
    end = min(nxt, g[-1]["e"] + 0.6, DUR)
    # a caption must never be on screen across a layout change; it would sit in the wrong place
    for b in BOUNDS:
        if g[-1]["e"] <= b < end:
            end = b
    pos = "split" if split_overlap(start, end) > (end - start) / 2 else "full"
    # round both ends first, then shave 0.01s: float noise otherwise makes adjacent clips overlap on one track
    caps.append(dict(start=round(start, 2), dur=round(round(end, 2) - round(start, 2) - 0.01, 2), text=display(ph), pos=pos))

for c in caps:
    print(f'{c["start"]:6.2f} {c["dur"]:4.2f} {c["pos"]:5} {c["text"]}')

full_top = cfg.get("full_caption_top", 900)
split_cap_top = SPLIT_Y - 260
logos_full_top = cfg.get("full_logo_top", full_top + 250)
# split logos go in the speaker half, right-aligned over the background: above the line they covered the UI being narrated
logos_split_top = SPLIT_Y + 40
CAP_BG = {
    "none": "",
    "box": ".cap .t{background:rgba(0,0,0,.9);padding:10px 30px 18px;border-radius:24px;text-shadow:none}",
    "gradient": ".cap::before{content:'';position:absolute;left:0;right:0;top:-60px;bottom:-60px;z-index:-1;"
                "background:linear-gradient(180deg,rgba(0,0,0,0),rgba(0,0,0,.62) 35%,rgba(0,0,0,.62) 65%,rgba(0,0,0,0))}",
}[cfg.get("caption_bg", "box")]

out = [f'''<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=1080, height=1920">
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@700;800&display=swap');
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;background:#000;overflow:hidden}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000}}
#vid{{position:absolute;left:0;top:0;width:1080px;height:1920px;object-fit:cover}}
.sub{{position:absolute;left:0;width:1080px;overflow:hidden}}
.cap{{position:absolute;left:0;width:1080px;height:240px;display:flex;align-items:center;justify-content:center;z-index:10}}
.cap.full{{top:{full_top}px}}
.cap.split{{top:{split_cap_top}px;align-items:flex-end;padding-bottom:22px}}
.cap .t{{display:block;max-width:940px;text-align:center;font-family:'Poppins',sans-serif;font-weight:800;font-size:76px;line-height:1.08;letter-spacing:-1.5px;color:#fff;text-shadow:0 0 22px rgba(0,0,0,.55),0 4px 12px rgba(0,0,0,.6),0 1px 3px rgba(0,0,0,.75)}}
{CAP_BG}
.logos{{position:absolute;left:0;width:1080px;height:230px;display:flex;align-items:center;justify-content:center;gap:44px;z-index:9}}
.logos.full{{top:{logos_full_top}px}}
.logos.split{{top:{logos_split_top}px;height:170px;justify-content:flex-end;padding-right:44px;gap:28px}}
.logos.split .tile{{width:150px;height:150px;border-radius:36px}}
.logos.split .tile img{{width:88px;height:88px}}
.tile{{width:190px;height:190px;border-radius:46px;background:#fff;display:flex;align-items:center;justify-content:center;box-shadow:0 18px 44px rgba(0,0,0,.38),0 2px 6px rgba(0,0,0,.25)}}
.tile img{{width:112px;height:112px;display:block}}
.tile.bare{{background:none;box-shadow:none;width:170px;height:170px;filter:drop-shadow(0 12px 24px rgba(0,0,0,.45))}}
.tile.bare img{{width:150px;height:150px}}
.tile.wide{{width:auto;padding:0 44px}}
.tile.wide img{{width:auto;height:96px}}
</style>
</head>
<body>
<div id="root" data-composition-id="{cfg["id"]}" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920">
<video id="vid" class="clip" data-start="0" data-duration="{DUR}" data-track-index="0" src="{cfg["video"]}" muted playsinline></video>
<audio id="aud" data-start="0" data-duration="{DUR}" data-track-index="1" src="{cfg["video"]}" data-volume="1"></audio>''']

for k, sc in enumerate(cfg.get("subcomps", [])):
    out.append(f'<div id="{sc["id"]}-host" class="sub" style="top:{sc.get("top", 0)}px;height:{sc["height"]}px" '
               f'data-composition-id="{sc["id"]}" data-composition-src="{sc["src"]}" data-start="{sc["start"]}" '
               f'data-duration="{sc["duration"]}" data-track-index="{6 + k}" data-width="1080" data-height="{sc["height"]}"></div>')

for n, c in enumerate(caps):
    out.append(f'<div id="cap{n}" class="clip cap {c["pos"]}" data-start="{c["start"]}" data-duration="{c["dur"]}" data-track-index="2"><span id="t{n}" class="t">{html.escape(c["text"])}</span></div>')

LOGOS = cfg.get("logos", [])
for k, L in enumerate(LOGOS):
    style = L.get("style", "")
    size = f' style="height:{L["img_h"] + 80}px"' if "img_h" in L else ""
    isize = f' style="height:{L["img_h"]}px"' if "img_h" in L else ""
    tiles = "".join(f'<div id="{L["id"]}-{j}" class="tile {style}"{size}><img src="{src}" alt="{alt}"{isize}></div>' for j, (src, alt) in enumerate(L["items"]))
    out.append(f'<div id="{L["id"]}" class="clip logos {L["pos"]}" data-start="{L["start"]}" data-duration="{round(L["end"] - L["start"], 2)}" data-track-index="{3 + k % 2}">{tiles}</div>')

js = ['window.__timelines = window.__timelines || {};', 'const tl = gsap.timeline({ paused: true });']
if cfg.get("caption_anim") == "pop":
    for n, c in enumerate(caps):
        js.append(f'tl.fromTo("#t{n}",{{opacity:0,scale:0.84,y:16}},{{opacity:1,scale:1,y:0,duration:0.16,ease:"back.out(2)"}},{c["start"]});')
for L in LOGOS:
    stag = L.get("stagger", [0] * len(L["items"]))
    for j in range(len(L["items"])):
        sel = f'#{L["id"]}-{j}'
        t0 = round(L["start"] + stag[j] + 0.02, 2)
        rot = -14 + 14 * j
        js.append(f'tl.fromTo("{sel}",{{opacity:0,scale:0.2,rotation:{rot},y:60}},{{opacity:1,scale:1,rotation:0,y:0,duration:0.42,ease:"back.out(2.4)"}},{t0});')
        js.append(f'tl.to("{sel}",{{rotation:3,y:-6,duration:0.5,ease:"sine.inOut"}},{round(t0 + 0.42, 2)});')
        js.append(f'tl.to("{sel}",{{opacity:0,scale:0.7,duration:0.1,ease:"power2.in"}},{round(L["end"] - 0.1, 2)});')
        js.append(f'tl.set("{sel}",{{opacity:0}},{round(L["end"], 2)});')
js.append(f'window.__timelines["{cfg["id"]}"] = tl;')

out.append("<script>\n" + "\n".join(js) + "\n</script>\n</div>\n</body>\n</html>\n")
open(cfg["out"], "w").write("\n".join(out))
print("wrote", cfg["out"])
