"""Writes compositions/coffee-claude-panel.html: a Claude desktop home screen (full frame, 1080x1920)
with the spoken prompt typed into the input, char by char inside each word's Whisper window."""
import html, json

ROOT = "/Users/robray/fc/firecrawl-transition"
START, DUR = 18.2, 6.067
d = json.load(open(f"{ROOT}/assets/clips/coffee-shop-location-fast.json"))
ws = [w for w in d["words"] if START <= w["start"] < START + DUR]
assert ws[0]["word"] == "I" and ws[-1]["word"] == "hour", [w["word"] for w in ws]
# Whisper drops punctuation from word tokens; put the sentence breaks back
PUNCT = {"Williamsburg": "Williamsburg.", "hour": "hour."}

chars, sets = [], []
n = 0
for k, w in enumerate(ws):
    text = PUNCT.get(w["word"], w["word"]) + ("" if k == len(ws) - 1 else " ")
    t0 = w["start"] - START
    # fast words get squashed by Whisper: give every word at least 0.18s to type
    span = max(0.18, min(w["end"] - w["start"], 0.45))
    for j, ch in enumerate(text):
        chars.append(f'<span class="cl-ch" id="cl-c{n}">{html.escape(ch)}</span>')
        sets.append(f'tl.set(q("#cl-c{n}"), {{ display: "inline" }}, {t0 + span * j / len(text):.3f});')
        n += 1
TYPE_START = ws[0]["start"] - START
TYPE_END = ws[-1]["start"] - START + 0.3

ico = lambda name, cls="cl-i": f'<div class="{cls}" style="--i:url(\'assets/icons/lucide-{name}.svg\')"></div>'
out = f"""<template id="coffee-claude-panel-template">
  <div data-composition-id="coffee-claude-panel" data-width="1080" data-height="1920">
    <div class="cl-bg"></div>
    <div id="cl-greet"><div class="cl-star"></div><span>Afternoon, Richard</span></div>
    <div id="cl-box">
      <div class="cl-text"><span class="cl-ph" id="cl-ph">How can I help you today?</span>{"".join(chars)}<span class="cl-cur" id="cl-cur"></span></div>
      <div class="cl-bar">
        {ico("plus", "cl-i cl-plus")}
        <div class="cl-seg"><div class="cl-on">Chat</div><div>Cowork</div></div>
        <div class="cl-model">Sonnet 5.5 <span>Medium</span></div>
        {ico("mic", "cl-i cl-mic")}
        {ico("chevron-down", "cl-i cl-chev")}
        <div class="cl-voice" id="cl-voice">{ico("audio-lines")}</div>
        <div class="cl-send" id="cl-send">{ico("arrow-up")}</div>
      </div>
    </div>
    <div id="cl-chips">
      <div class="cl-chip">{ico("pencil")}Write</div>
      <div class="cl-chip">{ico("chart-line")}Strategize</div>
      <div class="cl-chip">{ico("signpost")}Career chat</div>
      <div class="cl-chip">{ico("lightbulb")}Claude’s choice</div>
    </div>
    <style>
      @font-face {{ font-family: "Newsreader"; src: url("assets/fonts/Newsreader-Regular.woff2") format("woff2"); }}
      @font-face {{ font-family: "Suisse Intl"; src: url("assets/SuisseIntl-Regular.otf") format("opentype"); }}
      [data-composition-id="coffee-claude-panel"] {{ position: relative; width: 1080px; height: 1920px; overflow: hidden;
        font-family: "Suisse Intl", system-ui, sans-serif; color: #e8e6df; background: #171716; }}
      [data-composition-id="coffee-claude-panel"] * {{ box-sizing: border-box; }}
      .cl-bg {{ position: absolute; inset: 0; background: #171716; }}
      #cl-greet {{ position: absolute; left: 0; right: 0; top: 380px; display: flex; align-items: center; justify-content: center; gap: 22px;
        font-family: "Newsreader", Georgia, serif; font-size: 82px; letter-spacing: -0.015em; color: #eeece6; }}
      .cl-star {{ width: 74px; height: 74px; background: #d97757; -webkit-mask: no-repeat center/contain url("assets/icons/claude.svg"); mask: no-repeat center/contain url("assets/icons/claude.svg"); }}
      #cl-box {{ position: absolute; left: 44px; top: 530px; width: 992px; height: 330px; background: #262624; border: 2px solid #3b3a37; border-radius: 30px; }}
      .cl-text {{ position: absolute; left: 34px; right: 34px; top: 30px; font-size: 36px; line-height: 50px; color: #eeece6; }}
      .cl-ph {{ color: #8e8c86; }}
      .cl-ch {{ display: none; }}
      .cl-cur {{ display: inline-block; width: 3px; height: 40px; margin-left: 2px; vertical-align: -7px; background: #eeece6; }}
      .cl-bar {{ position: absolute; left: 26px; right: 26px; bottom: 24px; height: 64px; display: flex; align-items: center; gap: 14px; font-size: 30px; }}
      .cl-i {{ width: 34px; height: 34px; flex: none; background: #c9c6be; -webkit-mask: no-repeat center/contain var(--i); mask: no-repeat center/contain var(--i); }}
      .cl-plus {{ width: 40px; height: 40px; margin: 0 8px; background: #e8e6df; }}
      .cl-seg {{ display: flex; padding: 5px; gap: 4px; background: #1d1d1b; border-radius: 14px; color: #c9c6be; }}
      .cl-seg div {{ padding: 8px 18px; border-radius: 10px; }}
      .cl-seg .cl-on {{ background: #3a3936; border: 1.5px solid #4a4945; color: #eeece6; }}
      .cl-model {{ margin-left: auto; color: #d8d5cd; white-space: nowrap; }}
      .cl-model span {{ color: #8e8c86; margin-left: 6px; }}
      .cl-mic {{ margin-left: 18px; }}
      .cl-chev {{ width: 22px; height: 22px; background: #8e8c86; }}
      .cl-voice, .cl-send {{ position: relative; width: 56px; height: 56px; margin-left: 10px; display: flex; align-items: center; justify-content: center; border-radius: 14px; }}
      .cl-send {{ position: absolute; right: 0; background: #c6613f; opacity: 0; }}
      .cl-send .cl-i {{ background: #fff; width: 30px; height: 30px; }}
      #cl-chips {{ position: absolute; left: 0; right: 0; top: 1220px; display: flex; justify-content: center; gap: 14px; }}
      .cl-chip {{ display: flex; align-items: center; gap: 12px; height: 68px; padding: 0 22px; background: #2a2a28; border-radius: 16px; font-size: 29px; color: #e8e6df; white-space: nowrap; }}
      .cl-chip .cl-i {{ width: 30px; height: 30px; background: #a8a59d; }}
    </style>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <script>
      (function () {{
        window.__timelines = window.__timelines || {{}};
        const tl = gsap.timeline({{ paused: true }});
        const R = '[data-composition-id="coffee-claude-panel"] ';
        const q = (s) => s.split(",").map((x) => R + x.trim()).join(", ");
        tl.fromTo(q("#cl-greet"), {{ opacity: 0, y: 24 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "expo.out" }}, 0);
        tl.fromTo(q("#cl-box"), {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "expo.out" }}, 0.03);
        tl.fromTo(q("#cl-chips"), {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "expo.out" }}, 0.08);
        tl.set(q("#cl-cur"), {{ opacity: 0 }}, 0.07);
        tl.set(q("#cl-cur"), {{ opacity: 1 }}, {TYPE_START - 0.02:.3f});
        tl.set(q("#cl-ph"), {{ display: "none" }}, {TYPE_START:.3f});
        tl.set(q("#cl-voice"), {{ opacity: 0 }}, {TYPE_START:.3f});
        tl.fromTo(q("#cl-send"), {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.22, ease: "back.out(2)" }}, {TYPE_START:.3f});
        {chr(10).join("        " + s for s in sets).strip()}
        for (let t = {TYPE_END:.3f}; t < {DUR - 0.1}; t += 0.5) {{
          tl.set(q("#cl-cur"), {{ opacity: 0 }}, t);
          tl.set(q("#cl-cur"), {{ opacity: 1 }}, t + 0.25);
        }}
        window.__timelines["coffee-claude-panel"] = tl;
      }})();
    </script>
  </div>
</template>
"""
open(f"{ROOT}/compositions/coffee-claude-panel.html", "w").write(out)
print(n, "chars", TYPE_START, TYPE_END)
