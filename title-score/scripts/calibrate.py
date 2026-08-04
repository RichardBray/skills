#!/usr/bin/env python3
"""Fit data/model.json from data/calibration.json (titles -> real vidIQ scores).

Ridge regression over the hand features in score.py plus word uni/bigrams.
The two blocks get separate ridge strengths: hand features are few and trusted,
n-grams are many and noisy, so they are penalized far harder. Both strengths
are picked by K-fold CV on held-out titles, which is the number that matters --
in-sample error can always be driven to zero by memorizing the vocabulary.

Usage: calibrate.py            -> report only
       calibrate.py --write    -> also write data/model.json
"""
import argparse
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from score import features, ngrams  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data", "calibration.json")
MODEL = os.path.join(HERE, "..", "data", "model.json")

MIN_DF = 2  # ignore n-grams seen in only one title -- pure memorization


def build(rows):
    feat_keys = sorted(features(rows[0]["title"]))

    df = {}
    for r in rows:
        for k in ngrams(r["title"]):
            df[k] = df.get(k, 0) + 1
    gram_keys = sorted(k for k, c in df.items() if c >= MIN_DF)

    keys = feat_keys + gram_keys
    idx = {k: i for i, k in enumerate(keys)}
    X = np.zeros((len(rows), len(keys) + 1))
    X[:, -1] = 1.0  # intercept
    for i, r in enumerate(rows):
        for k, v in features(r["title"]).items():
            X[i, idx[k]] = v
        for k in ngrams(r["title"]):
            if k in idx:
                X[i, idx[k]] = 1.0
    y = np.array([float(r["vidiq"]) for r in rows])
    return keys, len(feat_keys), X, y


def ridge(X, y, n_feat, lam_f, lam_g):
    """Two-block ridge, solved in whichever space is smaller.

    There are far more n-gram columns than titles, so the primal p x p solve is
    the slow way round. Scaling the hand-feature block by sqrt(lam_g/lam_f)
    makes a single ridge strength lam_g equivalent to the two-block penalty,
    which then admits the dual n x n solve. The intercept is handled by
    centering rather than by a penalized column.
    """
    s = np.sqrt(lam_g / lam_f)
    Xs = X[:, :-1].copy()
    Xs[:, :n_feat] *= s

    mu, ybar = Xs.mean(0), y.mean()
    Xc, yc = Xs - mu, y - ybar

    n, p = Xc.shape
    if p <= n:
        w = np.linalg.solve(Xc.T @ Xc + lam_g * np.eye(p), Xc.T @ yc)
    else:
        w = Xc.T @ np.linalg.solve(Xc @ Xc.T + lam_g * np.eye(n), yc)

    b = ybar - mu @ w        # intercept, computed in the scaled space
    w[:n_feat] *= s          # then undo the scaling for the raw features
    return np.append(w, b)


def kfold_mae(X, y, n_feat, lam_f, lam_g, k=6, seed=0):
    rng = np.random.default_rng(seed)
    order = rng.permutation(len(y))
    errs = []
    for fold in np.array_split(order, k):
        m = np.ones(len(y), bool)
        m[fold] = False
        w = ridge(X[m], y[m], n_feat, lam_f, lam_g)
        errs.extend(np.abs(np.clip(X[fold] @ w, 0, 100) - y[fold]))
    return float(np.mean(errs))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    rows = json.load(open(DATA))
    keys, n_feat, X, y = build(rows)

    grid = [(lf, lg)
            for lf in (0.1, 0.3, 1.0, 3.0)
            for lg in (3.0, 10.0, 30.0, 100.0, 300.0)]
    lam_f, lam_g = min(grid, key=lambda p: kfold_mae(X, y, n_feat, *p))
    cv = kfold_mae(X, y, n_feat, lam_f, lam_g)

    w = ridge(X, y, n_feat, lam_f, lam_g)
    pred = np.clip(X @ w, 0, 100)
    err = np.abs(pred - y)

    print(f"n={len(y)} features={n_feat} ngrams={len(keys) - n_feat} "
          f"lambda_feat={lam_f} lambda_ngram={lam_g}")
    print(f"in-sample  MAE={err.mean():.2f} max={err.max():.1f} "
          f"within-5%={100 * np.mean(err <= 0.05 * y):.0f}%")
    base = float(np.mean(np.abs(y - y.mean())))
    print(f"held-out   MAE={cv:.2f}   <-- the honest number")
    print(f"baseline   MAE={base:.2f}   (always predict the corpus mean)")
    print("\nworst in-sample:")
    for r, p, e in sorted(zip(rows, pred, err), key=lambda t: -t[2])[:8]:
        print(f"  {e:5.1f}  ours={p:5.1f} vidiq={r['vidiq']:3d}  {r['title'][:58]}")

    if args.write:
        model = {
            "intercept": round(float(w[-1]), 4),
            "coef": {k: round(float(v), 4)
                     for k, v in zip(keys, w[:-1]) if abs(v) > 1e-4},
            "n_train": len(y),
            "cv_mae": round(cv, 2),
            "lambda": [lam_f, lam_g],
        }
        json.dump(model, open(MODEL, "w"), indent=1, sort_keys=True)
        print(f"\nwrote {MODEL}")


def demo():
    """Self-check for ridge(): the dual/scaling path is easy to get subtly wrong.

    Checked against a naive primal solve with an explicit penalty matrix, in
    both the p<=n and p>n regimes, with lam_f != lam_g so the block scaling is
    actually exercised.
    """
    def naive(X, y, n_feat, lam_f, lam_g):
        Xa = np.hstack([X[:, :-1], np.ones((len(X), 1))])
        p = np.zeros(Xa.shape[1])
        p[:n_feat] = lam_f
        p[n_feat:-1] = lam_g
        return np.linalg.solve(Xa.T @ Xa + np.diag(p), Xa.T @ y)

    rng = np.random.default_rng(0)
    for n, p in ((40, 12), (12, 40)):
        X = np.hstack([rng.normal(size=(n, p)), np.ones((n, 1))])
        y = rng.normal(size=n) * 10 + 70
        got = ridge(X, y, 4, 0.7, 9.0)
        want = naive(X, y, 4, 0.7, 9.0)
        assert np.allclose(got, want, atol=1e-6), (n, p, np.abs(got - want).max())

    # Shrinkage sanity: huge penalty collapses to predicting the mean.
    X = np.hstack([rng.normal(size=(20, 5)), np.ones((20, 1))])
    y = rng.normal(size=20) + 70
    w = ridge(X, y, 2, 1e9, 1e9)
    assert np.allclose(w[:-1], 0, atol=1e-4) and abs(w[-1] - y.mean()) < 1e-3
    print("demo ok")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo()
    else:
        main()
