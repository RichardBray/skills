#!/usr/bin/env python3
"""vidIQ-style YouTube title score (0-100), fitted to real vidIQ scores.

Feature-based linear model. Coefficients in COEF are produced by
scripts/calibrate.py from data/calibration.json (title -> real vidIQ score).

Usage: score.py "Your title here"     -> score + feature contributions
       score.py --json "Title"        -> JSON output
       echo "Title" | score.py -      -> one title per line from stdin
"""
import argparse
import json
import os
import re
import sys
from functools import lru_cache

# --- vocabularies -----------------------------------------------------------

# Curiosity / stakes / emotion. vidIQ rewards these heavily.
CURIOSITY = {
    "secret", "secrets", "shocking", "insane", "crazy", "weird", "strange",
    "hidden", "truth", "revealed", "reveal", "exposed", "mystery", "nobody",
    "wrong", "stop", "quit", "destroys", "beats", "actually", "really",
    "forever", "everything", "never", "always", "surprising", "brutal",
    "dangerous", "broken", "dead", "killed", "worst", "best", "finally",
}

# Framing verbs/nouns that signal a story or a result, not a lecture.
NARRATIVE = {
    "i", "my", "me", "we", "our", "built", "tested", "tried", "replaced",
    "cut", "quit", "shipped", "rebuilt", "broke", "fixed", "made", "spent",
}

# Direct address. Strong vidIQ signal.
SECOND_PERSON = {"you", "your", "you're", "youre", "yours"}

# Audience / promise words that widen the funnel.
AUDIENCE = {
    "beginners", "beginner", "tutorial", "guide", "explained", "learn",
    "walkthrough", "course", "basics", "crash", "intro", "introduction",
}

# Dry academic framing vidIQ punishes.
DRY_OPENERS = (
    "understanding ", "introduction to ", "an introduction", "overview of ",
    "building a ", "building an ", "getting started with ", "working with ",
    "exploring ", "a comprehensive",
)

DEPTH_PHRASES = ("deep dive", "from scratch", "full config", "walkthrough",
                 "under the hood", "internals", "from zero")

CONFLICT_PHRASES = ("gets wrong", "went badly", "ruins", "leaking", "is slow",
                    "slower than", "don't know", "doesn't work", "is broken",
                    "stopped using", "nobody talks about", "nobody told you")

# vidIQ's own emotion taxonomy, taken from the "Emotion" selector in its title
# SUGGESTION feature. vidIQ has never published the scorer's factors, so this is
# the closest thing to its native vocabulary for titles -- worth encoding on the
# theory that the generator and the scorer share a feature space.
EMOTION_PATTERNS = {
    "e_comparison": r"\b(vs|versus|compared|comparison|better than|instead of|"
                    r"or)\b",
    "e_credibility": r"\b(i|we|my|our|actually|really|honest|truth|proven|"
                     r"tested|years?|experience|senior|staff|expert)\b",
    "e_curiosity": r"\b(why|how|what|secret|hidden|nobody|surprising|weird|"
                   r"reason|happens?|discovered)\b",
    "e_desire": r"\b(best|fastest|easiest|perfect|ultimate|free|10x|faster|"
                r"simple|clean|beautiful|dream)\b",
    "e_extreme": r"\b(insane|crazy|never|always|every|everything|entire|"
                 r"completely|totally|forever|100x|worst|destroys?)\b",
    "e_list": r"^\s*\d+\b|\b\d+\s+(things|ways|tips|tricks|reasons|mistakes|"
              r"signs|steps|lessons|patterns|tools|levers)\b",
    "e_negativity": r"\b(wrong|broken|bad|fail\w*|slow|useless|stop|quit|"
                    r"mistake|dead|worse|hate|regret\w*|badly|dangerous)\b",
    "e_question": r"\?",
    "e_time": r"\b(\d+\s*(seconds?|minutes?|hours?|days?|weeks?|months?|years?)|"
              r"in 20\d\d|now|today|finally|still|already|before)\b",
}

WORD_RE = re.compile(r"[A-Za-z0-9'%.\-]+")


def features(title: str) -> dict:
    t = title.strip()
    low = t.lower()
    words = WORD_RE.findall(t)
    wl = [w.lower() for w in words]
    n = len(words) or 1
    letters = [c for c in t if c.isalpha()]

    return {
        # Length in chars, scaled to ~0-1 over the useful range, saturating.
        "len": min(len(t), 90) / 90.0,
        # Very short titles are a distinct cliff, not just "less length".
        "stub": 1.0 if len(words) <= 2 else 0.0,
        "words": min(n, 16) / 16.0,
        "number": 1.0 if re.search(r"\d", t) else 0.0,
        "curiosity": min(sum(w in CURIOSITY for w in wl), 3) / 3.0,
        "narrative": min(sum(w in NARRATIVE for w in wl), 3) / 3.0,
        "second_person": min(sum(w in SECOND_PERSON for w in wl), 2) / 2.0,
        "audience": min(sum(w in AUDIENCE for w in wl), 2) / 2.0,
        "question": 1.0 if "?" in t else 0.0,
        "colon": 1.0 if ":" in t else 0.0,
        "parens": 1.0 if "(" in t else 0.0,
        "bang": min(t.count("!"), 3) / 3.0,
        "caps": (sum(c.isupper() for c in letters) / len(letters)) if letters else 0.0,
        "dry": 1.0 if low.startswith(DRY_OPENERS) else 0.0,
        "vs": 1.0 if re.search(r"\b(vs|versus)\b", low) else 0.0,
        # Depth framing: signals a substantial video rather than a tip list.
        "depth": 1.0 if any(p in low for p in DEPTH_PHRASES) else 0.0,
        # Negative-outcome / conflict framing ("went badly", "gets wrong").
        "conflict": min(sum(p in low for p in CONFLICT_PHRASES), 2) / 2.0,
        # The three framings that minimal-pair testing showed actually move the
        # score, holding the topic fixed. "X Explained" was measured to be
        # roughly neutral, so it earns a feature mainly to absorb that bias.
        "accusation": 1.0 if re.search(
            r"\b(your|you're|youre|you)\b.{0,40}\b(wrong|broken|slow|useless|"
            r"liability|too many|too much|worse|fail\w*|don't|probably)\b",
            low) else 0.0,
        "first_person_result": 1.0 if re.search(
            r"\bi\b.{0,40}\b(cut|killed|took|built|made|rewrote|replaced|"
            r"deleted|shipped|trained|spent|ran|got|fixed|broke)\b",
            low) else 0.0,
        "explained_suffix": 1.0 if low.rstrip(" ?!.").endswith("explained") else 0.0,
        **{name: 1.0 if re.search(pat, low) else 0.0
           for name, pat in EMOTION_PATTERNS.items()},
    }


def ngrams(title: str) -> dict:
    """Word uni/bigrams plus character 3-5 grams, as a presence map.

    vidIQ's score turns out to be a learned text model, not a checklist: titles
    with identical structure but different topic words score far apart. The
    hand features above capture the structural part; these capture the rest.
    Character grams measurably beat word grams alone -- they generalize across
    morphology and to topic words never seen during calibration.
    """
    wl = [w.lower() for w in WORD_RE.findall(title)]
    grams = {f"w:{w}": 1.0 for w in wl}
    grams.update({f"b:{a} {b}": 1.0 for a, b in zip(wl, wl[1:])})

    s = " " + title.lower().strip() + " "
    for n in (3, 4, 5):
        for i in range(len(s) - n + 1):
            grams[f"c:{s[i:i + n]}"] = 1.0
    return grams


MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "..", "data", "model.json")


@lru_cache(maxsize=1)
def _model() -> dict:
    with open(MODEL_PATH) as f:
        return json.load(f)


def score_title(title: str) -> dict:
    m = _model()
    coef = m["coef"]
    f = features(title)
    g = ngrams(title)

    contrib = {k: coef[k] * v for k, v in f.items() if k in coef}
    gram_total = sum(coef[k] * v for k, v in g.items() if k in coef)
    raw = m["intercept"] + sum(contrib.values()) + gram_total

    return {
        "title": title.strip(),
        "score": round(max(0, min(100, raw))),
        "chars": len(title.strip()),
        "words": len(WORD_RE.findall(title)),
        "features": {k: round(v, 3) for k, v in f.items()},
        "contributions": {k: round(v, 2) for k, v in contrib.items()
                          if abs(v) >= 0.5},
        "vocab": round(gram_total, 2),
    }


def fmt(r: dict) -> str:
    top = sorted(r["contributions"].items(), key=lambda kv: -abs(kv[1]))
    parts = ", ".join(f"{k}{v:+.1f}" for k, v in top)
    return (f"{r['score']}  {r['title']}\n"
            f"  chars={r['chars']} words={r['words']} vocab={r['vocab']:+.1f}\n"
            f"  {parts}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("title", nargs="?", help="Title to score (or '-' for stdin)")
    p.add_argument("--json", action="store_true", help="JSON output")
    a = p.parse_args()

    titles = ([line.strip() for line in sys.stdin if line.strip()]
              if a.title in (None, "-") else [a.title])
    results = [score_title(t) for t in titles]
    if a.json:
        print(json.dumps(results if len(results) > 1 else results[0], indent=2))
    else:
        for r in results:
            print(fmt(r))


if __name__ == "__main__":
    main()
