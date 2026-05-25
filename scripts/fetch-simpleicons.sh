#!/bin/bash
# Simple Icons (CC0) / gilbarbara (フルカラー) から取得する
# 出力: logos.yaml の license=cc0 のロゴをローカルファイルとして保存
#
# 使い方:
#   bash scripts/fetch-simpleicons.sh
#
# 依存: curl, python (yaml)

set -e
cd "$(dirname "$0")/.."

# Simple Icons CDN は color指定可: https://cdn.simpleicons.org/<slug>/<hex_without_hash>
# gilbarbara/logos jsDelivr: https://cdn.jsdelivr.net/gh/gilbarbara/logos@main/logos/<name>.svg

# slug → Simple Icons slug マッピング（必要なものだけ）
declare -A SI_MAP=(
  [shopify]=shopify
  [magento]=magento
  [zapier]=zapier
  [make]=make
  [stripe]=stripe
  [paypal]=paypal
  [amazon-pay]=amazonpay
  [microsoft-365]=microsoft365
  [ms-teams]=microsoftteams
  [google-workspace]=googleworkspace
  [notion]=notion
  [slack]=slack
  [zoom]=zoom
  [hubspot]=hubspot
  [salesforce]=salesforce
  [marketo]=marketo
  [line]=line
  [gmail]=gmail
  [aws]=amazonwebservices
  [azure]=microsoftazure
  [gcp]=googlecloud
  [wordpress]=wordpress
  [tableau]=tableau
  [amazon]=amazon
)

# gilbarbara にあるフルカラーロゴ
declare -A GB_MAP=(
  [shopify]=shopify
  [stripe]=stripe
  [paypal]=paypal
  [aws]=aws
  [gcp]=google-cloud
  [azure]=azure
  [slack]=slack-icon
  [zoom]=zoom
  [hubspot]=hubspot
  [salesforce]=salesforce
  [wordpress]=wordpress-icon
  [notion]=notion
  [tableau]=tableau-icon
  [zapier]=zapier-icon
  [make]=make-icon
  [line]=line
  [gmail]=gmail-icon
  [magento]=magento
  [marketo]=marketo-icon
)

fetch_si() {
  local slug=$1
  local si_slug=$2
  local color=$3
  local outfile=$4

  local hex="${color#\#}"
  local url="https://cdn.simpleicons.org/${si_slug}/${hex}"

  mkdir -p "$(dirname "$outfile")"
  if curl -sfL "$url" -o "$outfile.tmp" && [ -s "$outfile.tmp" ]; then
    mv "$outfile.tmp" "$outfile"
    echo "  [SI] $slug -> $outfile"
    return 0
  else
    rm -f "$outfile.tmp"
    return 1
  fi
}

fetch_gb() {
  local slug=$1
  local gb_slug=$2
  local outfile=$3

  local url="https://cdn.jsdelivr.net/gh/gilbarbara/logos@main/logos/${gb_slug}.svg"

  mkdir -p "$(dirname "$outfile")"
  if curl -sfL "$url" -o "$outfile.tmp" && [ -s "$outfile.tmp" ]; then
    mv "$outfile.tmp" "$outfile"
    echo "  [GB] $slug -> $outfile"
    return 0
  else
    rm -f "$outfile.tmp"
    return 1
  fi
}

# logos.yaml から license=cc0 のエントリを取り出す
python <<'PY' > /tmp/cc0-list.txt
import yaml
with open('logos.yaml', 'r', encoding='utf-8') as f:
    data = yaml.safe_load(f)
for x in data:
    if x.get('license') == 'cc0':
        print(f"{x['slug']}\t{x['color']}\t{x['file']}")
PY

echo "=== Fetching CC0 logos (Simple Icons monochrome + gilbarbara color) ==="
echo ""

total=0
si_ok=0
gb_ok=0
fail=0

while IFS=$'\t' read -r slug color file; do
  total=$((total+1))
  echo "[$total] $slug ($color)"

  # gilbarbara をまず試す（フルカラー優先）
  gb_slug="${GB_MAP[$slug]:-}"
  if [ -n "$gb_slug" ]; then
    if fetch_gb "$slug" "$gb_slug" "$file"; then
      gb_ok=$((gb_ok+1))
      continue
    fi
  fi

  # フォールバックで Simple Icons（モノクロ + カラー指定）
  si_slug="${SI_MAP[$slug]:-}"
  if [ -n "$si_slug" ]; then
    if fetch_si "$slug" "$si_slug" "$color" "$file"; then
      si_ok=$((si_ok+1))
      continue
    fi
  fi

  echo "  [FAIL] $slug"
  fail=$((fail+1))
done < /tmp/cc0-list.txt

echo ""
echo "=== Result ==="
echo "  Total CC0: $total"
echo "  gilbarbara (color):  $gb_ok"
echo "  simpleicons (mono):  $si_ok"
echo "  FAIL:                $fail"

rm -f /tmp/cc0-list.txt
