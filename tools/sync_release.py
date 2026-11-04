"""Fills content/site.json's "download" block from a real release. It never publishes and never turns the download on.

Two sources, both read-only:
  --from-folder <dir>   a frozen release folder of the addon repo (dist/releases/<version>/ with release.json and
                        SHA256SUMS.txt). Gives version, file, size and sha256; the url stays empty until a public
                        GitHub Release exists.
  --from-github         the latest public GitHub Release of site.json's repos.releases (no login, public API).
                        Gives version, date, the asset's url and size, and the sha256 from its SHA256SUMS.txt asset.

Then review the diff of content/site.json and, only when the owner authorizes the release, set download.enabled to
true and rebuild. Usage:
  python tools/sync_release.py --from-folder E:/Firebrand/FoLeCom-integration/dist/releases/0.8.0-rc3-pre-setup
  python tools/sync_release.py --from-github
"""
import hashlib
import json
import os
import sys
import urllib.error
import urllib.request

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SITE = os.path.join(ROOT, "content", "site.json")


def save(site):
    with open(SITE, "w", encoding="utf-8", newline="\n") as f:
        json.dump(site, f, indent=2, ensure_ascii=False)
        f.write("\n")


def pick_zip(names):
    """The player's single download: FLC-<version>.zip (addon + catalog) if present, else the addon zip."""
    bundles = [n for n in names if n.startswith("FLC-") and n.endswith(".zip")]
    addon = [n for n in names if n.startswith("ForeverLevelingCompanion-") and n.endswith(".zip")]
    return (bundles or addon or [None])[0]


def from_folder(folder, site):
    with open(os.path.join(folder, "release.json"), encoding="utf-8") as f:
        rel = json.load(f)
    name = pick_zip(rel.get("zips", os.listdir(folder)))
    if not name:
        raise SystemExit("no FLC zip in that folder")
    path = os.path.join(folder, name)
    with open(path, "rb") as f:
        sha = hashlib.sha256(f.read()).hexdigest()
    sums = os.path.join(folder, "SHA256SUMS.txt")
    if os.path.exists(sums):
        listed = {line.split()[1]: line.split()[0] for line in open(sums, encoding="utf-8") if line.strip()}
        if listed.get(name) and listed[name] != sha:
            raise SystemExit(f"{name}: computed sha256 differs from SHA256SUMS.txt")
    d = site["download"]
    d.update(version=rel["version"], file=name, size_bytes=os.path.getsize(path), sha256=sha,
             date=rel.get("frozen_at", "")[:10])
    print(f"  {name}: {d['size_bytes']} bytes, sha256 {sha[:16]}..., version {d['version']}")
    print("  url and release_page stay as they are: set them from the public GitHub Release (--from-github).")


def from_github(site):
    repo = site["repos"]["releases"]
    api = f"https://api.github.com/repos/{repo}/releases/latest"
    try:
        with urllib.request.urlopen(urllib.request.Request(api, headers={"User-Agent": "flc-site"}), timeout=20) as r:
            rel = json.load(r)
    except urllib.error.HTTPError as e:
        raise SystemExit(f"{api}: HTTP {e.code} (no public release yet, or the repository is private)")
    assets = {a["name"]: a for a in rel.get("assets", [])}
    name = pick_zip(list(assets))
    if not name:
        raise SystemExit("the latest release has no FLC zip asset")
    sha = ""
    if "SHA256SUMS.txt" in assets:
        with urllib.request.urlopen(assets["SHA256SUMS.txt"]["browser_download_url"], timeout=20) as r:
            for line in r.read().decode("utf-8").splitlines():
                parts = line.split()
                if len(parts) == 2 and parts[1] == name:
                    sha = parts[0]
    d = site["download"]
    d.update(version=rel["tag_name"].lstrip("v"), file=name, url=assets[name]["browser_download_url"],
             release_page=rel["html_url"], size_bytes=assets[name]["size"], sha256=sha,
             date=(rel.get("published_at") or "")[:10],
             checksums_url=assets.get("SHA256SUMS.txt", {}).get("browser_download_url", ""))
    print(f"  {name} from {rel['html_url']}" + ("" if sha else "  (no SHA256SUMS.txt asset: add one)"))


def main(argv):
    with open(SITE, encoding="utf-8") as f:
        site = json.load(f)
    if "--from-folder" in argv:
        from_folder(argv[argv.index("--from-folder") + 1], site)
    elif "--from-github" in argv:
        from_github(site)
    else:
        raise SystemExit(__doc__)
    save(site)
    print(f"  content/site.json updated; download.enabled is still {site['download']['enabled']}")


if __name__ == "__main__":
    main(sys.argv[1:])
