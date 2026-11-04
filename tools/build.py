"""Builds the FLC website into dist/ (plain static files for any static host).

Inputs, all in this repository:
  content/site.json        versions, download, donations, reports, builds (the file to edit on a new release)
  content/*.json           features ledger, changelog, dungeon list
  i18n/<lang>.json         every text, one file per language (en is the reference)
  templates/*.html         Jinja2 pages and the shared layout
  assets/                  CSS, JS, fonts, original SVG art
  media/src/*.png          real in-game captures (tools/media.py), turned into WebP variants here

Usage:
  python tools/build.py               # build dist/
  python tools/build.py --serve       # build, then serve dist/ on the preview port (Ctrl+C to stop)
"""
import datetime as dt
import hashlib
import html
import http.server
import json
import os
import re
import shutil
import sys
from functools import partial
from urllib.parse import urlsplit

from jinja2 import Environment, FileSystemLoader, StrictUndefined
from markupsafe import Markup
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DIST = os.path.join(ROOT, "dist")
CACHE = os.path.join(ROOT, "build", "media-cache")
WIDTHS = (480, 800, 1200, 1600, 2400)

# slug -> template; slug "" is the home page. Every page exists in every language.
PAGES = [
    ("", "home.html", "home"),
    ("features", "features.html", "features"),
    ("leveling", "leveling.html", "leveling"),
    ("dungeons", "dungeons.html", "dungeons"),
    ("loot-atlas", "loot.html", "loot"),
    ("customization", "customization.html", "custom"),
    ("download", "download.html", "download"),
    ("support", "support.html", "support"),
    ("changelog", "changelog.html", "changelog"),
    ("report", "report.html", "report"),
    ("faq", "faq.html", "faq"),
    ("credits", "credits.html", "credits"),
]


def load(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return json.load(f)


class Texts:
    """Dotted lookups in one language's file. A missing key fails the build: no page ships half translated."""

    def __init__(self, lang, data):
        self.lang, self.data = lang, data

    def raw(self, key):
        node = self.data
        for part in key.split("."):
            if not isinstance(node, dict) or part not in node:
                raise KeyError(f"i18n/{self.lang}.json has no '{key}'")
            node = node[part]
        return node

    def __call__(self, key, **kw):
        value = self.raw(key)
        if isinstance(value, str):
            for k, v in kw.items():
                value = value.replace("{" + k + "}", str(v))
            return Markup(value)   # our own texts: inline <code>, <em>, <a> are intended
        return value


def keys_of(node, prefix=""):
    out = set()
    if isinstance(node, dict):
        for k, v in node.items():
            out |= keys_of(v, f"{prefix}{k}.")
    else:
        out.add(prefix[:-1])
    return out


def check_parity(langs):
    ref = keys_of(langs["en"])
    for lang, data in langs.items():
        missing, extra = ref - keys_of(data), keys_of(data) - ref
        if missing or extra:
            raise SystemExit(f"i18n/{lang}.json differs from en.json: missing {sorted(missing)[:10]} extra {sorted(extra)[:10]}")


# ---------------------------------------------------------------- media

def media_variants(manifest):
    """WebP variants of each master, cached by the master's hash. Returns id -> {w, h, srcset: [(w, file)], meta}.

    kind "ui" (addon windows): one file at the native width and WebP quality 95, never resized: narrower variants
    and lower qualities were what made their small text blurry. Lossless was measured too: 2-4 times the weight
    for no visible difference on these captures. kind "scene": quality 88, several widths."""
    os.makedirs(CACHE, exist_ok=True)
    out_dir = os.path.join(DIST, "media")
    os.makedirs(out_dir, exist_ok=True)
    info = {}
    for shot in manifest["shots"]:
        src = os.path.join(ROOT, "media", "src", shot["id"] + ".png")
        if not os.path.exists(src):
            raise SystemExit(f"media/src/{shot['id']}.png is missing: run python tools/media.py")
        with open(src, "rb") as f:
            digest = hashlib.sha256(f.read()).hexdigest()[:10]
        im = Image.open(src).convert("RGB")
        ui = shot.get("kind", "ui") == "ui"
        widths = [im.width] if ui else [w for w in WIDTHS if w < im.width] + [im.width]
        files = []
        for w in widths:
            name = f"{shot['id']}-{w}-{digest}{'-q95' if ui else ''}.webp"
            cached = os.path.join(CACHE, name)
            if not os.path.exists(cached):
                h = round(im.height * w / im.width)
                out = im if w == im.width else im.resize((w, h), Image.LANCZOS)
                out.save(cached, "WEBP", quality=95 if ui else 88, method=6)
            shutil.copy2(cached, os.path.join(out_dir, name))
            files.append((w, name))
        info[shot["id"]] = {"w": im.width, "h": im.height, "files": files, "meta": shot}
    return info


def og_image(manifest_info):
    """The social preview (1200x630): the hero capture with the night gradient. Text-free so it suits every language."""
    src = os.path.join(ROOT, "media", "src", "hero-photo.png")
    im = Image.open(src).convert("RGB")
    ratio = 1200 / 630
    w = im.width
    h = round(w / ratio)
    top = max(0, (im.height - h) // 2)
    im = im.crop((0, top, w, top + h)).resize((1200, 630), Image.LANCZOS)
    shade = Image.new("L", (1200, 630), 0)
    d = ImageDraw.Draw(shade)
    for y in range(630):
        d.line([(0, y), (1200, y)], fill=int(150 * max(0, (y - 300) / 330)))
    night = Image.new("RGB", (1200, 630), (11, 18, 32))
    im = Image.composite(night, im, shade)
    logo_path = os.path.join(ROOT, "assets", "img", "og-mark.png")
    if os.path.exists(logo_path):
        mark = Image.open(logo_path).convert("RGBA")
        im.paste(mark, (60, 630 - mark.height - 50), mark)
    out = os.path.join(DIST, "media", "og-flc.jpg")
    im.save(out, "JPEG", quality=86, optimize=True, progressive=True)
    return "media/og-flc.jpg"


# ---------------------------------------------------------------- site

def asset_hash(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()[:8]


def page_path(slug, lang, default, root=""):
    """The page's URL path. root: the site's folder when it is not served at the domain's root (GitHub Pages of a
    project repository serves https://<owner>.github.io/<repo>/), taken from site.base_url's path."""
    base = "/" if lang == default else f"/{lang}/"
    return root + base + (f"{slug}/" if slug else "")


def human_size(n):
    return f"{n / 1024 / 1024:.1f} MB" if n >= 1024 * 1024 else f"{max(1, round(n / 1024))} KB"


def fmt_date(iso, lang):
    if not iso:
        return ""
    d = dt.date.fromisoformat(iso)
    months = {
        "en": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
               "November", "December"],
        "es": ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre",
               "noviembre", "diciembre"],
    }
    names = months.get(lang, months["en"])
    if lang == "en":
        return f"{names[d.month - 1]} {d.day}, {d.year}"
    return f"{d.day} de {names[d.month - 1]} de {d.year}"


def build(serve=False, base_override=None):
    site = load("content/site.json")
    features = load("content/features.json")
    changelog = load("content/changelog.json")
    dungeons = load("content/dungeons.json")
    manifest = load("media/manifest.json")
    langs = {lang: load(f"i18n/{lang}.json") for lang in site["site"]["languages"]}
    check_parity(langs)
    default = site["site"]["default_language"]
    status_of = {f["id"]: f["status"] for g in features["groups"] for f in g["items"]}

    base_url = (base_override or site["site"]["base_url"]).rstrip("/")
    if not base_url:
        base_url = site["site"]["preview_url"].rstrip("/")
        print(f"  warning: site.base_url is empty; canonical, Open Graph and sitemap use {base_url}")

    parts = urlsplit(base_url)
    origin, root = f"{parts.scheme}://{parts.netloc}", parts.path.rstrip("/")
    os.makedirs(os.path.join(ROOT, "build"), exist_ok=True)
    with open(os.path.join(ROOT, "build", "last-build.json"), "w", encoding="utf-8") as f:
        json.dump({"base_url": base_url, "root": root}, f)

    download = site["download"]
    if download.get("enabled") and not (download.get("url") and download.get("version") and download.get("sha256")):
        raise SystemExit("download.enabled needs url, version and sha256 (run tools/sync_release.py)")
    for p in site["donations"]["platforms"]:
        url = p.get("url", "")
        if url and re.fullmatch(r"https?://(www\.)?(ko-fi\.com|cafecito\.app)/?", url):
            raise SystemExit(f"donations: {p['name']} url is the platform's home page, not the owner's page")

    if os.path.isdir(DIST):
        shutil.rmtree(DIST)
    os.makedirs(DIST)
    shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(DIST, "assets"),
                    ignore=shutil.ignore_patterns("*.md", "src"))
    shots = media_variants(manifest)
    og = og_image(shots)
    versions = {name: asset_hash(os.path.join(ROOT, "assets", sub, name))
                for sub, name in (("css", "site.css"), ("js", "site.js"))}

    env = Environment(loader=FileSystemLoader(os.path.join(ROOT, "templates")), autoescape=True,
                      undefined=StrictUndefined, trim_blocks=True, lstrip_blocks=True)
    today = dt.date.today()
    urls = []
    for slug, template, key in PAGES + [("404", "404.html", "notfound")]:
        for lang, data in langs.items():
            t = Texts(lang, data)

            def url(target, _lang=lang):
                if target.startswith(("http://", "https://", "#", "mailto:")):
                    return target
                slug_, _, frag = target.partition("#")
                path = page_path(slug_.strip("/"), _lang, default, root)
                return path + ("#" + frag if frag else "")

            def picture(shot_id, alt, sizes="100vw", cls="", eager=False, caption=None, small=None,
                        small_media="(max-width: 680px)"):
                """A capture as a lightbox link. small: another shot shown instead under small_media (art direction:
                a different real capture framed for phones, not the same one cropped by CSS)."""
                s = shots[shot_id]
                if s["meta"].get("kind", "ui") == "ui":
                    # an addon window never renders wider than its native pixels, whatever the layout asks for
                    sizes = f"(max-width: {s['w']}px) 100vw, {s['w']}px"
                srcset = ", ".join(f"{root}/media/{f} {w}w" for w, f in s["files"])
                fallback = f"{root}/media/" + s["files"][min(1, len(s["files"]) - 1)][1]
                largest = f"{root}/media/" + s["files"][-1][1]
                loading = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
                img = (f'<img src="{fallback}" srcset="{srcset}" sizes="{sizes}" width="{s["w"]}" height="{s["h"]}" '
                       f'alt="{html.escape(str(alt))}" {loading}>')
                extra = ""
                if small:
                    sm = shots[small]
                    sm_set = ", ".join(f"{root}/media/{f} {w}w" for w, f in sm["files"])
                    sm_sizes = f"(max-width: {sm['w']}px) 100vw, {sm['w']}px" if sm["meta"].get("kind", "ui") == "ui" else "100vw"
                    img = (f'<picture><source media="{small_media}" srcset="{sm_set}" sizes="{sm_sizes}" '
                           f'width="{sm["w"]}" height="{sm["h"]}">{img}</picture>')
                    extra = f' data-small="{root}/media/{sm["files"][-1][1]}" data-small-media="{small_media}"'
                kind = " shot--ui" if s["meta"].get("kind", "ui") == "ui" else ""
                return Markup(f'<a class="shot{kind} {cls}" href="{largest}" data-lightbox{extra} '
                              f'data-caption="{html.escape(str(caption or alt))}">{img}</a>')

            ctx = dict(
                t=t, lang=lang, langs=list(langs), default_lang=default, slug=slug, page_key=key,
                site=site, features=features, changelog=changelog, status_of=status_of, dungeons=dungeons, shots=shots,
                url=url, picture=picture, fmt_date=partial(fmt_date, lang=lang), human_size=human_size,
                base_url=base_url, origin=origin, root=root, og_image=f"{origin}{root}/{og}", year=today.year,
                v=versions, alternates={lg: page_path(slug, lg, default, root) for lg in langs} if slug != "404" else {},
                canonical=f"{origin}{page_path(slug, lang, default, root)}" if slug != "404" else "",
            )
            page = env.get_template(template).render(**ctx)
            if slug == "404":
                out = os.path.join(DIST, "404.html" if lang == default else os.path.join(lang, "404.html"))
            else:
                out = os.path.join(DIST, page_path(slug, lang, default).strip("/").replace("/", os.sep), "index.html")
                urls.append((slug, lang))
            os.makedirs(os.path.dirname(out), exist_ok=True)
            with open(out, "w", encoding="utf-8", newline="\n") as f:
                f.write(page)

    # sitemap with hreflang alternates, robots.txt
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for slug, lang in urls:
        lines.append(f"  <url><loc>{origin}{page_path(slug, lang, default, root)}</loc><lastmod>{site['site']['updated']}</lastmod>")
        for lg in langs:
            lines.append(f'    <xhtml:link rel="alternate" hreflang="{lg}" href="{origin}{page_path(slug, lg, default, root)}"/>')
        lines.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{origin}{page_path(slug, default, default, root)}"/>')
        lines.append("  </url>")
    lines.append("</urlset>")
    with open(os.path.join(DIST, "sitemap.xml"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
    with open(os.path.join(DIST, "robots.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write(f"User-agent: *\nAllow: /\nSitemap: {origin}{root}/sitemap.xml\n")
    # GitHub Pages reads the custom domain from a CNAME file at the site's root
    host = parts.hostname or ""
    if host and not root and not host.endswith(".github.io") and host not in ("localhost", "127.0.0.1"):
        with open(os.path.join(DIST, "CNAME"), "w", encoding="utf-8", newline="\n") as f:
            f.write(host + "\n")
    print(f"  built {len(urls)} pages in {len(langs)} languages -> {DIST}")

    if serve:
        local = parts.hostname in ("localhost", "127.0.0.1") and parts.port
        port = parts.port if local else int(site["site"]["preview_url"].rsplit(":", 1)[-1])

        class Handler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *a, **kw):
                super().__init__(*a, directory=DIST, **kw)

            def translate_path(self, path):   # serve dist/ under the site's folder, like the real host
                if root and path.startswith(root + "/"):
                    path = path[len(root):]
                elif root:
                    path = "/__outside_root__"
                return super().translate_path(path)

            def do_GET(self):
                if root and self.path in ("/", root):
                    self.send_response(302)
                    self.send_header("Location", root + "/")
                    self.end_headers()
                    return
                super().do_GET()

            def send_error(self, code, message=None, explain=None):
                if code == 404:   # behave like a static host: serve the 404 page
                    with open(os.path.join(DIST, "404.html"), "rb") as f:
                        body = f.read()
                    self.send_response(404)
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                    self.send_header("Content-Length", str(len(body)))
                    self.end_headers()
                    self.wfile.write(body)
                    return
                super().send_error(code, message, explain)

        http.server.ThreadingHTTPServer.allow_reuse_address = True
        with http.server.ThreadingHTTPServer(("127.0.0.1", port), Handler) as httpd:
            print(f"  serving http://localhost:{port}{root}/")
            httpd.serve_forever()


if __name__ == "__main__":
    override = sys.argv[sys.argv.index("--base-url") + 1] if "--base-url" in sys.argv else None
    build(serve="--serve" in sys.argv, base_override=override)
