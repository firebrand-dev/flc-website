"""Writes the site's original background art into assets/img (deterministic: same output on every run).

  topo.svg     contour lines, like the relief of a hand-drawn map; tiles vertically behind every page
  grain.svg    a fine paper grain for the parchment notes
  favicon.svg  the FLC emblem
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


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, content in (("topo.svg", topo()), ("grain.svg", GRAIN), ("favicon.svg", FAVICON)):
        with open(os.path.join(OUT, name), "w", encoding="utf-8", newline="\n") as f:
            f.write(content)
        print(f"  assets/img/{name}: {len(content) // 1024} KB")


if __name__ == "__main__":
    main()
