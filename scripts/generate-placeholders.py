"""
ロゴ未取得のサービス用にプレースホルダーSVGを生成する。

ブランドカラーの角丸長方形 + 中央にサービス名（適応サイズ）。
後から本物のロゴSVGに上書き差し替え可能。

ファイルが既に存在する場合はスキップ（本物ロゴを保護）。
"""

from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
LOGOS_YAML = ROOT / "logos.yaml"

# 1200x630 のOGPサイズ感ではなく、240x240 の正方形（D2 image shape向け）
W, H = 240, 240


def luminance(hex_color: str) -> float:
    """背景色の明度から文字色（白 or 黒）を決定"""
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16) / 255
    g = int(hex_color[2:4], 16) / 255
    b = int(hex_color[4:6], 16) / 255
    return 0.299 * r + 0.587 * g + 0.114 * b


def text_color_for(bg_hex: str) -> str:
    return "#000000" if luminance(bg_hex) > 0.6 else "#FFFFFF"


def fit_font_size(text: str, max_width: int = 220, base: int = 38) -> int:
    """テキスト長から font-size を見積もる（日本語1.0文字幅、英数字0.55文字幅）"""
    char_w_full = 1.0
    char_w_half = 0.55
    total = sum(char_w_full if ord(c) > 0x7F else char_w_half for c in text)
    # base*total ≒ width
    if total == 0:
        return base
    size = min(base, int(max_width / total))
    return max(12, size)


def wrap_text(text: str, max_chars: int = 8) -> list[str]:
    """日本語サービス名を2行に折り返す。簡易ルール: 半角換算で max_chars * 2"""
    width = 0
    line = ""
    lines = []
    limit = max_chars * 2  # 半角換算
    for ch in text:
        w = 2 if ord(ch) > 0x7F else 1
        if width + w > limit and line:
            lines.append(line)
            line = ch
            width = w
        else:
            line += ch
            width += w
    if line:
        lines.append(line)
    return lines[:3]  # 最大3行


def make_svg(name: str, color: str) -> str:
    fg = text_color_for(color)
    # 適応的サイズ計算: 折り返し後の最長行で決定
    lines = wrap_text(name, max_chars=7)
    longest = max(lines, key=lambda l: sum(2 if ord(c) > 0x7F else 1 for c in l))
    font_size = fit_font_size(longest, max_width=200, base=36)

    line_h = int(font_size * 1.3)
    total_h = line_h * len(lines)
    start_y = (H - total_h) / 2 + font_size * 0.85  # baselineに合わせる

    tspans = []
    for i, line in enumerate(lines):
        y = start_y + i * line_h
        # XMLエスケープ
        esc = (
            line.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
        )
        tspans.append(
            f'<text x="{W/2}" y="{y:.1f}" text-anchor="middle" '
            f'font-family="-apple-system, BlinkMacSystemFont, &quot;Hiragino Sans&quot;, '
            f'&quot;Yu Gothic&quot;, &quot;Meiryo&quot;, sans-serif" '
            f'font-size="{font_size}" font-weight="700" fill="{fg}">{esc}</text>'
        )

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'width="{W}" height="{H}">'
        f'<rect width="{W}" height="{H}" rx="32" fill="{color}"/>'
        f"{''.join(tspans)}"
        f"</svg>"
    )


def main():
    with LOGOS_YAML.open(encoding="utf-8") as f:
        logos = yaml.safe_load(f)

    created = skipped = 0

    for entry in logos:
        out = ROOT / entry["file"]
        if out.exists():
            skipped += 1
            continue

        out.parent.mkdir(parents=True, exist_ok=True)
        svg = make_svg(entry["name"], entry["color"])
        out.write_text(svg, encoding="utf-8")
        created += 1
        print(f"  + {out.relative_to(ROOT)}")

    print()
    print(f"created: {created}")
    print(f"skipped (already exists): {skipped}")
    print(f"total in yaml: {len(logos)}")


if __name__ == "__main__":
    main()
