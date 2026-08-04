# Reverse-engineering vidIQ's title score

Findings from building this skill. Everything here was measured against the
real `vidiq_score_title` MCP tool or sourced from vidIQ's own documentation.
Kept out of `SKILL.md` so it does not burn context on every invocation.

Corpus: `data/calibration.json`, 360 tech / AI / developer titles with real
vidIQ scores.

## What vidIQ publishes about the title score

**Almost nothing.** There is no help-center article, blog post, or changelog
describing factors, weights, or architecture. What exists:

- Range and framing: "vidIQ will automatically provide a **Title Score**
  (ranging from 1 to 100)... indicates how well your title is optimized in
  real-time." <https://support.vidiq.com/en/articles/10099905-title-suggestions>
- Colour bands: 0-40 red, 41-80 yellow, 81-100 green.
  <https://support.vidiq.com/en/articles/8972670-optimize>
- CTR-framed, not SEO-framed: "our AI rates it out of 100... Click-through rate
  is one of the strongest signals on YouTube."
  <https://vidiq.com/youtube-title-analyzer/>
- The score-explainer page vidIQ itself links to, `/en/articles/10106652-optimize-score`,
  is a dead 404.

**Do not confuse it with the vidIQ SEO Score**, which *is* documented (tag
count, tag volume, keyword usage, 50% actionable / 50% performance, channel
size matters). That decomposition belongs to the SEO score. Conflating the two
is the most common error in third-party writeups.

vidIQ has never stated that the title score is an ML model trained on CTR data,
never described training data, and never named a factor. Third-party claims
that it is ("Opus.pro") cite no source. No genuine reverse-engineering writeup
exists publicly.

**Safe to say publicly:** it is a 0-100 AI score for click-through potential,
it distinguishes long-form from Shorts, it optionally sharpens with channel
context, and it is colour-banded 0-40 / 41-80 / 81-100.
**Not safe to say:** that it is trained on CTR data, or what its factors are.

### One published feature vocabulary worth stealing

vidIQ's title *suggestion* feature exposes an "Emotion" selector with a fixed
set: None, Comparison, Credibility, Curiosity, Desire, Extreme, List,
Negativity, Question, Time. Not documented as scorer inputs, but it is the
closest thing vidIQ publishes to a native vocabulary for titles. Encoding these
nine as features (on the theory the generator and scorer share a feature space)
improved every metric slightly - see the ablation table below.

## Measured behaviour

- **Deterministic.** The same title returns the same score on repeat calls.
  Note that creators anecdotally report inconsistency; repeated measurement here
  did not reproduce that.
- **It rewards clickbait rather than punishing it.** `Stop Using React` = 74,
  `STOP USING REACT!!! THIS IS INSANE` = 89. The first version of this skill
  penalized caps and exclamation marks. That was backwards.
- **"For beginners" helps.** `Kubernetes Tutorial` = 64,
  `Kubernetes Tutorial for Beginners` = 77. The first version treated it as a
  cliche penalty. Also backwards.
- **Framing beats phrasing polish.** Minimal pairs with the topic held fixed:
  `Redis Persistence` 72 / `Redis Persistence Explained` 74 /
  `Your Redis Persistence Config Is Wrong` 92. Appending "Explained" is close to
  a no-op and sometimes negative (`gRPC Streaming` 52 ->
  `gRPC Streaming Explained` 50). Second-person accusation and first-person
  result framing are what move the number.
- **Dry academic openers appear to hurt - weakly evidenced.**
  `Webpack Configuration Options` = 76 ->
  `Understanding Webpack Configuration Options` = 67. But only 29 within-topic
  pairs vary on this feature and a within-topic estimator flips its sign. The
  pair is real; the generalization is not established.
- **It is a learned text model, not a checklist.** This is the central finding.
  Structurally identical titles about different topics score far apart, and some
  topics are pinned almost regardless of framing:
  `Async Await in JavaScript` = 56, `Understanding Async Await in JavaScript`
  = 56, and even `Why Async Await Is Quietly Ruining Your JavaScript` = 56 -
  while `Terraform Modules` = 73.
- **It is not keyword search volume.** The obvious explanation for that gap,
  ruled out: `async await javascript` and `terraform modules` have near-identical
  vidIQ keyword metrics (overall 65.0 vs 65.1) yet title scores of 56 vs 73. The
  gap lives in the text model, not in demand data.
- **Observed range roughly 41-96.** Nothing in 360 dev-niche titles landed in
  the red band. Treat "below 50" as effectively the floor.

## Accuracy

Held-out (K-fold) MAE on the 360-title corpus, each row adding to the previous:

| model | held-out MAE |
| --- | --- |
| always predict the corpus mean (baseline) | 7.31 |
| hand features only | 6.73 |
| \+ word n-grams | 6.12 |
| \+ char 3-5 grams | 5.32 |
| \+ vidIQ emotion taxonomy (current) | **5.24** |

**True holdout:** 12 fresh titles scored by the model *before* querying vidIQ
came out at **MAE 7.33, mean relative error 9.9%, 2/12 inside 5%**.
Cross-validated MAE is therefore optimistic. Treat ~7 points as the realistic
error on a genuinely new title.

In-sample MAE is ~2.0 and is meaningless here - the n-gram block memorizes
training titles. Only held-out numbers are reported as headline figures.

### Ranking (the metric that matches actual use)

From `scripts/eval_ranking.py`, all predictions out-of-fold:

| metric | result | chance |
| --- | --- | --- |
| Spearman, whole corpus | 0.632 | 0 |
| pairwise, random pairs | 74.1% | 50% |
| pairwise, pairs differing by >5 points | 81.2% | 50% |
| **pairwise, within one topic** | **75.8%** | 50% |

Within-topic accuracy matching random-pair accuracy is the meaningful part: the
model is not merely riding topic signal to look good.

### Why 5% is not reachable this way

The learning curve is flat. Held-out MAE by corpus size: 5.74 at n=100, 5.37 at
n=180, 5.33 at n=260, 5.21 at n=348. Extrapolating, even ~1000 labeled titles
lands near 5 points (~7%), not the ~3.8 that 5% requires.

Hand features are saturated too: the three framing features derived from
minimal-pair testing moved held-out MAE by 0.03.

Closing the gap needs a better text representation (sentence embeddings), not
more n-grams and not more rows.

## Things that were tried and did not work

Don't rebuild these without new evidence.

- **Topic anchor + framing delta.** Decompose the score into a per-topic base
  plus a framing adjustment, fitting framing weights on within-topic pairwise
  differences so the topic effect cancels exactly. Well motivated by the
  minimal-pair data, and it lost: out-of-fold MAE 5.68 vs 5.32, Spearman 0.522
  vs 0.622, pairwise 69.1% vs 73.6%. Within-topic was a tie (74.6% vs 73.7%,
  inside noise). The character n-grams already infer topic at a far finer grain
  than a bucketed anchor can.
- **Keyword search volume as a feature.** Ruled out by measurement above.

## Methodological notes

- **Within-topic estimator.** Fitting on pairwise differences within a topic
  cancels the topic effect exactly, giving unconfounded framing coefficients. It
  disagrees with the global fit on the sign of `dry`, `colon`, and `bang` - but
  those have only 29, 17, and 14 supporting pairs, so neither estimate is
  trustworthy there. `narrative` and `curiosity` also flip, with 118 and 113
  pairs, which is better supported and suggests the global fit understates both.
  Useful as a diagnostic even though it failed as a predictor.
- **Dual ridge solve.** ~7000 n-gram columns against ~360 titles, so the fitter
  scales the hand-feature block and solves the n x n dual system instead of the
  p x p primal. `scripts/calibrate.py --demo` checks this against a naive primal
  solve in both regimes.
- **Minimal pairs are credit-efficient.** Each pair isolates one factor with the
  topic cancelled, and yielded far more signal per credit than random sampling.

## Corpus limits (bounds what any of this can be trusted for)

- **Long-form only.** `type` is required and `long` / `short` score differently.
  Every row was collected with `type="long"`. Shorts needs its own corpus.
- **No channel context.** `channelId` / `videoId` are optional and documented as
  improving accuracy; every row omitted them. So this approximates vidIQ's
  *generic* scorer, not the score for a specific channel.
- **It can go stale.** vidIQ does not version or changelog the scorer. If they
  retrain, the corpus silently becomes wrong.

## Highest-value next steps

1. **Rebuild the corpus with a real `channelId`.** Same credit cost, correct
   target. Independently supported by the one published study using real CTR
   labels (Paskalev, ~15k videos), which found title conventions are
   genre-specific and models should be trained within a vertical.
   <https://georgepaskalev.medium.com/can-you-predict-a-youtube-videos-ctr-using-machine-learning-bc20bb142a47>
2. **Active learning.** Generate ~50k candidates offline, query vidIQ only on
   the most-uncertain (bootstrap-ridge disagreement). Typically 2-5x more
   credit-efficient than the random sampling used here.
3. **Sentence embeddings + more data, together.** Past ~2000 rows, embeddings
   plus gradient boosting or a fine-tuned small transformer becomes the right
   student model. Either upgrade alone underdelivers.

Realistic ceiling estimate with paid credits and embeddings: ~4-5 points
(~6%). Sub-5% is not promised.

## Credits

vidIQ scoring costs 5 credits per call. The plan used here renews 2000
credits monthly.
