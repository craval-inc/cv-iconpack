"""
Bcart アプリストア (https://app.bcart.jp/) から、各公式アプリのアイコン画像を一括取得する。

これにより、各社公式サイトから取れなかった Bcart連携系のロゴ
(Btone/キャムマックス/s-flow/TēPs/テットリンク/Yoom/Commercerobo/logiec/
ロジモプロ/LTV-Lab/ECサーチ/ECレコメンダー/One'sCloset/CDataDrivers) が取れる。
"""

import yaml
import urllib.request
import urllib.error
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOGOS_YAML = ROOT / "logos.yaml"

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"

# Bcart アプリストアから抽出した URL マップ (slug → アイコンURL)
APP_LOGOS = {
    "tetlink":      "https://bcart-appstore.s3.ap-northeast-1.amazonaws.com/73/icon_image/t7Yk4NfbBek6nASluuAjpKlxyhm7hwOYp5of3vjN.png",
    "btone":        "https://bcart-appstore.s3.ap-northeast-1.amazonaws.com/59/icon_image/zzvyWbB2AUpVGiqbp5mBP0jmkxHA7zAS55vywnPe.png",
    "cammacs":      "https://bcart-appstore.s3.ap-northeast-1.amazonaws.com/60/icon_image/nhTqK3ilFw6kTtW2MTvPIOkUwJ3OTIAwCl92CQGM.png",
    "s-flow":       "https://bcart-appstore.s3.ap-northeast-1.amazonaws.com/62/icon_image/a1wz9u5We3FOiyub7ZlVqs9ihyjBLLbq8FZBYCe2.png",
    "teps":         "https://bcart-appstore.s3.ap-northeast-1.amazonaws.com/22/icon_image/IWGdoj2jqvQxQDId1T3m8fzp9TFECK4bc1czOq1H.png",
    "onescloset":   "https://bcart-appstore.s3.ap-northeast-1.amazonaws.com/21/icon_image/a7kS85pof62WvcI0LMAk8CxdruCtE18PwpCCxBdO.png",
    "ltv-lab":      "https://bcart-appstore.s3.ap-northeast-1.amazonaws.com/30/icon_image/Kl2bnJvmOiCmRfWOLEDySGZo0c6Bntx5c380lnHB.png",
    "commercerobo": "https://bcart-appstore.s3.ap-northeast-1.amazonaws.com/66/icon_image/b3AqT0SUKI59LrWO1ljJo21j8u53yWUcVzpALUUL.png",
    "logimopro":    "https://bcart-appstore.s3.ap-northeast-1.amazonaws.com/39/icon_image/GOSEQPPuLosOAPCZB1DUMT8ZwRdoxBNP5zL0C07U.png",
    "logiec":       "https://bcart-appstore.s3.ap-northeast-1.amazonaws.com/43/icon_image/TWzlpZOd7CCAwNkb8OtX0d2vKUkjviFQAGLim2lC.png",
    "ec-search":    "https://bcart-appstore.s3.ap-northeast-1.amazonaws.com/42/icon_image/ZWiHyA6fg2oHKPoGaMCxmaAD91H726KA6bMUaqJh.png",
    "ec-recommender": "https://bcart-appstore.s3.ap-northeast-1.amazonaws.com/10/icon_image/bs3WCTYA8HJUH1nZ3ujMEfB8QkfbxYSwOVft6Hc8.png",
    # 既存差替: ECコネクターは前回間違ったロゴ取った可能性高い (multivendor.svg)
    "ec-connector": "https://bcart-appstore.s3.ap-northeast-1.amazonaws.com/19/icon_image/sZnKzaQ4vaaS2Jhp0edoiSC6dpyhV59j0XsiPLjj.jpg",
    # Yoomも前回 provider-Google を取ってしまったので差替
    "yoom":         "https://bcart-appstore.s3.ap-northeast-1.amazonaws.com/55/icon_image/q1HzVrHoo3dcxfRFvh53KfhIrYSlZvTL9jK3Yqrw.png",
    # うちでのこづちも差替 (webp の代わりに公式PNGに)
    "uchideno-kozuchi": "https://bcart-appstore.s3.ap-northeast-1.amazonaws.com/57/icon_image/ZIH3IS4pSX32OTJr2H4hd9xBgCFWCWB5aS8SeCtw.jpg",
}


def fetch(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.read(), r.headers.get("Content-Type", "")
    except Exception as e:
        print(f"  ERROR: {e}")
        return None, None


def main():
    with LOGOS_YAML.open(encoding="utf-8") as f:
        logos = yaml.safe_load(f)
    by_slug = {x["slug"]: x for x in logos}

    success = 0
    fail = 0

    for slug, url in APP_LOGOS.items():
        entry = by_slug.get(slug)
        if not entry:
            print(f"[SKIP] {slug}: not in logos.yaml")
            continue

        print(f"[{slug}] {url}")
        data, ct = fetch(url)
        if not data or len(data) < 200:
            print(f"  FAIL")
            fail += 1
            continue

        # 拡張子推定
        if url.endswith(".png") or "png" in ct:
            ext = "png"
        elif url.endswith(".jpg") or url.endswith(".jpeg") or "jpeg" in ct:
            ext = "jpg"
        elif url.endswith(".svg") or "svg" in ct:
            ext = "svg"
        else:
            ext = "png"  # フォールバック

        base = Path(entry["file"]).with_suffix("")
        outpath = ROOT / base.with_suffix(f".{ext}")
        outpath.parent.mkdir(parents=True, exist_ok=True)

        # 既存ファイルがあれば削除（拡張子違いも含めて）
        for old_ext in (".svg", ".png", ".jpg", ".jpeg", ".webp"):
            old = ROOT / base.with_suffix(old_ext)
            if old.exists() and old != outpath:
                old.unlink()

        outpath.write_bytes(data)
        print(f"  OK -> {outpath.relative_to(ROOT)} ({len(data)} bytes)")
        success += 1
        time.sleep(0.3)

    print()
    print(f"Success: {success} / Fail: {fail}")


if __name__ == "__main__":
    main()
