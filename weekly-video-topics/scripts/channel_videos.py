#!/usr/bin/env python3
"""Latest videos and view counts for a YouTube channel, from its public RSS feed.

Usage: channel_videos.py [channel_id]   (default: the Firecrawl channel)
The feed only holds the 15 most recent uploads. Prints TSV: published, views, title, url.
"""
import html, re, sys, urllib.request

channel = sys.argv[1] if len(sys.argv) > 1 else "UCO60vEm-6WAAtGckVqCi6Vg"
url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel}"
feed = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=30).read().decode()

for entry in re.findall(r"<entry>(.*?)</entry>", feed, re.S):
    published = re.search(r"<published>(.*?)<", entry).group(1)[:10]
    views = re.search(r'views="(\d+)"', entry)
    title = html.unescape(re.search(r"<title>(.*?)<", entry).group(1))
    video_id = re.search(r"<yt:videoId>(.*?)<", entry).group(1)
    print(f"{published}\t{views.group(1) if views else '?'}\t{title}\thttps://www.youtube.com/watch?v={video_id}")
