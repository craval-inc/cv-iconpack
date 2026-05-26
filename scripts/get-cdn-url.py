"""logos.yaml から slug → 正しい CDN URL を返す簡易ヘルパ。

使い方:
  python scripts/get-cdn-url.py bcart kintone ec-connector
"""
import sys
import yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
with (ROOT / "logos.yaml").open(encoding="utf-8") as f:
    logos = yaml.safe_load(f)
by_slug = {x["slug"]: x for x in logos}

CDN = "https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main"

for slug in sys.argv[1:]:
    entry = by_slug.get(slug)
    if not entry:
        print(f"{slug}\tNOT_FOUND")
        continue
    print(f"{slug}\t{CDN}/{entry['file'].replace(chr(92), '/')}")
