"""
CC0 ライセンスのロゴを Simple Icons + gilbarbara/logos から取得する。

logos.yaml の license=cc0 のエントリ全件をダウンロードして
file: で指定されたパスに保存する。

- gilbarbara/logos: フルカラー優先（jsDelivr CDN経由）
- Simple Icons: モノクロをカラー指定で取得（フォールバック）
"""

import os
import sys
import yaml
import urllib.request
import urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOGOS_YAML = ROOT / "logos.yaml"

# slug → Simple Icons の slug
SI_MAP = {
    "shopify": "shopify",
    "magento": "magento",
    "zapier": "zapier",
    "make": "make",
    "stripe": "stripe",
    "paypal": "paypal",
    "amazon-pay": "amazonpay",
    "microsoft-365": "microsoft365",
    "ms-teams": "microsoftteams",
    "google-workspace": "googleworkspace",
    "notion": "notion",
    "slack": "slack",
    "zoom": "zoom",
    "hubspot": "hubspot",
    "salesforce": "salesforce",
    "marketo": "marketo",
    "line": "line",
    "gmail": "gmail",
    "aws": "amazonwebservices",
    "azure": "microsoftazure",
    "gcp": "googlecloud",
    "wordpress": "wordpress",
    "tableau": "tableau",
    "amazon": "amazon",
}

# slug → gilbarbara/logos の filename (拡張子なし)
GB_MAP = {
    "shopify": "shopify",
    "stripe": "stripe",
    "paypal": "paypal",
    "aws": "aws",
    "gcp": "google-cloud",
    "azure": "azure",
    "slack": "slack-icon",
    "zoom": "zoom",
    "hubspot": "hubspot",
    "salesforce": "salesforce",
    "wordpress": "wordpress-icon",
    "notion": "notion",
    "tableau": "tableau-icon",
    "zapier": "zapier-icon",
    "make": "make-icon",
    "line": "line",
    "gmail": "gmail-icon",
    "magento": "magento",
    "marketo": "marketo-icon",
    "amazon-pay": "amazon-pay",
    "amazon": "amazon",
    "microsoft-365": "microsoft",
    "ms-teams": "microsoft-teams",
    "google-workspace": "google",
}

USER_AGENT = "Mozilla/5.0 (saas-logos fetcher; +https://github.com/craval-inc/cv-iconpack)"


def fetch(url: str, timeout: int = 15) -> bytes | None:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = r.read()
            if data and len(data) > 50:
                return data
    except urllib.error.HTTPError as e:
        print(f"    HTTP {e.code}: {url}")
    except Exception as e:
        print(f"    ERROR: {e}")
    return None


def save(content: bytes, outpath: Path) -> None:
    outpath.parent.mkdir(parents=True, exist_ok=True)
    outpath.write_bytes(content)


def main():
    with LOGOS_YAML.open(encoding="utf-8") as f:
        logos = yaml.safe_load(f)

    cc0 = [x for x in logos if x.get("license") == "cc0"]
    print(f"CC0 logos: {len(cc0)}")
    print()

    gb_ok = si_ok = fail = 0

    for i, entry in enumerate(cc0, 1):
        slug = entry["slug"]
        color = entry["color"].lstrip("#")
        outpath = ROOT / entry["file"]

        print(f"[{i:2d}/{len(cc0)}] {slug}")

        # 1. gilbarbara をまず試す
        gb_slug = GB_MAP.get(slug)
        if gb_slug:
            url = f"https://cdn.jsdelivr.net/gh/gilbarbara/logos@main/logos/{gb_slug}.svg"
            data = fetch(url)
            if data:
                save(data, outpath)
                gb_ok += 1
                print(f"    GB OK: {outpath.relative_to(ROOT)}")
                continue

        # 2. Simple Icons フォールバック
        si_slug = SI_MAP.get(slug)
        if si_slug:
            url = f"https://cdn.simpleicons.org/{si_slug}/{color}"
            data = fetch(url)
            if data:
                save(data, outpath)
                si_ok += 1
                print(f"    SI OK: {outpath.relative_to(ROOT)}")
                continue

        print(f"    FAIL")
        fail += 1

    print()
    print("=" * 50)
    print(f"  gilbarbara (color):  {gb_ok}")
    print(f"  Simple Icons (mono): {si_ok}")
    print(f"  FAIL:                {fail}")


if __name__ == "__main__":
    main()
