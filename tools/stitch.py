"""Joins the slices tools/shots.mjs writes for very long full-page captures (name.part0.png, name.part1.png, ...)
into name.png and deletes the slices. Usage: python tools/stitch.py build/shots/some-dir"""
import glob
import os
import re
import sys

from PIL import Image

for folder in sys.argv[1:]:
    groups = {}
    for path in glob.glob(os.path.join(folder, "*.part*.png")):
        m = re.match(r"(.*)\.part(\d+)\.png$", path)
        groups.setdefault(m.group(1), []).append((int(m.group(2)), path))
    for base, parts in groups.items():
        parts.sort()
        ims = [Image.open(p).convert("RGB") for _, p in parts]
        out = Image.new("RGB", (ims[0].width, sum(i.height for i in ims)))
        y = 0
        for im in ims:
            out.paste(im, (0, y))
            y += im.height
        out.save(base + ".png", optimize=True)
        for _, p in parts:
            os.remove(p)
        print(f"  {os.path.basename(base)}.png {out.size[0]}x{out.size[1]} from {len(parts)} slices")
