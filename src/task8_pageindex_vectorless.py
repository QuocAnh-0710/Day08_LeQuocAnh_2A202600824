"""
Task 8 — PageIndex Vectorless RAG.

PageIndex sử dụng structural understanding của document thay vì embeddings.
Đăng ký tại: https://pageindex.ai/

Nếu không có API key → fallback sang simple keyword search trên corpus local.
"""

import json
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PAGEINDEX_API_KEY = os.getenv("PAGEINDEX_API_KEY", "")
STANDARDIZED_DIR = Path(__file__).parent.parent / "data" / "standardized"
CORPUS_FILE = Path(__file__).parent.parent / "data" / "corpus.json"


def _fallback_keyword_search(query: str, top_k: int = 5) -> list[dict]:
    """
    Fallback: keyword search đơn giản trên corpus local khi không có PageIndex API key.
    Tính score theo số từ query xuất hiện trong content.
    """
    if not CORPUS_FILE.exists():
        return []

    corpus = json.loads(CORPUS_FILE.read_text(encoding="utf-8"))
    query_words = set(query.lower().split())

    scored = []
    for item in corpus:
        content_lower = item["content"].lower()
        # Count overlapping words
        content_words = set(content_lower.split())
        overlap = len(query_words & content_words)
        if overlap > 0:
            score = overlap / (len(query_words) + 1)
            scored.append({
                "content": item["content"],
                "score": round(score, 4),
                "metadata": item.get("metadata", {}),
                "source": "pageindex",
            })

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]


def upload_documents():
    """Upload markdown documents lên PageIndex."""
    if not PAGEINDEX_API_KEY:
        print("  ⚠ Không có PAGEINDEX_API_KEY, bỏ qua upload")
        return

    try:
        from pageindex import PageIndex

        pi = PageIndex(api_key=PAGEINDEX_API_KEY)

        for md_file in STANDARDIZED_DIR.rglob("*.md"):
            content = md_file.read_text(encoding="utf-8")
            pi.upload(
                content=content,
                metadata={"filename": md_file.name, "type": md_file.parent.name},
            )
            print(f"  ✓ Uploaded: {md_file.name}")
    except ImportError:
        print("  ⚠ pageindex package chưa cài, bỏ qua upload")
    except Exception as e:
        print(f"  ✗ Upload error: {e}")


def pageindex_search(query: str, top_k: int = 5) -> list[dict]:
    """
    Vectorless retrieval sử dụng PageIndex.
    Fallback sang keyword search nếu không có API key.

    Returns:
        List of {'content': str, 'score': float, 'metadata': dict, 'source': 'pageindex'}
    """
    if not PAGEINDEX_API_KEY:
        return _fallback_keyword_search(query, top_k)

    try:
        from pageindex import PageIndex

        pi = PageIndex(api_key=PAGEINDEX_API_KEY)
        results = pi.query(query=query, top_k=top_k)

        return [
            {
                "content": r.text if hasattr(r, "text") else str(r),
                "score": float(r.score) if hasattr(r, "score") else 0.5,
                "metadata": r.metadata if hasattr(r, "metadata") else {},
                "source": "pageindex",
            }
            for r in results
        ]
    except ImportError:
        return _fallback_keyword_search(query, top_k)
    except Exception as e:
        print(f"  ⚠ PageIndex error: {e}, fallback sang keyword search")
        return _fallback_keyword_search(query, top_k)


if __name__ == "__main__":
    if not PAGEINDEX_API_KEY:
        print("⚠ PAGEINDEX_API_KEY chưa set → dùng keyword search fallback")
        print("  Đăng ký tại: https://pageindex.ai/\n")
    else:
        print("Uploading documents...")
        upload_documents()

    print("Test query: 'hình phạt sử dụng ma tuý'")
    results = pageindex_search("hình phạt sử dụng ma tuý", top_k=3)
    for r in results:
        print(f"  [{r['score']:.3f}] [{r['source']}] {r['content'][:80]}...")
