# title-score

Score a YouTube title 0-100 with a model fitted by regression against real
vidIQ title scores, for the tech / AI / developer niche.

## Installation

```sh
npx skills add https://github.com/RichardBray/skills --skill title-score
```

## Usage

```
/title-score [title to score]
```

Or run the script directly (standard library only, no dependencies):

```bash
scripts/score.py "Your Title Here"
scripts/score.py --json "Your Title Here"
printf "Title one\nTitle two\n" | scripts/score.py -
```

## How it works

A ridge regression over two blocks of features:

1. **Structural** - length, word count, digits, curiosity / narrative /
   second-person vocabulary, punctuation, caps ratio, dry academic openers,
   depth framing, conflict framing, accusation framing.
2. **Text n-grams** - word uni/bigrams plus character 3-5 grams.

The n-gram block is there because vidIQ turned out to be a learned text model
rather than a checklist: titles with identical structure but different topics
score far apart, and some topics barely move no matter how they are reframed.

Weights live in `data/model.json`; the labeled corpus is
`data/calibration.json` (~360 titles). Refit with:

```bash
uv run --with numpy python scripts/calibrate.py --write
```

## Accuracy

**This is an approximation, not the real vidIQ score.**

Held-out (K-fold) MAE is **5.3 points**, against a 7.3 baseline for always
predicting the corpus mean. On a true holdout of 12 fresh titles scored before
querying vidIQ, error was **7.3 points / 9.9% relative**.

It does not match vidIQ to within 5%, and the learning curve is flat enough
(5.74 at n=100 -> 5.21 at n=348) that more labeled data will not get it there.
Use it to **rank** title variants, which it does well: 75.8% accurate on
same-topic pairs against a 50% coin flip.

Call the vidIQ API when the absolute number matters. See **`RESEARCH.md`** for
the full reverse-engineering writeup - what vidIQ does and does not publish,
every measured finding, ranking metrics, failed approaches, and next steps.
