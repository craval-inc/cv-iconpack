# cv-iconpack

株式会社CravalのBtoB ECメディア・営業資料・図解で使うSVGアセット集（社内用）。

## 使い方

### CDN直リンク（推奨）

jsDelivr経由でGitHubから直接配信される。バージョン固定するなら `@main` を `@<commit-sha>` に変更。

```
https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/<category>/<slug>.svg
```

### D2 での参照例

```d2
bcart: Bカート {
  shape: image
  icon: https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/ec-platform/bcart.svg
}
kintone: kintone {
  shape: image
  icon: https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/groupware/kintone.svg
}
bcart -> kintone: API連携
```

### HTML での参照例

```html
<img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/payment/stripe.svg" alt="Stripe" width="64">
```

## メタデータ

`logos.yaml` に全ロゴのメタ情報あり。slug / 提供会社 / カテゴリ / ブランドカラー / 公式URL / プレスキットURL / ライセンス区分。

## ライセンス

- メタデータ・スクリプト: MIT (株式会社Craval)
- ロゴ画像: 各社の商標。公正使用の範囲で利用 (詳細は [LICENSE](./LICENSE) 参照)

## ロゴ収集状況

- 合計: **124社**
- 本物ロゴ取得済: 18社（Simple Icons / gilbarbara/logos / 公式DL）
- プレースホルダー: 106社（ブランドカラー + 社名テキスト、後日プレスキットから差替予定）

プレースホルダーでも D2 や HTML から参照可能。差替時はファイル名を変えず上書き保存するだけで CDN にも反映される（jsDelivr キャッシュは最大12時間）。

## カテゴリ別一覧

### BtoB/BtoC ECプラットフォーム (15)

| slug | 名称 | 提供会社 | カラー | プレビュー |
|------|------|---------|--------|----------|
| `aladdin-ec` | アラジンEC | 株式会社アイル | `#00529F` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/ec-platform/aladdin-ec.svg" width="40"> |
| `bcart` | Bカート | 株式会社Dai | `#005BAC` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/ec-platform/bcart.svg" width="40"> |
| `bee-cross-border` | Bee Cross Border | 株式会社Bee | `#FFA500` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/ec-platform/bee-cross-border.svg" width="40"> |
| `ec-cube` | EC-CUBE | 株式会社イーシーキューブ | `#FF7700` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/ec-platform/ec-cube.svg" width="40"> |
| `ecbeing` | ecbeing | 株式会社ecbeing | `#E60012` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/ec-platform/ecbeing.svg" width="40"> |
| `ecforce` | ecforce | 株式会社SUPER STUDIO | `#1C1C1C` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/ec-platform/ecforce.svg" width="40"> |
| `futureshop` | futureshop | 株式会社フューチャーショップ | `#1E88E5` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/ec-platform/futureshop.svg" width="40"> |
| `gmo-cloud-ec` | GMOクラウドEC | GMOメイクショップ株式会社 | `#FF6600` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/ec-platform/gmo-cloud-ec.svg" width="40"> |
| `magento` | Adobe Commerce (Magento) | Adobe Inc. | `#EE672F` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/ec-platform/magento.svg" width="40"> |
| `makeshop` | MakeShop | GMOメイクショップ株式会社 | `#FF6600` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/ec-platform/makeshop.svg" width="40"> |
| `orange-ec` | Orange EC | エスアイアソシエイツ株式会社 | `#FF6600` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/ec-platform/orange-ec.svg" width="40"> |
| `shopify` | Shopify | Shopify Inc. | `#7AB55C` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/ec-platform/shopify.svg" width="40"> |
| `shopify-plus` | Shopify Plus | Shopify Inc. | `#5A8E3C` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/ec-platform/shopify-plus.svg" width="40"> |
| `si-web-shopping` | SI Web Shopping | 株式会社SIシステム | `#003366` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/ec-platform/si-web-shopping.svg" width="40"> |
| `w2-unified` | W2 Unified | W2株式会社 | `#0066CC` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/ec-platform/w2-unified.svg" width="40"> |

### 販売管理ソフト (13)

| slug | 名称 | 提供会社 | カラー | プレビュー |
|------|------|---------|--------|----------|
| `aladdin-office` | アラジンオフィス | 株式会社アイル | `#00529F` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/sales-management/aladdin-office.svg" width="40"> |
| `as-hanbai` | A's販売 | 株式会社アクト | `#0066CC` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/sales-management/as-hanbai.svg" width="40"> |
| `bcpos` | BCPOS | 株式会社ビジコム | `#0066B3` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/sales-management/bcpos.svg" width="40"> |
| `hanbai-daijin` | 販売大臣 | 応研株式会社 | `#0066B3` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/sales-management/hanbai-daijin.svg" width="40"> |
| `hanbaio` | 販売王 | ソリマチ株式会社 | `#005BAC` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/sales-management/hanbaio.svg" width="40"> |
| `kanjyo-bugyo` | 勘定奉行 | 株式会社オービックビジネスコンサルタント (OBC) | `#005BAC` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/sales-management/kanjyo-bugyo.svg" width="40"> |
| `kura-bugyo` | 蔵奉行 | 株式会社オービックビジネスコンサルタント (OBC) | `#005BAC` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/sales-management/kura-bugyo.svg" width="40"> |
| `pca-shokon` | PCA商魂・商管 | ピー・シー・エー株式会社 | `#E60012` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/sales-management/pca-shokon.svg" width="40"> |
| `sho-bugyo` | 商奉行 | 株式会社オービックビジネスコンサルタント (OBC) | `#005BAC` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/sales-management/sho-bugyo.svg" width="40"> |
| `shokura-bugyo` | 商蔵奉行クラウド | 株式会社オービックビジネスコンサルタント (OBC) | `#005BAC` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/sales-management/shokura-bugyo.svg" width="40"> |
| `smile-v` | SMILE V | 株式会社大塚商会 | `#FFA500` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/sales-management/smile-v.svg" width="40"> |
| `super-cocktail` | スーパーカクテルCore | 内田洋行ITソリューションズ | `#003366` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/sales-management/super-cocktail.svg" width="40"> |
| `yayoi-hanbai` | 弥生販売 | 弥生株式会社 | `#E60012` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/sales-management/yayoi-hanbai.svg" width="40"> |

### Bカート公式ERP/販売管理アプリ (8)

| slug | 名称 | 提供会社 | カラー | プレビュー |
|------|------|---------|--------|----------|
| `banking-erp` | BANKING ERP | 株式会社スマイルワークス | `#003366` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/erp-bcart-app/banking-erp.svg" width="40"> |
| `btone` | Btone（ビートーン） | 株式会社ソトバコ | `#1C1C1C` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/erp-bcart-app/btone.svg" width="40"> |
| `cammacs` | キャムマックス | 株式会社キャム | `#005BAC` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/erp-bcart-app/cammacs.svg" width="40"> |
| `cross-mall` | CROSS MALL | 株式会社ウイングス・コンサルティング | `#FF6600` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/erp-bcart-app/cross-mall.svg" width="40"> |
| `goqsystem` | GoQSystem | 株式会社GoQSystem | `#0099CC` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/erp-bcart-app/goqsystem.svg" width="40"> |
| `onescloset` | One'sCloset | 株式会社フレイトリンクスジャパン | `#000000` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/erp-bcart-app/onescloset.svg" width="40"> |
| `s-flow` | s-flow | 株式会社エスフロー | `#0099CC` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/erp-bcart-app/s-flow.svg" width="40"> |
| `smileworks` | SmileWorks | 株式会社スマイルワークス | `#FFA500` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/erp-bcart-app/smileworks.svg" width="40"> |

### EAI / データ連携 / ノーコード自動化 (8)

| slug | 名称 | 提供会社 | カラー | プレビュー |
|------|------|---------|--------|----------|
| `cdata-arc` | CData Arc | CData Software Japan | `#0085CA` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/eai/cdata-arc.svg" width="40"> |
| `ec-connector` | ECコネクター | 株式会社久 | `#0066CC` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/eai/ec-connector.svg" width="40"> |
| `make` | Make | Celonis SE | `#6D00CC` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/eai/make.svg" width="40"> |
| `teps` | TēPs（テープス） | テープス株式会社 | `#00C853` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/eai/teps.svg" width="40"> |
| `tetlink` | テットリンク | 株式会社テットラスト | `#0066CC` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/eai/tetlink.svg" width="40"> |
| `workato` | Workato | Workato Inc. | `#E94B35` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/eai/workato.svg" width="40"> |
| `yoom` | Yoom | Yoom株式会社 | `#FFC107` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/eai/yoom.svg" width="40"> |
| `zapier` | Zapier | Zapier Inc. | `#FF4A00` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/eai/zapier.svg" width="40"> |

### 在庫管理・WMS (9)

| slug | 名称 | 提供会社 | カラー | プレビュー |
|------|------|---------|--------|----------|
| `assist-tencho` | アシスト店長 | 株式会社ハングリード | `#FF6600` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/inventory-wms/assist-tencho.svg" width="40"> |
| `commercerobo` | Commercerobo | 株式会社コマースロボティクス | `#003366` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/inventory-wms/commercerobo.svg" width="40"> |
| `logiec` | logiec（ロジーク） | 株式会社はぴロジ | `#0099CC` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/inventory-wms/logiec.svg" width="40"> |
| `logiless` | LOGILESS（ロジレス） | 株式会社ロジレス | `#0099CC` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/inventory-wms/logiless.svg" width="40"> |
| `logimopro` | ロジモプロ | 株式会社清長 | `#FF6600` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/inventory-wms/logimopro.svg" width="40"> |
| `logizard-zero` | ロジザードZERO | ロジザード株式会社 | `#0066B3` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/inventory-wms/logizard-zero.svg" width="40"> |
| `next-engine` | ネクストエンジン | NE株式会社 | `#E60012` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/inventory-wms/next-engine.svg" width="40"> |
| `rakuraku-zaiko` | らくらく在庫 | グリニッジ株式会社 | `#00A651` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/inventory-wms/rakuraku-zaiko.svg" width="40"> |
| `tempostar` | TEMPOSTAR | SAVAWAY株式会社 | `#005BAC` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/inventory-wms/tempostar.svg" width="40"> |

### POS・レジ (3)

| slug | 名称 | 提供会社 | カラー | プレビュー |
|------|------|---------|--------|----------|
| `airregi` | Airレジ | 株式会社リクルート | `#FF6F61` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/pos/airregi.svg" width="40"> |
| `smaregi` | スマレジ | 株式会社スマレジ | `#00A0E9` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/pos/smaregi.svg" width="40"> |
| `ubiregi` | ユビレジ | 株式会社ユビレジ | `#FF6600` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/pos/ubiregi.svg" width="40"> |

### 決済 (15)

| slug | 名称 | 提供会社 | カラー | プレビュー |
|------|------|---------|--------|----------|
| `amazon-pay` | Amazon Pay | Amazon.com Inc. | `#FF9900` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/payment/amazon-pay.svg" width="40"> |
| `bcart-creca` | Bカートクレカ決済 | 株式会社ゼウス | `#005BAC` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/payment/bcart-creca.svg" width="40"> |
| `bcart-kakebarai` | Bカート掛け払い | マネーフォワードケッサイ株式会社 | `#005BAC` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/payment/bcart-kakebarai.svg" width="40"> |
| `gmo-pg` | GMOペイメントゲートウェイ | GMOペイメントゲートウェイ株式会社 | `#003366` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/payment/gmo-pg.svg" width="40"> |
| `kuroneko-kakebarai` | クロネコ掛け払い | ヤマトクレジットファイナンス株式会社 | `#000000` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/payment/kuroneko-kakebarai.svg" width="40"> |
| `kuroneko-webcollect` | クロネコwebコレクト | ヤマト運輸株式会社 | `#000000` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/payment/kuroneko-webcollect.svg" width="40"> |
| `np-kakebarai` | NP掛け払い | 株式会社ネットプロテクションズ | `#FF6600` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/payment/np-kakebarai.svg" width="40"> |
| `paid` | Paid（ペイド） | 株式会社ラクーンフィナンシャル | `#E60012` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/payment/paid.svg" width="40"> |
| `paygent` | PAYGENT | 株式会社ペイジェント | `#0066CC` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/payment/paygent.svg" width="40"> |
| `paypal` | PayPal | PayPal Holdings | `#003087` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/payment/paypal.svg" width="40"> |
| `paypay` | PayPay | PayPay株式会社 | `#FF0033` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/payment/paypay.svg" width="40"> |
| `rakuten-pay` | 楽天ペイ | 楽天ペイメント株式会社 | `#BF0000` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/payment/rakuten-pay.svg" width="40"> |
| `sbpayment` | SBペイメントサービス | SBペイメントサービス株式会社 | `#FF6600` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/payment/sbpayment.svg" width="40"> |
| `stripe` | Stripe | Stripe Inc. | `#635BFF` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/payment/stripe.svg" width="40"> |
| `veritrans` | ベリトランス | ベリトランス株式会社 | `#005BAC` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/payment/veritrans.svg" width="40"> |

### 物流・送り状発行 (5)

| slug | 名称 | 提供会社 | カラー | プレビュー |
|------|------|---------|--------|----------|
| `japan-post` | 日本郵便 | 日本郵便株式会社 | `#DA1F26` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/logistics/japan-post.svg" width="40"> |
| `sagawa-e-hiden` | e飛伝Ⅲ | 佐川急便株式会社 | `#005BAC` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/logistics/sagawa-e-hiden.svg" width="40"> |
| `yamato` | ヤマト運輸 | ヤマト運輸株式会社 | `#FFCB05` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/logistics/yamato.svg" width="40"> |
| `yamato-b2cloud` | ヤマトB2クラウド | ヤマト運輸株式会社 | `#000000` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/logistics/yamato-b2cloud.svg" width="40"> |
| `yu-print-r` | ゆうプリR | 日本郵便株式会社 | `#DA1F26` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/logistics/yu-print-r.svg" width="40"> |

### グループウェア・コミュニケーション基盤 (11)

| slug | 名称 | 提供会社 | カラー | プレビュー |
|------|------|---------|--------|----------|
| `chatwork` | Chatwork | Chatwork株式会社 | `#1F2D3D` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/groupware/chatwork.svg" width="40"> |
| `cybozu-office` | サイボウズOffice | サイボウズ株式会社 | `#3E6EB4` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/groupware/cybozu-office.svg" width="40"> |
| `desknets-neo` | desknet's NEO | 株式会社ネオジャパン | `#0066B3` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/groupware/desknets-neo.svg" width="40"> |
| `garoon` | Garoon | サイボウズ株式会社 | `#005BAC` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/groupware/garoon.svg" width="40"> |
| `google-workspace` | Google Workspace | Google LLC | `#4285F4` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/groupware/google-workspace.svg" width="40"> |
| `kintone` | kintone | サイボウズ株式会社 | `#00A0E9` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/groupware/kintone.svg" width="40"> |
| `microsoft-365` | Microsoft 365 | Microsoft Corporation | `#D83B01` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/groupware/microsoft-365.svg" width="40"> |
| `ms-teams` | Microsoft Teams | Microsoft Corporation | `#6264A7` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/groupware/ms-teams.svg" width="40"> |
| `notion` | Notion | Notion Labs Inc. | `#000000` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/groupware/notion.svg" width="40"> |
| `slack` | Slack | Slack Technologies (Salesforce) | `#4A154B` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/groupware/slack.svg" width="40"> |
| `zoom` | Zoom | Zoom Video Communications | `#2D8CFF` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/groupware/zoom.svg" width="40"> |

### CRM / MA / SFA (10)

| slug | 名称 | 提供会社 | カラー | プレビュー |
|------|------|---------|--------|----------|
| `eight` | Eight | Sansan株式会社 | `#E60012` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/crm-ma/eight.svg" width="40"> |
| `hubspot` | HubSpot | HubSpot Inc. | `#FF7A59` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/crm-ma/hubspot.svg" width="40"> |
| `kairos3` | Kairos3 | カイロスマーケティング株式会社 | `#0066B3` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/crm-ma/kairos3.svg" width="40"> |
| `list-finder` | List Finder | 株式会社Innovation X Solutions | `#0099CC` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/crm-ma/list-finder.svg" width="40"> |
| `ltv-lab` | LTV-Lab for BtoB | 株式会社LTV-X | `#0066CC` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/crm-ma/ltv-lab.svg" width="40"> |
| `marketo` | Marketo Engage | Adobe Inc. | `#5C4C9F` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/crm-ma/marketo.svg" width="40"> |
| `pardot` | Account Engagement (Pardot) | Salesforce Inc. | `#00A1E0` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/crm-ma/pardot.svg" width="40"> |
| `salesforce` | Salesforce | Salesforce Inc. | `#00A1E0` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/crm-ma/salesforce.svg" width="40"> |
| `sansan` | Sansan | Sansan株式会社 | `#E60012` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/crm-ma/sansan.svg" width="40"> |
| `uchideno-kozuchi` | うちでのこづち | 株式会社E-Grant | `#FF6600` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/crm-ma/uchideno-kozuchi.svg" width="40"> |

### 会計・労務 (5)

| slug | 名称 | 提供会社 | カラー | プレビュー |
|------|------|---------|--------|----------|
| `freee` | freee | フリー株式会社 | `#00B8E2` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/backoffice/freee.svg" width="40"> |
| `moneyforward` | マネーフォワード | 株式会社マネーフォワード | `#005BAC` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/backoffice/moneyforward.svg" width="40"> |
| `obic-bugyo-cloud` | 奉行クラウド | 株式会社オービックビジネスコンサルタント (OBC) | `#005BAC` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/backoffice/obic-bugyo-cloud.svg" width="40"> |
| `smarthr` | SmartHR | 株式会社SmartHR | `#00A0E9` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/backoffice/smarthr.svg" width="40"> |
| `yayoi` | 弥生会計 | 弥生株式会社 | `#E60012` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/backoffice/yayoi.svg" width="40"> |

### コミュニケーション（顧客対応） (4)

| slug | 名称 | 提供会社 | カラー | プレビュー |
|------|------|---------|--------|----------|
| `gmail` | Gmail | Google LLC | `#EA4335` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/communication/gmail.svg" width="40"> |
| `line` | LINE | LINEヤフー株式会社 | `#06C755` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/communication/line.svg" width="40"> |
| `line-official` | LINE公式アカウント | LINEヤフー株式会社 | `#06C755` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/communication/line-official.svg" width="40"> |
| `relation` | Re:lation（リレーション） | 株式会社インゲージ | `#0099CC` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/communication/relation.svg" width="40"> |

### レビュー・サイト内検索・売上UP (4)

| slug | 名称 | 提供会社 | カラー | プレビュー |
|------|------|---------|--------|----------|
| `ec-recommender` | ECレコメンダー | エクスプロージョン株式会社 | `#0099CC` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/review-tool/ec-recommender.svg" width="40"> |
| `ec-search` | ECサーチ | エクスプロージョン株式会社 | `#005BAC` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/review-tool/ec-search.svg" width="40"> |
| `goq-smile` | GoQ Smile | 株式会社GoQSystem | `#0099CC` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/review-tool/goq-smile.svg" width="40"> |
| `u-komi` | U-KOMI | 株式会社サブスパイア | `#FF6600` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/review-tool/u-komi.svg" width="40"> |

### 開発基盤・データ (5)

| slug | 名称 | 提供会社 | カラー | プレビュー |
|------|------|---------|--------|----------|
| `aws` | Amazon Web Services | Amazon.com Inc. | `#FF9900` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/dev/aws.svg" width="40"> |
| `azure` | Microsoft Azure | Microsoft Corporation | `#0078D4` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/dev/azure.svg" width="40"> |
| `gcp` | Google Cloud Platform | Google LLC | `#4285F4` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/dev/gcp.svg" width="40"> |
| `tableau` | Tableau | Tableau Software (Salesforce) | `#E97627` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/dev/tableau.svg" width="40"> |
| `wordpress` | WordPress | WordPress Foundation | `#21759B` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/dev/wordpress.svg" width="40"> |

### 国内モール / SaaSカート (8)

| slug | 名称 | 提供会社 | カラー | プレビュー |
|------|------|---------|--------|----------|
| `amazon` | Amazon | Amazon.com Inc. | `#FF9900` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/jp-mall/amazon.svg" width="40"> |
| `base` | BASE | BASE株式会社 | `#00C800` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/jp-mall/base.svg" width="40"> |
| `colorme` | カラーミーショップ | GMOペパボ株式会社 | `#FF6600` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/jp-mall/colorme.svg" width="40"> |
| `mercari-shops` | メルカリShops | 株式会社メルカリ | `#FF0033` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/jp-mall/mercari-shops.svg" width="40"> |
| `qoo10` | Qoo10 | eBay Japan合同会社 | `#FF0033` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/jp-mall/qoo10.svg" width="40"> |
| `rakuten-ichiba` | 楽天市場 | 楽天グループ株式会社 | `#BF0000` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/jp-mall/rakuten-ichiba.svg" width="40"> |
| `stores` | STORES | ストアーズ株式会社 | `#000000` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/jp-mall/stores.svg" width="40"> |
| `yahoo-shopping` | Yahoo!ショッピング | LINEヤフー株式会社 | `#FF0033` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/jp-mall/yahoo-shopping.svg" width="40"> |

### 自社 (1)

| slug | 名称 | 提供会社 | カラー | プレビュー |
|------|------|---------|--------|----------|
| `craval` | Craval（株式会社Craval） | 株式会社Craval | `#1C1C1C` | <img src="https://cdn.jsdelivr.net/gh/craval-inc/cv-iconpack@main/logos/craval/craval.svg" width="40"> |

## ロゴ追加・差替の運用

### 新しいサービスを追加する

1. `logos.yaml` にエントリ追加（slug/name/category/vendor/color/source/license/file）
2. `logos/<category>/<slug>.svg` にロゴを配置（本物 or プレースホルダー）
3. `python scripts/generate-placeholders.py` で未配置ロゴのプレースホルダーを一括生成
4. `python scripts/build-readme.py` で README 再生成
5. commit & push

### プレースホルダーを本物ロゴに差替える

1. 各社プレスキット (`logos.yaml` の `press_kit` 参照) からSVGをDL
2. 既存ファイルを上書き（ファイル名は変えない）
3. commit & push → jsDelivr CDNに最大12時間で反映

### 関連リポジトリ

- [craval-inc/craval-site-renewal](https://github.com/craval-inc/craval-site-renewal): BtoB ECメディア本体
- [craval-inc/article-tool](https://github.com/craval-inc/article-tool): 記事生成ツール
