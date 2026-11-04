"""Checks the built site in dist/: run after tools/build.py.

  - every internal link and asset resolves to a file in dist/
  - every external link answers (with --external; GitHub can rate-limit, so it is opt-in)
  - every <img> has an alt, ids are unique, each page has exactly one <h1> and a lang
  - the colour pairs the design uses for text meet WCAG AA contrast
  - nothing links to a donation platform's home page, and no donation link exists while site.json has none
Usage: python tools/check.py [--external]
"""
import json
import os
import re
import sys
import urllib.error
import urllib.request
from html.parser import HTMLParser

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DIST = os.path.join(ROOT, "dist")


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.imgs, self.ids, self.h1, self.lang = [], [], [], 0, None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.lang = a.get("lang")
        if tag == "h1":
            self.h1 += 1
        if "id" in a:
            self.ids.append(a["id"])
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag in ("link", "script") and (a.get("href") or a.get("src")):
            if a.get("rel") not in ("canonical", "alternate"):
                self.links.append(a.get("href") or a.get("src"))
        if tag == "img":
            self.imgs.append(a)
            if a.get("src"):
                self.links.append(a["src"])
            for part in (a.get("srcset") or "").split(","):
                if part.strip():
                    self.links.append(part.strip().split()[0])


def site_root():
    try:
        with open(os.path.join(ROOT, "build", "last-build.json"), encoding="utf-8") as f:
            return json.load(f).get("root", "")
    except OSError:
        return ""


SITE_ROOT = site_root()


def resolve(href):
    path = href.split("#")[0].split("?")[0]
    if not path:
        return True
    if SITE_ROOT and path.startswith("/"):
        if not path.startswith(SITE_ROOT + "/"):
            return False   # a root-relative link that would leave the site's folder
        path = path[len(SITE_ROOT):]
    full = os.path.join(DIST, path.lstrip("/").replace("/", os.sep))
    return os.path.isfile(full) or os.path.isfile(os.path.join(full, "index.html"))


def luminance(hex_):
    rgb = [int(hex_[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    rgb = [c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4 for c in rgb]
    return .2126 * rgb[0] + .7152 * rgb[1] + .0722 * rgb[2]


def contrast(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + .05) / (lb + .05)


def main():
    problems, external = [], set()
    pages = 0
    for dirpath, _, files in os.walk(DIST):
        for name in files:
            if not name.endswith(".html"):
                continue
            pages += 1
            path = os.path.join(dirpath, name)
            rel = os.path.relpath(path, DIST)
            p = Page()
            with open(path, encoding="utf-8") as f:
                p.feed(f.read())
            if p.h1 != 1:
                problems.append(f"{rel}: {p.h1} <h1>")
            if not p.lang:
                problems.append(f"{rel}: no lang")
            dup = {i for i in p.ids if p.ids.count(i) > 1}
            if dup:
                problems.append(f"{rel}: duplicate ids {sorted(dup)}")
            for img in p.imgs:
                if "alt" not in img:
                    problems.append(f"{rel}: <img> without alt ({img.get('src')})")
            for href in p.links:
                if href.startswith(("http://", "https://")):
                    if "localhost" not in href:
                        external.add(href)
                elif href.startswith(("mailto:", "#", "data:")):
                    continue
                elif not resolve(href):
                    problems.append(f"{rel}: broken link {href}")

    # donation links: never a platform's home page; none at all while site.json has none
    site = json.load(open(os.path.join(ROOT, "content", "site.json"), encoding="utf-8"))
    configured = {p["url"] for p in site["donations"]["platforms"] if p.get("url")}
    for href in external:
        if re.match(r"https?://(www\.)?(ko-fi\.com|cafecito\.app|ayudar\.ar|paypal\.(com|me))", href) and href not in configured:
            problems.append(f"donation link not in site.json: {href}")

    # text colour pairs used by the design (foreground, background)
    pairs = {
        "body text": ("#ece4d0", "#0b1220"), "secondary text": ("#c9c1ae", "#0b1220"),
        "muted text": ("#9a937f", "#0b1220"), "muted on panel": ("#9a937f", "#121c31"),
        "bronze link": ("#d4b16f", "#0b1220"), "parchment text": ("#2b2317", "#ddd0b0"),
        "parchment link": ("#6b3f12", "#ddd0b0"), "button text": ("#1c1408", "#b68d4f"),
        "review badge": ("#f2c779", "#121c31"), "client badge": ("#8fe3bd", "#121c31"),
        "emerald": ("#3fbf8a", "#0b1220"), "amber": ("#e4ad4f", "#0b1220"),
    }
    for label, (fg, bg) in pairs.items():
        ratio = contrast(fg, bg)
        if ratio < 4.5:
            problems.append(f"contrast {label}: {ratio:.2f} < 4.5")

    if "--external" in sys.argv:
        for href in sorted(external):
            req = urllib.request.Request(href, method="GET", headers={"User-Agent": "flc-site-check"})
            try:
                with urllib.request.urlopen(req, timeout=15) as r:
                    status = r.status
            except urllib.error.HTTPError as e:
                status = e.code
            except Exception as e:  # noqa: BLE001
                status = type(e).__name__
            ok = status == 200
            print(f"  {'ok ' if ok else 'BAD'} {status} {href}")
            if not ok:
                problems.append(f"external link {href}: {status}")

    print(f"  {pages} pages, {len(external)} external links")
    for p in problems:
        print("  PROBLEM", p)
    if problems:
        raise SystemExit(1)
    print("  all checks passed")


if __name__ == "__main__":
    main()
