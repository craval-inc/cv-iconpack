# 図解サンプル

cv-iconpack のロゴを使った D2 図解のサンプル集。

## 動作確認方法

### Web Playground（インストール不要）

1. https://play.d2lang.com にアクセス
2. このディレクトリの `.d2` ファイルの中身を貼り付け
3. 即レンダリング

### CLI（D2インストール後）

```bash
# Windows: winget install d2
# Mac:     brew install d2

d2 examples/bcart-kintone-integration.d2 out.svg
```

## サンプル一覧

| ファイル | 内容 | 使うロゴ |
|---|---|---|
| `bcart-kintone-integration.d2` | Bカート × kintone のWebhook連携 | bcart / ec-connector / kintone |
| `bcart-yayoi-integration.d2` | Bカート × 弥生販売 のCSV連携 (NP掛け払い + ヤマトB2 込み) | bcart / ec-connector / yayoi-hanbai / np-kakebarai / yamato-b2cloud |
