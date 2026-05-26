/**
 * 各ロゴの実寸とアスペクト比を測定して metadata.json に書き出す。
 * 図解のD2を書くときに、これを参照してロゴごとに最適なwidth/heightを決める。
 */
'use strict';
const fs = require('fs');
const path = require('path');
const sharp = require('sharp');
const yaml = require('js-yaml');

const ROOT = path.resolve(__dirname, '..');
const logos = yaml.load(fs.readFileSync(path.join(ROOT, 'logos.yaml'), 'utf8'));

(async () => {
  const result = {};
  for (const e of logos) {
    const p = path.join(ROOT, e.file);
    if (!fs.existsSync(p)) continue;
    try {
      const m = await sharp(p, { density: 200 }).metadata();
      const ar = m.width / m.height;
      let shape;
      if (ar > 2.5) shape = 'wide';
      else if (ar > 1.5) shape = 'horizontal';
      else if (ar > 0.8) shape = 'square';
      else shape = 'vertical';
      result[e.slug] = { w: m.width, h: m.height, ar: +ar.toFixed(2), shape };
    } catch (err) {
      result[e.slug] = { error: err.message };
    }
  }
  fs.writeFileSync(path.join(ROOT, 'logos-metadata.json'), JSON.stringify(result, null, 2));
  // 表示用
  const order = Object.entries(result).sort((a, b) => (b[1].ar || 0) - (a[1].ar || 0));
  console.log('slug                        size           ar    shape');
  console.log('----------------------------------------------------------');
  for (const [slug, info] of order) {
    if (info.error) continue;
    console.log(`${slug.padEnd(28)} ${(info.w + '×' + info.h).padEnd(14)} ${String(info.ar).padEnd(5)} ${info.shape}`);
  }
})();
