from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTICLES_DIR = ROOT / "articles"
TEMPLATES_DIR = ROOT / "templates"


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "new-article"


def main() -> int:
    if len(sys.argv) < 2:
        print('Usage: python .\\scripts\\new_article.py "article-title"')
        return 1

    slug = slugify(" ".join(sys.argv[1:]))
    article_dir = ARTICLES_DIR / slug

    if article_dir.exists():
        print(f"Article already exists: {article_dir}")
        return 1

    article_dir.mkdir(parents=True)

    brief_template = TEMPLATES_DIR / "article_brief.md"
    shutil.copy2(brief_template, article_dir / "00_brief.md")

    for file_name in [
        "01_research.md",
        "02_outline.md",
        "03_draft.md",
        "04_final.md",
        "notes.md",
    ]:
        (article_dir / file_name).write_text("", encoding="utf-8")

    print(f"Created: {article_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
