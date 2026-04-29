#!/usr/bin/env python3
"""Heuristic reimplementation of vidIQ-style YouTube title score (0-100).

Not affiliated with vidIQ. Weights are tunable in WEIGHTS at the top.
Usage: score.py "Your title here"     -> prints score + breakdown
       score.py --json "Title"        -> JSON output
       echo "Title" | score.py -      -> reads from stdin (one per line)
"""
import argparse
import json
import re
import sys

WEIGHTS = {
    "length":       1.5,
    "word_count":   1.0,
    "number":       0.6,
    "power":        1.0,
    "sentiment":    0.9,
    "caps":         0.9,
    "punct":        0.7,
    "stopword":     0.7,
    "specificity": 1.6,
    "cliche":       0.9,
}

CLICHE_PHRASES = [
    "ultimate guide", "change your life", "you must", "do this instead",
    "you need to know", "for beginners", "will blow your mind",
    "that will change", "you should know", "in 2026", "in 2025",
    "everything you", "the best way",
]

POWER_WORDS = {
    # curiosity / surprise
    "secret","secrets","shocking","insane","crazy","weird","strange","hidden",
    "truth","revealed","reveal","exposed","mystery","why","how","what","this",
    # superlatives / comparative
    "best","worst","fastest","slowest","biggest","smallest","ultimate","top",
    "perfect","powerful","amazing","incredible","essential","favorite",
    # value / utility
    "free","new","easy","simple","quick","instant","proven","guide","tutorial",
    # emotional
    "love","hate","fail","mistake","mistakes","wrong","never","stop","avoid",
    # tech-flavored
    "killer","destroys","beats","faster","better","vs","versus",
    # narrative / curiosity-gap
    "tried","happened","saved","quit","released",
}

STOPWORDS = {
    "a","an","the","of","in","on","at","to","for","with","and","or","but",
    "is","are","was","were","be","been","being","it","its","as","by","from",
    "that","this","these","those","i","you","he","she","we","they",
}

POSITIVE = {"best","amazing","incredible","perfect","love","powerful","fast","faster",
            "easy","simple","new","free","great","awesome","beautiful","beats","wins"}
NEGATIVE = {"worst","hate","fail","wrong","stop","never","avoid","bad","slow","ugly",
            "mistake","mistakes","destroys","killer","crazy","insane","shocking"}


def length_score(title: str) -> float:
    n = len(title)
    if n < 20: return max(0, n * 2)             # 0-40
    if n <= 40: return 60 + (n - 20)            # 60-80
    if n <= 60: return 90 + (n - 40) * 0.5      # 90-100
    if n <= 65: return 100 - (n - 60) * 1.0     # 100-95 (peak ~50-65)
    if n <= 80: return 95 - (n - 65) * 2.5      # 95-57.5 (drop fast)
    if n <= 100: return 57 - (n - 80) * 1.5     # 57-27
    return max(10, 25 - (n - 100))


def word_count_score(words: list) -> float:
    n = len(words)
    if n <= 2: return 20
    if n <= 4: return 50 + (n - 2) * 10         # 50-70
    if n <= 9: return 80 + (9 - abs(n - 7)) * 2 # peak ~7
    if n <= 12: return 90 - (n - 9) * 5
    return max(30, 75 - (n - 12) * 5)


def has_number(title: str) -> bool:
    return bool(re.search(r"\d", title))


def power_score(words_lower: list) -> float:
    hits = sum(1 for w in words_lower if w in POWER_WORDS)
    if hits == 0: return 55
    if hits == 1: return 70
    if hits == 2: return 80
    if hits == 3: return 75
    return 60  # diminishing / spammy


def sentiment_score(words_lower: list) -> float:
    pos = sum(1 for w in words_lower if w in POSITIVE)
    neg = sum(1 for w in words_lower if w in NEGATIVE)
    polarity = pos + neg
    if polarity == 0: return 50
    if polarity == 1: return 80
    if polarity == 2: return 95
    return 85


def caps_score(title: str, words: list) -> float:
    letters = [c for c in title if c.isalpha()]
    if not letters: return 50
    upper_ratio = sum(1 for c in letters if c.isupper()) / len(letters)
    if upper_ratio > 0.6: return 20  # SHOUTING
    # Title Case-ish: most non-stopword words start uppercase
    content = [w for w in words if w.lower() not in STOPWORDS and w.isalpha()]
    if not content: return 60
    titled = sum(1 for w in content if w[0].isupper())
    ratio = titled / len(content)
    return 55 + ratio * 45  # 55-100 (lowercase not punished as hard)


def punct_score(title: str) -> float:
    score = 60
    if ":" in title: score += 15
    if "?" in title: score += 10
    if "—" in title or " - " in title: score += 5
    bangs = title.count("!")
    if bangs == 1: score += 5
    elif bangs >= 2: score -= 15
    if title.count("...") or title.count("…"): score -= 5
    return max(0, min(100, score))


def stopword_score(words_lower: list) -> float:
    if not words_lower: return 50
    ratio = sum(1 for w in words_lower if w in STOPWORDS) / len(words_lower)
    if ratio < 0.15: return 95
    if ratio < 0.3:  return 85
    if ratio < 0.45: return 70
    if ratio < 0.6:  return 50
    return 25


def specificity_score(words: list) -> float:
    if not words: return 0
    # proper-noun-ish: capitalized non-first non-stopword tokens
    proper = 0
    for i, w in enumerate(words):
        if not w or not w[0].isalpha(): continue
        if w.lower() in STOPWORDS: continue
        if w[0].isupper() and (i > 0 or len(words) > 1):
            proper += 1
    if proper == 0: return 35
    if proper == 1: return 65
    if proper == 2: return 85
    return 95


def cliche_score(title_lower: str) -> float:
    hits = sum(1 for p in CLICHE_PHRASES if p in title_lower)
    if hits == 0: return 80
    if hits == 1: return 35
    return 15


def score_title(title: str) -> dict:
    title = title.strip()
    words = re.findall(r"[A-Za-z0-9'×\-]+", title)
    words_lower = [w.lower() for w in words]

    components = {
        "length":       length_score(title),
        "word_count":   word_count_score(words),
        "number":       85 if has_number(title) else 45,
        "power":        power_score(words_lower),
        "sentiment":    sentiment_score(words_lower),
        "caps":         caps_score(title, words),
        "punct":        punct_score(title),
        "stopword":     stopword_score(words_lower),
        "specificity": specificity_score(words),
        "cliche":      cliche_score(title.lower()),
    }

    total_w = sum(WEIGHTS.values())
    weighted = sum(components[k] * WEIGHTS[k] for k in components) / total_w
    final = round(max(0, min(100, weighted)))

    return {
        "title": title,
        "score": final,
        "chars": len(title),
        "words": len(words),
        "components": {k: round(v, 1) for k, v in components.items()},
        "weights": WEIGHTS,
    }


def fmt(result: dict) -> str:
    out = [f"{result['score']}  {result['title']}"]
    out.append(f"  chars={result['chars']} words={result['words']}")
    parts = ", ".join(f"{k}={v}" for k, v in result["components"].items())
    out.append(f"  {parts}")
    return "\n".join(out)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("title", nargs="?", help="Title to score (or '-' for stdin)")
    p.add_argument("--json", action="store_true", help="JSON output")
    args = p.parse_args()

    if args.title == "-" or args.title is None:
        titles = [line.strip() for line in sys.stdin if line.strip()]
    else:
        titles = [args.title]

    results = [score_title(t) for t in titles]
    if args.json:
        print(json.dumps(results if len(results) > 1 else results[0], indent=2))
    else:
        for r in results:
            print(fmt(r))


if __name__ == "__main__":
    main()
