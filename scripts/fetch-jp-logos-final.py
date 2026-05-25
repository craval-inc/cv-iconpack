"""
fetch-jp-logos-retry.py で取れなかった分の最終取得。

戦略:
  1. ページ内の <link rel="apple-touch-icon">, <link rel="icon"> を試す
  2. og:image / twitter:image を試す
  3. ドメインの /favicon.ico, /apple-touch-icon.png, /apple-touch-icon-precomposed.png
  4. それでもダメなら別の慣用パス: /img/header_logo.png, /assets/images/header/logo.png 等

ロゴ画質よりも「何かしら本物の画像が取れる」ことを優先。
PNG/ICO/JPGも許容（YAMLの file: 拡張子は sync-extensions.py で後から同期）。
"""

import sys
import time
import yaml
import re
import urllib.request
import urllib.parse
from pathlib import Path
from html.parser import HTMLParser

sys.path.insert(0, str(Path(__file__).resolve().parent))
from importlib import import_module
fjl = import_module("fetch-jp-logos")

ROOT = Path(__file__).resolve().parent.parent
LOGOS_YAML = ROOT / "logos.yaml"
FAIL_LIST = ROOT / "scripts" / "fail.txt"


EXTRA_PATHS = [
    "apple-touch-icon.png",
    "apple-touch-icon-precomposed.png",
    "favicon.ico",
    "img/header_logo.png",
    "img/header/logo.png",
    "img/common/header_logo.png",
    "assets/images/logo.png",
    "assets/images/header/logo.png",
    "assets/images/common/logo.png",
    "images/header/logo.png",
    "images/common/logo.png",
    "common/images/logo.png",
    "shared/images/logo.png",
]


class MetaParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.og_image = None
        self.tw_image = None
        self.icons: list[str] = []
        self.apple = None

    def handle_starttag(self, tag, attrs):
        a = {k: v or "" for k, v in attrs}
        if tag == "meta":
            prop = (a.get("property") or a.get("name") or "").lower()
            content = a.get("content")
            if prop == "og:image" and content:
                self.og_image = content
            elif prop in ("twitter:image", "twitter:image:src") and content:
                self.tw_image = content
        elif tag == "link":
            rel = a.get("rel", "").lower()
            href = a.get("href")
            if not href:
                return
            if "apple-touch-icon" in rel:
                self.apple = href
            elif "icon" in rel:
                self.icons.append(href)


def try_meta(source_url: str) -> tuple[str, bytes] | None:
    page = fjl.fetch_url(source_url, timeout=10)
    if not page:
        return None
    html, _ = page
    try:
        text = html.decode("utf-8", errors="ignore")
    except Exception:
        return None

    parser = MetaParser()
    try:
        parser.feed(text)
    except Exception:
        pass

    candidates: list[str] = []
    if parser.apple:
        candidates.append(parser.apple)
    if parser.og_image:
        candidates.append(parser.og_image)
    if parser.tw_image:
        candidates.append(parser.tw_image)
    candidates.extend(parser.icons)

    for c in candidates:
        url = urllib.parse.urljoin(source_url, c)
        result = fjl.fetch_url(url, timeout=8)
        if not result:
            continue
        data, ct = result
        norm = fjl.normalize_svg(data, ct)
        if not norm or len(norm) < 200:
            continue
        ext = (
            "svg" if (url.endswith(".svg") or "svg" in ct)
            else "png" if (url.endswith(".png") or "png" in ct)
            else "ico" if (url.endswith(".ico") or "icon" in ct)
            else "jpg" if "jpeg" in ct
            else "webp" if "webp" in ct
            else None
        )
        if ext:
            print(f"      META OK: {url}")
            return (ext, norm)
    return None


def try_extra_paths(source_url: str) -> tuple[str, bytes] | None:
    parsed = urllib.parse.urlparse(source_url)
    base = f"{parsed.scheme}://{parsed.netloc}/"
    for path in EXTRA_PATHS:
        url = base + path
        result = fjl.fetch_url(url, timeout=6)
        if not result:
            continue
        data, ct = result
        norm = fjl.normalize_svg(data, ct)
        if not norm or len(norm) < 200:
            continue
        ext = (
            "svg" if (url.endswith(".svg") or "svg" in ct)
            else "png" if (url.endswith(".png") or "png" in ct)
            else "ico" if (url.endswith(".ico") or "icon" in ct)
            else None
        )
        if ext:
            print(f"      EXTRA OK: {url}")
            return (ext, norm)
    return None


def main():
    fails = [line.strip().split("\t") for line in FAIL_LIST.read_text(encoding="utf-8").splitlines() if line.strip()]
    with LOGOS_YAML.open(encoding="utf-8") as f:
        logos = yaml.safe_load(f)
    by_slug = {x["slug"]: x for x in logos}

    print(f"=== Final attempt: {len(fails)} entries ===\n")
    success = 0
    still_fail = []

    for i, parts in enumerate(fails, 1):
        if len(parts) < 3:
            continue
        slug, name, source = parts[0], parts[1], parts[2]
        entry = by_slug.get(slug)
        if not entry:
            continue

        print(f"[{i}/{len(fails)}] {slug} ({name})")
        print(f"  source: {source}")

        result = try_meta(source)
        if not result:
            result = try_extra_paths(source)

        if not result:
            print(f"      STILL FAIL\n")
            still_fail.append(f"{slug}\t{name}\t{source}")
            time.sleep(0.3)
            continue

        ext, data = result
        base = Path(entry["file"]).with_suffix("")
        outpath = ROOT / base.with_suffix(f".{ext}")
        outpath.parent.mkdir(parents=True, exist_ok=True)
        old = ROOT / entry["file"]
        if old.exists() and old != outpath:
            old.unlink()
        outpath.write_bytes(data)
        print(f"      SAVED: {outpath.relative_to(ROOT)} ({len(data)} bytes)\n")
        success += 1
        time.sleep(0.3)

    print("=" * 60)
    print(f"  Success: {success}")
    print(f"  Still fail: {len(still_fail)}")
    if still_fail:
        FAIL_LIST.write_text("\n".join(still_fail), encoding="utf-8")


if __name__ == "__main__":
    main()
