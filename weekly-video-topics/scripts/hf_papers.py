#!/usr/bin/env python3
"""Most-upvoted Hugging Face Daily Papers over the last N days.

Usage: hf_papers.py [--days 7] [--limit 25]
Prints TSV: upvotes, github stars, date, title, arxiv url.
"""
import argparse, datetime as dt, json, urllib.request

p = argparse.ArgumentParser()
p.add_argument("--days", type=int, default=7)
p.add_argument("--limit", type=int, default=25)
args = p.parse_args()

papers = {}
today = dt.date.today()
for i in range(args.days):
    day = today - dt.timedelta(days=i)
    url = f"https://huggingface.co/api/daily_papers?date={day.isoformat()}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        entries = json.load(urllib.request.urlopen(req, timeout=30))
    except Exception:
        continue
    for e in entries:
        paper = e["paper"]
        papers[paper["id"]] = (paper.get("upvotes") or 0, paper.get("githubStars") or 0, day.isoformat(), paper["title"])

for pid, (up, stars, day, title) in sorted(papers.items(), key=lambda kv: -kv[1][0])[: args.limit]:
    print(f"{up}\t{stars}\t{day}\t{title}\thttps://arxiv.org/abs/{pid}")
