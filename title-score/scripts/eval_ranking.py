#!/usr/bin/env python3
"""Measure whether the model RANKS titles correctly, not just how close it gets.

Ranking is what the skill is actually used for ("which of these variants?"),
and MAE does not measure it. All numbers here come from out-of-fold
predictions, so no title is scored by a model that saw it.

Three metrics, in increasing order of how much they matter:
  1. Spearman over the whole corpus - easy, flattered by the topic spread.
  2. Pairwise accuracy over random pairs.
  3. Pairwise accuracy WITHIN a topic - the real use case, and the hard one,
     because picking between framings of your own video is exactly the
     comparison where the topic signal cancels out.

Usage: eval_ranking.py
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import calibrate as C  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data", "calibration.json")

# Topic groups for the within-topic metric. A title belongs to a group if it
# contains the group's key phrase; groups with fewer than 2 members are
# dropped. These are the topics the minimal-pair calibration batch swept.
TOPIC_KEYS = [
    "redis persistence", "webassembly", "vector database", "postgres query",
    "borrow checker", "retrieval augmented", "graphql schema", "crdt",
    "jwt", "fine-tun", "container queries", "grpc streaming",
    "garbage collection", "prompt injection", "monorepo", "sharding",
    "downtime database migration", "distributed tracing", "type inference",
    "cold start", "docker", "kubernetes", "terraform", "async await",
    "rust", "react", "kafka",
]


def out_of_fold(rows, k=6, seed=0):
    keys, nf, X, y = C.build(rows)
    lam_f, lam_g = 1.0, 30.0
    pred = np.zeros(len(y))
    order = np.random.default_rng(seed).permutation(len(y))
    for fold in np.array_split(order, k):
        m = np.ones(len(y), bool)
        m[fold] = False
        w = C.ridge(X[m], y[m], nf, lam_f, lam_g)
        pred[fold] = np.clip(X[fold] @ w, 0, 100)
    return pred, y


def spearman(a, b):
    ra = np.argsort(np.argsort(a)).astype(float)
    rb = np.argsort(np.argsort(b)).astype(float)
    ra -= ra.mean()
    rb -= rb.mean()
    return float(ra @ rb / np.sqrt((ra @ ra) * (rb @ rb)))


def pairwise(idx, pred, y, min_gap=0.0):
    """Fraction of comparable pairs the model orders correctly (ties excluded)."""
    win = tot = 0
    for i in range(len(idx)):
        for j in range(i + 1, len(idx)):
            a, b = idx[i], idx[j]
            if abs(y[a] - y[b]) <= min_gap:
                continue
            tot += 1
            win += (pred[a] - pred[b]) * (y[a] - y[b]) > 0
    return win, tot


def main():
    rows = json.load(open(DATA))
    pred, y = out_of_fold(rows)
    titles = [r["title"].lower() for r in rows]
    n = len(rows)

    print(f"n={n}  (all predictions are out-of-fold)\n")
    print(f"Spearman, whole corpus:      {spearman(pred, y):.3f}")

    w, t = pairwise(list(range(n)), pred, y)
    print(f"Pairwise, random pairs:      {w / t:.1%}  ({w}/{t})")

    w, t = pairwise(list(range(n)), pred, y, min_gap=5)
    print(f"Pairwise, gap > 5 points:    {w / t:.1%}  ({w}/{t})")

    print("\nWithin-topic (the real use case):")
    tw = tt = 0
    per_topic = []
    for key in TOPIC_KEYS:
        idx = [i for i, s in enumerate(titles) if key in s]
        if len(idx) < 2:
            continue
        w, t = pairwise(idx, pred, y)
        if t == 0:
            continue
        tw += w
        tt += t
        per_topic.append((w / t, t, key))

    for acc, t, key in sorted(per_topic):
        print(f"  {acc:5.0%}  ({t:3d} pairs)  {key}")
    print(f"\nWithin-topic overall:        {tw / tt:.1%}  ({tw}/{tt})")
    print("Coin flip would be           50.0%")


if __name__ == "__main__":
    main()
