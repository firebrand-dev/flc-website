"""Crops the real in-game captures listed in media/manifest.json into media/src/<id>.png.

The sources live in the addon's repository and its test reports; they are only read. The masters in media/src are
what the site uses, so the site builds without the addon's folders. Usage:
    python tools/media.py            # every shot
    python tools/media.py boss-card  # only these ids
    python tools/media.py --sheet    # also writes build/media-sheet.jpg to review them together
"""
import json
import os
import sys

from PIL import Image, ImageDraw

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MANIFEST = os.path.join(ROOT, "media", "manifest.json")
OUT = os.path.join(ROOT, "media", "src")


def resolve(src, roots):
    key, _, rel = src.partition(":")
    return os.path.join(roots[key], rel)


def main(argv):
    with open(MANIFEST, encoding="utf-8") as f:
        manifest = json.load(f)
    only = {a for a in argv if not a.startswith("--")}
    os.makedirs(OUT, exist_ok=True)
    done = []
    for shot in manifest["shots"]:
        if only and shot["id"] not in only:
            continue
        path = resolve(shot["src"], manifest["roots"])
        if not os.path.exists(path):
            print(f"  missing source for {shot['id']}: {path} (keeping the existing master)")
            continue
        im = Image.open(path).convert("RGB").crop(tuple(shot["box"]))
        dest = os.path.join(OUT, shot["id"] + ".png")
        im.save(dest, optimize=True)
        done.append((shot["id"], im))
        print(f"  {shot['id']}: {im.size[0]}x{im.size[1]}")
    if "--sheet" in argv and done:
        w = 620
        thumbs = []
        for name, im in done:
            t = im.resize((w, max(1, int(im.height * w / im.width))))
            ImageDraw.Draw(t).text((4, 2), name, fill=(255, 255, 0))
            thumbs.append(t)
        cols = 3
        rows = (len(thumbs) + cols - 1) // cols
        rh = [max(t.height for t in thumbs[r * cols:(r + 1) * cols]) for r in range(rows)]
        sheet = Image.new("RGB", (cols * w, sum(rh)), (30, 30, 30))
        y = 0
        for r in range(rows):
            for c, t in enumerate(thumbs[r * cols:(r + 1) * cols]):
                sheet.paste(t, (c * w, y))
            y += rh[r]
        os.makedirs(os.path.join(ROOT, "build"), exist_ok=True)
        sheet.save(os.path.join(ROOT, "build", "media-sheet.jpg"), quality=80)
        print("  sheet: build/media-sheet.jpg")


if __name__ == "__main__":
    main(sys.argv[1:])
