"""Linked clips that no longer line up (start or duration differ across a link group).

Usage: link_sync.py <project.beproj>
"""
import json
import sys
from collections import defaultdict

TICKS = 705_600_000
doc = json.load(open(f"{sys.argv[1]}/project.json"))
groups = defaultdict(list)
for i, track in enumerate(doc["tracks"]):
    for clip in track["clips"]:
        if clip.get("linkId"):
            groups[clip["linkId"]].append((i, clip))
bad = [(cs, link) for link, cs in groups.items()
       if len({c["start"] for _, c in cs}) > 1 or len({c["duration"] for _, c in cs}) > 1]
for cs, link in sorted(bad, key=lambda b: min(c["start"] for _, c in b[0])):
    print(link, [(f"track {i}", c["type"], round(c["start"] / TICKS, 3), round(c["duration"] / TICKS, 3)) for i, c in cs])
print(f"{len(groups)} link groups, {len(bad)} out of sync")
sys.exit(1 if bad else 0)
