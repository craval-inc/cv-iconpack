"""
logos/ 配下の実ファイル拡張子と logos.yaml の file: フィールドを同期する。

fetch-jp-logos.py で .svg 以外の拡張子で保存されたファイル (png/jpg/webp) を検出し、
YAMLの file: フィールドを実際の拡張子に書き換える。

プレースホルダー (.svg) が残っていれば削除して、本物の方を残す。
"""

import yaml
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOGOS_YAML = ROOT / "logos.yaml"

EXTS = [".svg", ".png", ".jpg", ".jpeg", ".webp"]


def find_actual_file(base_no_ext: Path) -> Path | None:
    """指定パス(拡張子なし)に対応する実ファイル(svg/png/jpg/jpeg/webp)を探す"""
    for ext in EXTS:
        p = base_no_ext.with_suffix(ext)
        if p.exists():
            return p
    return None


def is_placeholder_svg(path: Path) -> bool:
    """プレースホルダーSVGかどうか"""
    if not path.exists() or path.suffix != ".svg":
        return False
    try:
        text = path.read_text(encoding="utf-8")
        return 'rx="32"' in text and "<path" not in text and "<g " not in text
    except Exception:
        return False


def main():
    with LOGOS_YAML.open(encoding="utf-8") as f:
        logos = yaml.safe_load(f)

    text = LOGOS_YAML.read_text(encoding="utf-8")
    updated = 0
    deleted_placeholders = 0

    for entry in logos:
        slug = entry["slug"]
        file_in_yaml = entry["file"]
        base = (ROOT / file_in_yaml).with_suffix("")

        # 同じ basename で複数拡張子が存在する場合の処理
        existing = []
        for ext in EXTS:
            p = base.with_suffix(ext)
            if p.exists():
                existing.append(p)

        if not existing:
            continue

        # 本物優先（プレースホルダーSVGは捨てる）
        non_placeholders = [p for p in existing if not is_placeholder_svg(p)]

        if not non_placeholders:
            # 全部プレースホルダー: そのまま
            continue

        # 本物が複数あればSVG優先、次にPNG, JPG, WebP
        priority = {".svg": 0, ".png": 1, ".jpg": 2, ".jpeg": 2, ".webp": 3}
        non_placeholders.sort(key=lambda p: priority.get(p.suffix.lower(), 9))
        keep = non_placeholders[0]

        # それ以外のファイル（プレースホルダーSVG含む）を削除
        for p in existing:
            if p != keep:
                p.unlink()
                deleted_placeholders += 1
                print(f"  delete: {p.relative_to(ROOT)}")

        # YAML更新
        new_file_path = str(keep.relative_to(ROOT)).replace("\\", "/")
        if new_file_path != file_in_yaml:
            # logos.yaml のテキストを文字列置換（書式維持）
            old_line = f"  file: {file_in_yaml}"
            new_line = f"  file: {new_file_path}"
            if old_line in text:
                text = text.replace(old_line, new_line, 1)
                updated += 1
                print(f"  yaml:   {slug}: {file_in_yaml} -> {new_file_path}")

    LOGOS_YAML.write_text(text, encoding="utf-8")
    print()
    print(f"updated yaml entries: {updated}")
    print(f"deleted duplicates:   {deleted_placeholders}")


if __name__ == "__main__":
    main()
