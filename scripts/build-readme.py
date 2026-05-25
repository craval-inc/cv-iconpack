"""
README.md を logos.yaml から再生成する。

logos.yaml を変更した後 or プレースホルダーを差し替えた後に実行。
"""

import yaml
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent

CAT_LABELS = {
    "ec-platform":      "BtoB/BtoC ECプラットフォーム",
    "sales-management": "販売管理ソフト",
    "erp-bcart-app":    "Bカート公式ERP/販売管理アプリ",
    "eai":              "EAI / データ連携 / ノーコード自動化",
    "inventory-wms":    "在庫管理・WMS",
    "pos":              "POS・レジ",
    "payment":          "決済",
    "logistics":        "物流・送り状発行",
    "groupware":        "グループウェア・コミュニケーション基盤",
    "crm-ma":           "CRM / MA / SFA",
    "backoffice":       "会計・労務",
    "communication":    "コミュニケーション（顧客対応）",
    "review-tool":      "レビュー・サイト内検索・売上UP",
    "dev":              "開発基盤・データ",
    "jp-mall":          "国内モール / SaaSカート",
    "craval":           "自社",
}


def is_real_logo(filepath: Path) -> bool:
    """プレースホルダー以外（=本物ロゴ）かどうか判定"""
    if not filepath.exists():
        return False
    # 非SVG（PNG/JPG/WebP）は全て本物扱い
    if filepath.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp"):
        return True
    if filepath.suffix.lower() != ".svg":
        return False
    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception:
        return False
    if "<path" in content or "<g " in content:
        return True
    # プレースホルダーは <rect rx="32"> + <text> のみ
    return False


def main():
    with (ROOT / "logos.yaml").open(encoding="utf-8") as f:
        logos = yaml.safe_load(f)

    by_cat: dict[str, list] = defaultdict(list)
    for x in logos:
        by_cat[x["category"]].append(x)

    md: list[str] = []
    md.append("# cv-iconpack")
    md.append("")
    md.append("株式会社CravalのBtoB ECメディア・営業資料・図解で使うSVGアセット集（社内用）。")
    md.append("")
    md.append("## 使い方")
    md.append("")
    md.append("### CDN直リンク（推奨）")
    md.append("")
    md.append("jsDelivr経由でGitHubから直接配信される。バージョン固定するなら `@main` を `@<commit-sha>` に変更。")
    md.append("")
    md.append("```")
    md.append("https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/<category>/<slug>.svg")
    md.append("```")
    md.append("")
    md.append("### D2 での参照例")
    md.append("")
    md.append("```d2")
    md.append("bcart: Bカート {")
    md.append("  shape: image")
    md.append("  icon: https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/ec-platform/bcart.svg")
    md.append("}")
    md.append("kintone: kintone {")
    md.append("  shape: image")
    md.append("  icon: https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/groupware/kintone.svg")
    md.append("}")
    md.append("bcart -> kintone: API連携")
    md.append("```")
    md.append("")
    md.append("### HTML での参照例")
    md.append("")
    md.append("```html")
    md.append('<img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/payment/stripe.svg" alt="Stripe" width="64">')
    md.append("```")
    md.append("")
    md.append("## メタデータ")
    md.append("")
    md.append("`logos.yaml` に全ロゴのメタ情報あり。slug / 提供会社 / カテゴリ / ブランドカラー / 公式URL / プレスキットURL / ライセンス区分。")
    md.append("")
    md.append("## ライセンス")
    md.append("")
    md.append("- メタデータ・スクリプト: MIT (株式会社Craval)")
    md.append("- ロゴ画像: 各社の商標。公正使用の範囲で利用 (詳細は [LICENSE](./LICENSE) 参照)")
    md.append("")

    # 収集状況
    total = len(logos)
    got_real = 0
    for x in logos:
        f = ROOT / x["file"]
        if is_real_logo(f):
            got_real += 1
    placeholder = total - got_real

    md.append("## ロゴ収集状況")
    md.append("")
    md.append(f"- 合計: **{total}社**")
    md.append(f"- 本物ロゴ取得済: {got_real}社（Simple Icons / gilbarbara/logos / 公式DL）")
    md.append(f"- プレースホルダー: {placeholder}社（ブランドカラー + 社名テキスト、後日プレスキットから差替予定）")
    md.append("")
    md.append("プレースホルダーでも D2 や HTML から参照可能。差替時はファイル名を変えず上書き保存するだけで CDN にも反映される（jsDelivr キャッシュは最大12時間）。")
    md.append("")

    md.append("## カテゴリ別一覧")
    md.append("")

    for cat in CAT_LABELS:
        if cat not in by_cat:
            continue
        items = sorted(by_cat[cat], key=lambda x: x["slug"])
        md.append(f"### {CAT_LABELS[cat]} ({len(items)})")
        md.append("")
        md.append("| slug | 名称 | 提供会社 | カラー | プレビュー |")
        md.append("|------|------|---------|--------|----------|")
        for x in items:
            slug = x["slug"]
            name = x["name"]
            vendor = x.get("vendor", "-")
            color = x["color"]
            url = f"https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/{x['file'].replace(chr(92), '/')}"
            md.append(f'| `{slug}` | {name} | {vendor} | `{color}` | <img src="{url}" width="40"> |')
        md.append("")

    md.append("## ロゴ追加・差替の運用")
    md.append("")
    md.append("### 新しいサービスを追加する")
    md.append("")
    md.append("1. `logos.yaml` にエントリ追加（slug/name/category/vendor/color/source/license/file）")
    md.append("2. `logos/<category>/<slug>.svg` にロゴを配置（本物 or プレースホルダー）")
    md.append("3. `python scripts/generate-placeholders.py` で未配置ロゴのプレースホルダーを一括生成")
    md.append("4. `python scripts/build-readme.py` で README 再生成")
    md.append("5. commit & push")
    md.append("")
    md.append("### プレースホルダーを本物ロゴに差替える")
    md.append("")
    md.append("1. 各社プレスキット (`logos.yaml` の `press_kit` 参照) からSVGをDL")
    md.append("2. 既存ファイルを上書き（ファイル名は変えない）")
    md.append("3. commit & push → jsDelivr CDNに最大12時間で反映")
    md.append("")
    md.append("### 関連リポジトリ")
    md.append("")
    md.append("- [craval-inc/craval-site-renewal](https://github.com/craval-inc/craval-site-renewal): BtoB ECメディア本体")
    md.append("- [craval-inc/article-tool](https://github.com/craval-inc/article-tool): 記事生成ツール")

    (ROOT / "README.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"README.md generated: {len(md)} lines")
    print(f"  total: {total}, real: {got_real}, placeholder: {placeholder}")


if __name__ == "__main__":
    main()
