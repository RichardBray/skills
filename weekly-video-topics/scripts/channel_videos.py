#!/usr/bin/env python3
"""Latest videos, views and likes for a YouTube channel, from its public RSS feed.

Usage: channel_videos.py [channel_id]   (default: the Firecrawl channel)
The feed only holds the 15 most recent uploads and has no comment counts.
Prints TSV: published, views, likes, likes per 1k views, title, url.
"""
import html, re, sys, urllib.request

channel = sys.argv[1] if len(sys.argv) > 1 else "UCO60vEm-6WAAtGckVqCi6Vg"
url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel}"
feed = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=30).read().decode()

print("published\tviews\tlikes\tlikes_per_1k\ttitle\turl")
for entry in re.findall(r"<entry>(.*?)</entry>", feed, re.S):
    published = re.search(r"<published>(.*?)<", entry).group(1)[:10]
    views = re.search(r'views="(\d+)"', entry)
    likes = re.search(r'starRating count="(\d+)"', entry)
    title = html.unescape(re.search(r"<title>(.*?)<", entry).group(1))
    video_id = re.search(r"<yt:videoId>(.*?)<", entry).group(1)
    v = int(views.group(1)) if views else 0
    l = int(likes.group(1)) if likes else 0
    per_1k = f"{1000 * l / v:.1f}" if v else "?"
    print(f"{published}\t{v or '?'}\t{l if likes else '?'}\t{per_1k}\t{title}\thttps://www.youtube.com/watch?v={video_id}")
