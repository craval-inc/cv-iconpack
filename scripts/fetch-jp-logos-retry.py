"""
fetch-jp-logos.py で取れなかったロゴを再取得する。

戦略:
  1. source URL のドメインルートに対し、よくあるロゴパスを試す:
       /logo.svg, /assets/logo.svg, /img/logo.svg, /images/logo.svg,
       /static/logo.svg, /favicon.svg, /apple-touch-icon.png
  2. プレス/会社情報ページを試す:
       /press/, /press-kit/, /brand/, /logo/, /about/, /company/,
       /material/, /asset/, /resource/, /download/
  3. それらのページに対しても再度 LogoFinder を走らせる

fail.txt から対象を読み込み、成功したら本物のSVG/PNGを保存する。
"""

import sys
import time
import yaml
import urllib.request
import urllib.parse
import urllib.error
import re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from importlib import import_module
fjl = import_module("fetch-jp-logos")

ROOT = Path(__file__).resolve().parent.parent
LOGOS_YAML = ROOT / "logos.yaml"
FAIL_LIST = ROOT / "scripts" / "fail.txt"

# 直リンクで試すパス
DIRECT_PATHS = [
    "logo.svg",
    "assets/logo.svg",
    "assets/img/logo.svg",
    "assets/images/logo.svg",
    "img/logo.svg",
    "images/logo.svg",
    "static/logo.svg",
    "static/img/logo.svg",
    "common/img/logo.svg",
    "img/common/logo.svg",
    "wp-content/themes/logo.svg",
    "favicon.svg",
]

# 探索するページ
SEARCH_PAGES = [
    "press/",
    "press-kit/",
    "brand/",
    "logo/",
    "about/",
    "about/logo/",
    "about/brand/",
    "company/",
    "company/logo/",
    "company/brand/",
    "material/",
    "asset/",
    "assets/",
    "resource/",
    "download/",
    "service/",
    "products/",
]


def try_direct(source_url: str) -> tuple[str, bytes] | None:
    """ドメインルート直下のロゴ候補パスを順に試す"""
    parsed = urllib.parse.urlparse(source_url)
    base = f"{parsed.scheme}://{parsed.netloc}/"

    for path in DIRECT_PATHS:
        url = base + path
        result = fjl.fetch_url(url, timeout=8)
        if not result:
            continue
        data, ct = result
        norm = fjl.normalize_svg(data, ct)
        if not norm or len(norm) < 200:
            continue

        # 拡張子判定
        if url.endswith(".svg") or "svg" in ct:
            print(f"      DIRECT OK: {url}")
            return ("svg", norm)
        elif url.endswith(".png") or "png" in ct:
            print(f"      DIRECT OK: {url}")
            return ("png", norm)
    return None


def try_subpages(source_url: str) -> tuple[str, bytes] | None:
    """about/press/brand 系サブページを巡回して logo を見つける"""
    parsed = urllib.parse.urlparse(source_url)
    base = f"{parsed.scheme}://{parsed.netloc}/"

    for sub in SEARCH_PAGES:
        url = base + sub
        result = fjl.fetch_url(url, timeout=8)
        if not result:
            continue
        html, _ = result
        try:
            html_text = html.decode("utf-8", errors="ignore")
        except Exception:
            continue

        # ページ内に "logo" を含む img/svg があるか軽くチェック
        if "logo" not in html_text.lower():
            continue

        parser = fjl.LogoFinder(url)
        try:
            parser.feed(html_text)
        except Exception:
            continue

        pick = parser.best()
        if not pick:
            continue
        kind, value = pick

        if kind == "inline":
            print(f"      SUBPAGE OK ({sub}): inline SVG")
            return ("svg", value.encode("utf-8"))
        else:
            res2 = fjl.fetch_url(value, timeout=8)
            if not res2:
                continue
            data, ct = res2
            norm = fjl.normalize_svg(data, ct)
            if not norm or len(norm) < 200:
                continue
            ext = "svg" if (value.endswith(".svg") or "svg" in ct) else ("png" if "png" in ct else "jpg")
            print(f"      SUBPAGE OK ({sub}): {value}")
            return (ext, norm)
    return None


def main():
    if not FAIL_LIST.exists():
        print("fail.txt が見つからない。fetch-jp-logos.py を先に実行してください")
        return

    fails = [line.strip().split("\t") for line in FAIL_LIST.read_text(encoding="utf-8").splitlines() if line.strip()]

    with LOGOS_YAML.open(encoding="utf-8") as f:
        logos = yaml.safe_load(f)
    by_slug = {x["slug"]: x for x in logos}

    print(f"=== Retry: {len(fails)} entries ===\n")

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

        # 試行1: 直リンク
        result = try_direct(source)
        # 試行2: サブページ巡回
        if not result:
            result = try_subpages(source)

        if not result:
            print(f"      STILL FAIL\n")
            still_fail.append(f"{slug}\t{name}\t{source}")
            time.sleep(0.3)
            continue

        ext, data = result
        # 元のYAMLパスの拡張子部分を実際の拡張子に置換
        base = Path(entry["file"]).with_suffix("")
        outpath = ROOT / base.with_suffix(f".{ext}")
        outpath.parent.mkdir(parents=True, exist_ok=True)
        # プレースホルダーがあれば削除
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
        print(f"\n  Updated fail.txt with {len(still_fail)} entries")


if __name__ == "__main__":
    main()
