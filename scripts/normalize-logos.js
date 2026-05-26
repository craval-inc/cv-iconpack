/**
 * 全ロゴを統一サイズの白背景カードに正規化する。
 *
 * 各ロゴのアスペクト比は保ったまま、240x120 の白背景キャンバスの
 * 中央に最大fitで配置する。これで図解で並べたときサイズが揃う。
 *
 * 出力: logos/normalized/<slug>.png
 */

'use strict';

const fs = require('fs');
const path = require('path');
const sharp = require('sharp');
const yaml = require('js-yaml');

const ROOT = path.resolve(__dirname, '..');
const LOGOS_YAML = path.join(ROOT, 'logos.yaml');
const OUT_DIR = path.join(ROOT, 'logos', 'normalized');

const CANVAS_W = 240;
const CANVAS_H = 120;
const INNER_PADDING = 14; // ロゴの周囲余白

async function normalize(entry) {
  const inputPath = path.join(ROOT, entry.file);
  if (!fs.existsSync(inputPath)) {
    console.warn(`  SKIP: missing ${entry.file}`);
    return null;
  }

  const outPath = path.join(OUT_DIR, `${entry.slug}.png`);

  try {
    // 内側のロゴ表示エリア
    const maxLogoW = CANVAS_W - INNER_PADDING * 2;
    const maxLogoH = CANVAS_H - INNER_PADDING * 2;

    // ロゴをアスペクト比保持でfit、透明背景PNGに変換
    const logoBuf = await sharp(inputPath, { density: 300 })
      .resize(maxLogoW, maxLogoH, {
        fit: 'contain',
        background: { r: 0, g: 0, b: 0, alpha: 0 },
      })
      .png()
      .toBuffer();

    const logoMeta = await sharp(logoBuf).metadata();

    // 白背景キャンバス + ロゴ中央配置
    await sharp({
      create: {
        width: CANVAS_W,
        height: CANVAS_H,
        channels: 4,
        background: { r: 255, g: 255, b: 255, alpha: 1 },
      },
    })
      .composite([
        {
          input: logoBuf,
          top: Math.round((CANVAS_H - logoMeta.height) / 2),
          left: Math.round((CANVAS_W - logoMeta.width) / 2),
        },
      ])
      .png()
      .toFile(outPath);

    return outPath;
  } catch (e) {
    console.error(`  ERROR ${entry.slug}: ${e.message}`);
    return null;
  }
}

async function main() {
  const logos = yaml.load(fs.readFileSync(LOGOS_YAML, 'utf8'));

  if (!fs.existsSync(OUT_DIR)) fs.mkdirSync(OUT_DIR, { recursive: true });

  let ok = 0;
  let fail = 0;

  for (const entry of logos) {
    const r = await normalize(entry);
    if (r) {
      console.log(`  OK   ${entry.slug.padEnd(28)} -> ${path.relative(ROOT, r)}`);
      ok++;
    } else {
      fail++;
    }
  }

  console.log(`\nDone: ${ok} success / ${fail} failed`);
}

main().catch(e => {
  console.error(e);
  process.exit(1);
});
