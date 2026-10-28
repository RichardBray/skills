"""Crop a 2x phone screenshot to the top half's shape (800x711 -> 1080x960 at scale 1.35).

Usage: crop_panel.py <in.png> <top_px> <out.png>
"""
import sys
from PIL import Image

src, top, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
im = Image.open(src).convert("RGB")
im.crop((0, top, 800, top + 711)).save(out)
print(out)
