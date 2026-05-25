"""
Bcart アプリストア HTML を実際にパースして正しい (ID → 名前 → URL) を取得し、
slug にマッピングして再ダウンロードする。

前回 (fetch-bcart-appstore.py) は WebFetch が返したマッピング表が誤っており、
ロゴが全然違うサービスのものになってしまっていた。今回はパース自前。
"""

import re
import yaml
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOGOS_YAML = ROOT / "logos.yaml"
APPSTORE_URL = "https://app.bcart.jp/"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/130.0"

# Bcart appstore のアプリ名 → 当リポの slug マッピング
# (アプリ名は HTML の h2/h3 から抽出される正確な名前)
NAME_TO_SLUG = {
    "Paid（ペイド）":                          "paid",
    "ゆうプリR":                                "yu-print-r",
    "e飛伝Ⅲ":                                 "sagawa-e-hiden",
    "B2クラウド":                               "yamato-b2cloud",
    "Re:lation（リレーション）":                   "relation",
    "ペイパル":                                 None,  # PayPalはCC0で取得済み
    "ネクストエンジン":                            "next-engine",
    "クロネコ掛け払い":                            "kuroneko-kakebarai",
    "NP掛け払い":                               "np-kakebarai",
    "Googleアナリティクス(GA4) eコマース計測連携":     None,  # 個別ロゴなし
    "One&#039;sCloset連携":                   "onescloset",
    "TēPs（テープス）":                          "teps",
    "LTV-Lab for BtoB":                       "ltv-lab",
    "CData Drivers for Bcart":                None,  # CDataArcと統合
    "CData Arc":                              "cdata-arc",
    "PAYGENT":                                "paygent",
    "クロネコwebコレクト":                         "kuroneko-webcollect",
    "LOGILESS":                               "logiless",
    "ロジモプロ":                                "logimopro",
    "ECサーチ":                                 "ec-search",
    "logiec(ロジーク)":                          "logiec",
    "らくらく在庫":                                "rakuraku-zaiko",
    "GoQSystem":                              "goqsystem",
    "GoQ Smile":                              "goq-smile",
    "Bカート掛け払い":                            "bcart-kakebarai",
    "Bカート掛け払い 請求代行プラン":                  None,
    "Bカートクレカ決済":                           "bcart-creca",
    "うちでのこづち":                              "uchideno-kozuchi",
    "Yoom":                                   "yoom",
    "クラウドERPシステム「SmileWorks」":           "smileworks",
    "商品画像deサジェスト":                         None,  # logos.yamlに無い
    "EC レコメンダー":                            "ec-recommender",
    "Btone（ビートーン）":                         "btone",
    "キャムマックス連携":                           "cammacs",
    "クラウド販売管理システム s-flow":                "s-flow",
    "BANKING ERP":                            "banking-erp",
    "Commercerobo":                           "commercerobo",
    "CROSS MALL連携":                          "cross-mall",
    "U-KOMI":                                 "u-komi",
    "GoQSystem（ごくーシステム）":                  None,  # GoQSystem(ID44)と統合
    "テットリンク":                                "tetlink",
    "GoQSystem（ごくーシステム）在庫連携":           None,
    "ロジザードZERO連携アプリ":                     "logizard-zero",
}


def fetch_html() -> str:
    req = urllib.request.Request(APPSTORE_URL, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode("utf-8")


def parse_appstore(html: str) -> dict[int, tuple[str, str]]:
    """ID → (name, icon_url) を返す"""
    icon_urls = {}
    for m in re.finditer(
        r'href="https://app\.bcart\.jp/apps/(\d+)"\s*>\s*<img\s+src="(https://bcart-appstore\.s3[^"]+)"',
        html,
    ):
        app_id = int(m.group(1))
        icon_urls.setdefault(app_id, m.group(2))

    name_map = {}
    for m in re.finditer(r'href="https://app\.bcart\.jp/apps/(\d+)"', html):
        app_id = int(m.group(1))
        if app_id in name_map:
            continue
        chunk = html[m.end():m.end() + 2000]
        nm = re.search(r'<h[2-4][^>]*>\s*([^<]+?)\s*</h[2-4]>', chunk)
        if nm:
            name_map[app_id] = nm.group(1).strip()

    return {
        i: (name_map.get(i, "?"), icon_urls[i])
        for i in icon_urls
        if i in name_map
    }


def cleanup_old(slug: str, logos: list[dict]) -> Path | None:
    """既存の同slugファイルを全拡張子で削除し、ベースパスを返す"""
    entry = next((x for x in logos if x["slug"] == slug), None)
    if not entry:
        return None
    base = Path(entry["file"]).with_suffix("")
    for ext in (".svg", ".png", ".jpg", ".jpeg", ".webp"):
        p = ROOT / base.with_suffix(ext)
        if p.exists():
            p.unlink()
    return ROOT / base


def fetch_binary(url: str) -> tuple[bytes, str] | None:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.read(), r.headers.get("Content-Type", "")
    except Exception as e:
        print(f"  ERR: {e}")
        return None


def main():
    print("Fetching appstore HTML...")
    html = fetch_html()
    apps = parse_appstore(html)
    print(f"Parsed {len(apps)} apps\n")

    with LOGOS_YAML.open(encoding="utf-8") as f:
        logos = yaml.safe_load(f)

    success = 0
    skipped = 0
    not_in_yaml = 0

    for app_id, (name, url) in sorted(apps.items()):
        slug = NAME_TO_SLUG.get(name)
        if slug is None:
            skipped += 1
            continue

        entry = next((x for x in logos if x["slug"] == slug), None)
        if not entry:
            print(f"  [WARN] ID={app_id} name='{name}' slug='{slug}' not in logos.yaml")
            not_in_yaml += 1
            continue

        # ダウンロード
        result = fetch_binary(url)
        if not result:
            continue
        data, ct = result

        # 拡張子判定
        ext = "png"
        if url.endswith(".jpg") or url.endswith(".jpeg") or "jpeg" in ct:
            ext = "jpg"
        elif url.endswith(".svg") or "svg" in ct:
            ext = "svg"
        elif url.endswith(".png") or "png" in ct:
            ext = "png"

        base = cleanup_old(slug, logos)
        outpath = base.with_suffix(f".{ext}")
        outpath.parent.mkdir(parents=True, exist_ok=True)
        outpath.write_bytes(data)
        print(f"  ID={app_id:3d} | {name[:35]:35s} | -> {outpath.relative_to(ROOT)}")
        success += 1

    print()
    print(f"success: {success} / skipped(mapped to None): {skipped} / not in yaml: {not_in_yaml}")


if __name__ == "__main__":
    main()
