"""
Task 3 — Convert toàn bộ file trong data/landing/ thành Markdown.

Sử dụng MarkItDown của Microsoft để convert PDF/DOCX sang .md.
JSON news articles được convert bằng cách extract content_markdown trực tiếp.
"""

import json
from pathlib import Path

LANDING_DIR = Path(__file__).parent.parent / "data" / "landing"
OUTPUT_DIR = Path(__file__).parent.parent / "data" / "standardized"


def convert_legal_docs():
    """Convert DOCX files trong data/landing/legal/ sang markdown."""
    from markitdown import MarkItDown

    legal_dir = LANDING_DIR / "legal"
    output_dir = OUTPUT_DIR / "legal"
    output_dir.mkdir(parents=True, exist_ok=True)

    if not legal_dir.exists():
        print("  ⚠ data/landing/legal/ chưa tồn tại, bỏ qua")
        return 0

    md = MarkItDown()
    converted = 0

    for filepath in legal_dir.iterdir():
        if filepath.suffix.lower() in (".pdf", ".docx", ".doc"):
            print(f"  Converting: {filepath.name}")
            result = md.convert(str(filepath))
            output_path = output_dir / f"{filepath.stem}.md"
            output_path.write_text(result.text_content, encoding="utf-8")
            print(f"    ✓ Saved: {output_path.name} ({len(result.text_content):,} chars)")
            converted += 1

    return converted


def convert_news_articles():
    """Convert JSON news articles sang markdown."""
    news_dir = LANDING_DIR / "news"
    output_dir = OUTPUT_DIR / "news"
    output_dir.mkdir(parents=True, exist_ok=True)

    if not news_dir.exists():
        print("  ⚠ data/landing/news/ chưa tồn tại, bỏ qua")
        return 0

    converted = 0

    for filepath in sorted(news_dir.iterdir()):
        if filepath.suffix.lower() == ".json":
            print(f"  Converting: {filepath.name}")
            data = json.loads(filepath.read_text(encoding="utf-8"))

            output_path = output_dir / f"{filepath.stem}.md"

            # Format markdown với metadata header
            title = data.get("title", "Unknown Title")
            url = data.get("url", "N/A")
            date = data.get("date_crawled", "N/A")
            content = data.get("content_markdown", "")

            header = (
                f"# {title}\n\n"
                f"**Source:** {url}  \n"
                f"**Crawled:** {date}\n\n"
                f"---\n\n"
            )

            full_content = header + content
            output_path.write_text(full_content, encoding="utf-8")
            print(f"    ✓ Saved: {output_path.name} ({len(full_content):,} chars)")
            converted += 1

        elif filepath.suffix.lower() in (".html", ".md", ".txt"):
            # Copy trực tiếp sang output với tên .md
            output_path = output_dir / f"{filepath.stem}.md"
            content = filepath.read_text(encoding="utf-8", errors="ignore")
            output_path.write_text(content, encoding="utf-8")
            print(f"    ✓ Copied: {output_path.name}")
            converted += 1

    return converted


def convert_all():
    """Convert toàn bộ files từ landing sang standardized."""
    print("=" * 60)
    print("Task 3: Convert to Markdown (MarkItDown)")
    print("=" * 60)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("\n--- Legal Documents ---")
    n_legal = convert_legal_docs()

    print("\n--- News Articles ---")
    n_news = convert_news_articles()

    total = n_legal + n_news
    print(f"\n✓ Đã convert {total} files ({n_legal} legal + {n_news} news)")
    print(f"  Output tại: {OUTPUT_DIR}")
    return total


if __name__ == "__main__":
    convert_all()
