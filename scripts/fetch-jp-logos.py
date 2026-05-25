"""
日本SaaSロゴを各社公式サイトから取得する。

各エントリの source URL にアクセスし、ロゴSVG/PNGをスクレイピングする。
取得可能なパターン:
  1. <img class="logo|header-logo|site-logo|brand" src="...">
  2. <header>内の <img src="...">
  3. インラインSVG (<svg ...><path .../></svg>)
  4. og:image / og:logo メタタグ
  5. <link rel="icon" type="image/svg+xml">

取得結果は logos/<category>/<slug>.svg に上書き保存。
プレースホルダーから本物ロゴへ差替する。

取得失敗したものは fail.txt に slug 一覧を出力。
"""

import re
import sys
import time
import yaml
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parent.parent
LOGOS_YAML = ROOT / "logos.yaml"

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"

LOGO_HINTS = re.compile(
    r"(logo|brand|header|site-?logo|navbar-?logo|header-?logo|company-?logo)",
    re.IGNORECASE,
)


def fetch_url(url: str, timeout: int = 20) -> tuple[bytes, str] | None:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            content_type = r.headers.get("Content-Type", "")
            data = r.read()
            return data, content_type
    except urllib.error.HTTPError as e:
        print(f"      HTTP {e.code}", file=sys.stderr)
    except Exception as e:
        print(f"      ERR: {e}", file=sys.stderr)
    return None


class LogoFinder(HTMLParser):
    """ヘッダー周辺の img/svg を順位付けて収集"""

    def __init__(self, base_url: str):
        super().__init__()
        self.base_url = base_url
        self.candidates: list[tuple[int, str]] = []  # (score, abs_url)
        self.in_header = False
        self.header_depth = 0
        self.svg_buf: list[str] = []
        self.in_svg = False
        self.svg_depth = 0
        self.inline_svgs: list[tuple[int, str]] = []
        self.icons: list[tuple[int, str]] = []

    def _score(self, attrs_dict: dict, is_header: bool) -> int:
        s = 0
        if is_header:
            s += 50
        for k, v in attrs_dict.items():
            if not v:
                continue
            if k in ("class", "id", "alt", "title") and LOGO_HINTS.search(v):
                s += 30
            if k == "src" and LOGO_HINTS.search(v):
                s += 20
        return s

    def _abs(self, url: str) -> str:
        if not url:
            return ""
        if url.startswith("//"):
            return "https:" + url
        return urllib.parse.urljoin(self.base_url, url)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str]]):
        a = {k: v or "" for k, v in attrs}

        if tag in ("header", "nav"):
            self.in_header = True
            self.header_depth = 1
        elif self.in_header:
            self.header_depth += 1

        if tag == "img":
            src = a.get("src") or a.get("data-src") or ""
            if src:
                score = self._score(a, self.in_header)
                # SVG優先、PNG/WebP/JPG許容
                if src.lower().endswith(".svg") or "svg" in (a.get("type") or ""):
                    score += 100
                elif any(src.lower().endswith(ext) for ext in (".png", ".webp", ".jpg", ".jpeg")):
                    score += 10
                if score > 0:
                    self.candidates.append((score, self._abs(src)))

        if tag == "link":
            rel = a.get("rel", "").lower()
            href = a.get("href", "")
            type_ = a.get("type", "").lower()
            if href and ("icon" in rel or "logo" in rel):
                score = 5
                if "svg" in type_ or href.lower().endswith(".svg"):
                    score += 60
                self.icons.append((score, self._abs(href)))

        if tag == "meta":
            prop = (a.get("property") or a.get("name") or "").lower()
            content = a.get("content", "")
            if prop in ("og:image", "og:logo", "twitter:image") and content:
                self.candidates.append((1, self._abs(content)))

        if tag == "svg" and self.in_header:
            self.in_svg = True
            self.svg_depth = 1
            attrs_str = " ".join(f'{k}="{v}"' for k, v in attrs if v)
            self.svg_buf = [f"<svg {attrs_str}>"]
        elif self.in_svg:
            self.svg_depth += 1
            attrs_str = " ".join(f'{k}="{v}"' for k, v in attrs if v)
            self.svg_buf.append(f"<{tag} {attrs_str}>".replace("  ", " "))

    def handle_endtag(self, tag: str):
        if self.in_svg:
            self.svg_buf.append(f"</{tag}>")
            self.svg_depth -= 1
            if tag == "svg" and self.svg_depth <= 0:
                self.in_svg = False
                svg_text = "".join(self.svg_buf)
                # path/g/rect 等を含むSVGのみ採用（ただの空SVGは除外）
                if re.search(r"<(path|g|rect|circle|polygon|polyline)", svg_text):
                    self.inline_svgs.append((100, svg_text))
                self.svg_buf = []

        if self.in_header:
            self.header_depth -= 1
            if self.header_depth <= 0:
                self.in_header = False

    def handle_data(self, data: str):
        if self.in_svg:
            self.svg_buf.append(data)

    def best(self) -> tuple[str, str] | None:
        """(type, value) を返す。type は 'url' または 'inline'"""
        # 1. インラインSVG最優先
        if self.inline_svgs:
            self.inline_svgs.sort(reverse=True)
            return ("inline", self.inline_svgs[0][1])
        # 2. .svg URL 高スコア
        if self.candidates:
            self.candidates.sort(reverse=True)
            top = self.candidates[0]
            if top[0] >= 30:
                return ("url", top[1])
        # 3. アイコン
        if self.icons:
            self.icons.sort(reverse=True)
            return ("url", self.icons[0][1])
        # 4. img フォールバック
        if self.candidates:
            return ("url", self.candidates[0][1])
        return None


def normalize_svg(content: bytes, content_type: str) -> bytes | None:
    """SVGならそのまま、PNG/JPG等ならbytesを返す（拡張子は呼び出し側で判断）"""
    if not content or len(content) < 50:
        return None
    head = content[:200].decode("utf-8", errors="ignore")
    if "<svg" in head or "svg+xml" in content_type:
        return content
    if content_type.startswith("image/"):
        return content
    # 不明: HTMLとかが返ってきた場合は弾く
    return None


def fetch_logo_for(entry: dict) -> tuple[str, bytes] | None:
    """エントリ1件のロゴを取りに行く。成功なら (ext, content)、失敗ならNone"""
    source = entry.get("source")
    if not source:
        return None

    print(f"  source: {source}")
    page = fetch_url(source)
    if not page:
        return None
    html, _ct = page

    try:
        html_text = html.decode("utf-8", errors="ignore")
    except Exception:
        return None

    parser = LogoFinder(source)
    try:
        parser.feed(html_text)
    except Exception as e:
        print(f"      parse error: {e}", file=sys.stderr)

    pick = parser.best()
    if not pick:
        print(f"      no logo candidate found", file=sys.stderr)
        return None

    kind, value = pick
    if kind == "inline":
        print(f"      inline SVG found ({len(value)} chars)")
        # XMLヘッダーがなければ付ける
        if "<?xml" not in value[:50] and "xmlns" not in value[:200]:
            value = '<svg xmlns="http://www.w3.org/2000/svg" ' + value[4:]
        return ("svg", value.encode("utf-8"))
    else:
        print(f"      candidate URL: {value}")
        result = fetch_url(value)
        if not result:
            return None
        data, ct = result
        normalized = normalize_svg(data, ct)
        if not normalized:
            return None
        # 拡張子判定
        if value.lower().endswith(".svg") or "svg+xml" in ct or normalized[:200].decode("utf-8", errors="ignore").find("<svg") >= 0:
            return ("svg", normalized)
        elif value.lower().endswith(".png") or "png" in ct:
            return ("png", normalized)
        elif value.lower().endswith((".jpg", ".jpeg")) or "jpeg" in ct:
            return ("jpg", normalized)
        elif value.lower().endswith(".webp") or "webp" in ct:
            return ("webp", normalized)
        return None


def is_placeholder(filepath: Path) -> bool:
    """既存ファイルがプレースホルダーか判定"""
    if not filepath.exists():
        return True
    try:
        text = filepath.read_text(encoding="utf-8")
    except Exception:
        return False
    # プレースホルダーは generate-placeholders.py が出力する形式
    # <rect rx="32"> から始まる単純構造
    if 'rx="32"' in text and "<path" not in text and "<g " not in text:
        return True
    return False


def main():
    with LOGOS_YAML.open(encoding="utf-8") as f:
        logos = yaml.safe_load(f)

    # cc0以外（=日本SaaS等）のうちプレースホルダーになっているものを対象
    targets = []
    for entry in logos:
        if entry.get("license") == "cc0":
            continue
        if entry.get("license") == "own":
            continue
        filepath = ROOT / entry["file"]
        if is_placeholder(filepath):
            targets.append(entry)

    print(f"=== Target: {len(targets)} placeholders ===\n")

    success = 0
    fail_list = []

    for i, entry in enumerate(targets, 1):
        slug = entry["slug"]
        name = entry["name"]
        print(f"[{i}/{len(targets)}] {slug} ({name})")

        result = fetch_logo_for(entry)
        if not result:
            print(f"      FAIL\n")
            fail_list.append(f"{slug}\t{name}\t{entry.get('source', '')}")
            time.sleep(0.5)
            continue

        ext, data = result
        outpath = ROOT / entry["file"]

        # 元ファイルが .svg だが取得は .png/.webp の場合は拡張子変更
        if ext != "svg":
            new_path = outpath.with_suffix(f".{ext}")
            new_path.parent.mkdir(parents=True, exist_ok=True)
            new_path.write_bytes(data)
            # YAML側のfileパスを更新する必要があるが、今は保存だけしてログに残す
            print(f"      OK ({ext}, {len(data)} bytes) -> {new_path.relative_to(ROOT)}")
            print(f"      NOTE: file ext changed .svg -> .{ext}, update logos.yaml")
        else:
            outpath.parent.mkdir(parents=True, exist_ok=True)
            outpath.write_bytes(data)
            print(f"      OK ({ext}, {len(data)} bytes) -> {outpath.relative_to(ROOT)}")

        success += 1
        time.sleep(0.5)  # 各社サーバーに優しく

    print()
    print("=" * 60)
    print(f"  Success: {success}")
    print(f"  Fail:    {len(fail_list)}")

    if fail_list:
        fail_file = ROOT / "scripts" / "fail.txt"
        fail_file.write_text("\n".join(fail_list), encoding="utf-8")
        print(f"\n  Failed list saved to: {fail_file.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
