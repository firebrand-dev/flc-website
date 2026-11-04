"""Writes the site's original background art into assets/img (deterministic: same output on every run).

  topo.svg     contour lines, like the relief of a hand-drawn map; tiles vertically behind every page
  grain.svg    a fine paper grain for the parchment notes
  favicon.svg  the FLC emblem
  seal-tested.svg / seal-review.svg   wax seals for the proof labels (green: tested in the client; amber: in review)
  leather.webp the midnight leather binding: a tileable grain for the page ground
Usage: python tools/art.py
"""
import math
import os
import random

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "assets", "img")


def blob(cx, cy, r, rng, seed_phases):
    """A closed wobbly ring: a circle with a few low-frequency harmonics, as a smooth cubic path."""
    pts = []
    n = 28
    for i in range(n):
        a = 2 * math.pi * i / n
        k = 1 + sum(amp * math.sin(f * a + ph) for f, amp, ph in seed_phases)
        pts.append((cx + r * k * math.cos(a), cy + r * k * 0.82 * math.sin(a)))
    # Catmull-Rom to Bezier
    d = [f"M{pts[0][0]:.0f} {pts[0][1]:.0f}"]
    for i in range(n):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d.append(f"C{c1[0]:.0f} {c1[1]:.0f} {c2[0]:.0f} {c2[1]:.0f} {p2[0]:.0f} {p2[1]:.0f}")
    return "".join(d) + "Z"


def topo():
    rng = random.Random(1604)
    w, h = 1400, 1800
    paths = []
    # hills: centers placed so the pattern tiles vertically without a seam (copies above and below)
    hills = [(rng.uniform(80, w - 80), rng.uniform(0, h), rng.uniform(140, 300)) for _ in range(7)]
    for cx, cy, rmax in hills:
        phases = [(f, rng.uniform(.03, .09), rng.uniform(0, 6.28)) for f in (2, 3, 5)]
        rings = int(rmax / 30)
        for j in range(1, rings + 1):
            r = rmax * j / rings
            jitter = [(f, a * (0.6 + 0.4 * j / rings), ph + j * .07) for f, a, ph in phases]
            for dy in [d for d in (-h, 0, h) if -rmax * 1.3 < cy + d < h + rmax * 1.3]:
                major = j % 4 == 0
                paths.append((blob(cx, cy + dy, r, rng, jitter), major))
    body = "".join(
        f'<path d="{d}" stroke-width="{1.1 if major else .6}" opacity="{.11 if major else .065}"/>' for d, major in paths)
    # a faint graticule, like the edge of a map sheet
    grid = "".join(f'<path d="M{x} 0V{h}" opacity=".035"/>' for x in range(0, w + 1, 175))
    grid += "".join(f'<path d="M0 {y}H{w}" opacity=".035"/>' for y in range(0, h + 1, 225))
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
           f'<g fill="none" stroke="#c9a46a">{grid}{body}</g></svg>')
    return svg


GRAIN = ('<svg xmlns="http://www.w3.org/2000/svg" width="240" height="240">'
         '<filter id="g"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="3" stitchTiles="stitch"/>'
         '<feColorMatrix values="0 0 0 0 .25  0 0 0 0 .18  0 0 0 0 .08  0 0 0 .55 0"/></filter>'
         '<rect width="240" height="240" filter="url(#g)" opacity=".5"/></svg>')

FAVICON = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48">'
           '<rect width="48" height="48" rx="10" fill="#0b1220"/>'
           '<path d="M24 6 42 24 24 42 6 24Z" fill="#121c31" stroke="#d4b16f" stroke-width="2.4"/>'
           '<path d="M17.5 31 30 18.5m0 0h-8.5m8.5 0V27" fill="none" stroke="#efe4c8" stroke-width="3.2" '
           'stroke-linecap="round" stroke-linejoin="round"/><circle cx="24" cy="24" r="2" fill="#3fbf8a"/></svg>')


def seal(fill, hi, lo, mark, seed):
    """A wax seal: an irregular poured rim, a pressed inner ring and a stamped mark. 40x40 viewBox."""
    rng = random.Random(seed)
    n = 9
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n + rng.uniform(-.18, .18)
        r = 17.4 + rng.uniform(-1.6, 1.4)
        pts.append((20 + r * math.cos(a), 20 + r * math.sin(a)))
    # a poured blob: smooth closed curve through uneven points (Catmull-Rom to Bezier)
    d = [f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"]
    for i in range(n):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d.append(f"C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}")
    d = " ".join(d) + "Z"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40">'
            f'<defs><radialGradient id="w" cx=".38" cy=".32" r=".75"><stop offset="0" stop-color="{hi}"/>'
            f'<stop offset=".55" stop-color="{fill}"/><stop offset="1" stop-color="{lo}"/></radialGradient></defs>'
            f'<path d="{d}" fill="url(#w)" stroke="{lo}" stroke-width=".8" stroke-linejoin="round"/>'
            f'<circle cx="20" cy="20" r="11.2" fill="{lo}" opacity=".28"/>'
            f'<circle cx="20" cy="20" r="11.2" fill="none" stroke="{lo}" stroke-width="2" opacity=".8"/>'
            f'<circle cx="20" cy="20" r="11.2" fill="none" stroke="{hi}" stroke-width=".8" opacity=".6" transform="translate(-.8 -.8)"/>'
            f'{mark}</svg>')


CHECK = '<path d="m14.5 20.5 4 4 7.5-8.5" fill="none" stroke="#0e2a1c" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" opacity=".85"/>'
QUESTION = ('<path d="M16.6 16.6a3.6 3.6 0 1 1 5 3.3c-1 .5-1.6 1.2-1.6 2.3v.6" fill="none" stroke="#3a2205" '
            'stroke-width="2.4" stroke-linecap="round" opacity=".85"/><circle cx="20" cy="26.4" r="1.4" fill="#3a2205" opacity=".85"/>')


def leather(path):
    """Midnight leather: low-frequency mottling plus fine pores and creases, brown-black, tileable (256 px)."""
    from PIL import Image, ImageFilter
    rng = random.Random(1604)
    size = 256
    base = Image.new("L", (size, size))
    px = base.load()
    for y in range(size):
        for x in range(size):
            px[x, y] = rng.randint(0, 255)
    fine = base.filter(ImageFilter.GaussianBlur(0.8))
    coarse = base.resize((32, 32)).resize((size, size), Image.BICUBIC).filter(ImageFilter.GaussianBlur(6))
    out = Image.new("RGB", (size, size))
    po, pf, pc = out.load(), fine.load(), coarse.load()
    for y in range(size):
        for x in range(size):
            t = (pc[x, y] - 128) * 0.10 + (pf[x, y] - 128) * 0.07
            po[x, y] = (max(0, int(16 + t)), max(0, int(13 + t * .85)), max(0, int(11 + t * .7)))
    out.save(path, "WEBP", quality=90)


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, content in (("topo.svg", topo()), ("grain.svg", GRAIN), ("favicon.svg", FAVICON)):
        with open(os.path.join(OUT, name), "w", encoding="utf-8", newline="\n") as f:
            f.write(content)
        print(f"  assets/img/{name}: {len(content) // 1024} KB")
    for name, args in (("seal-tested.svg", ("#2f8a5f", "#6fd39e", "#174a32", CHECK, 7)),
                       ("seal-review.svg", ("#c4862c", "#f2c06a", "#6e450f", QUESTION, 11))):
        with open(os.path.join(OUT, name), "w", encoding="utf-8", newline="\n") as f:
            f.write(seal(*args))
        print(f"  assets/img/{name}")
    leather(os.path.join(OUT, "leather.webp"))
    print("  assets/img/leather.webp")


if __name__ == "__main__":
    main()
