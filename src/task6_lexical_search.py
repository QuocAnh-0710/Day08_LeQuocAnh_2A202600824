"""
Task 6 — Lexical Search Module (BM25).

BM25 (Best Match 25) — cơ chế hoạt động:
    score(q, d) = Σ IDF(qi) * (tf(qi,d) * (k1+1)) / (tf(qi,d) + k1*(1 - b + b*|d|/avgdl))

    - TF (Term Frequency): từ xuất hiện nhiều trong document → điểm cao hơn
      nhưng có saturation: thêm lần nữa ít tăng điểm hơn (k1 = 1.5)
    - IDF (Inverse Document Frequency): từ hiếm (ít doc chứa) → quan trọng hơn
    - Length normalization: document dài không bị ưu tiên quá mức (b = 0.75)

Corpus được load từ data/corpus.json (cùng chunks với ChromaDB ở Task 4).
"""

import json
from pathlib import Path

_CORPUS_FILE = Path(__file__).parent.parent / "data" / "corpus.json"

# Lazy-load index
_bm25 = None
_corpus: list[dict] = []


def _load_corpus() -> list[dict]:
    """Load corpus từ file JSON."""
    if not _CORPUS_FILE.exists():
        raise RuntimeError(
            "corpus.json chưa tồn tại. Chạy task4_chunking_indexing.run_pipeline() trước."
        )
    return json.loads(_CORPUS_FILE.read_text(encoding="utf-8"))


def _get_bm25():
    """Lazy init BM25 index."""
    global _bm25, _corpus
    if _bm25 is None:
        from rank_bm25 import BM25Okapi

        _corpus = _load_corpus()
        # Tokenize: split đơn giản, lowercase
        # Với tiếng Việt, word-level tokenization cơ bản vẫn cho kết quả tốt
        tokenized = [doc["content"].lower().split() for doc in _corpus]
        _bm25 = BM25Okapi(tokenized, k1=1.5, b=0.75)

    return _bm25, _corpus


def lexical_search(query: str, top_k: int = 10) -> list[dict]:
    """
    Tìm kiếm từ khóa sử dụng BM25.

    Args:
        query: Câu truy vấn
        top_k: Số lượng kết quả tối đa

    Returns:
        List of {'content': str, 'score': float, 'metadata': dict}
        Sorted by BM25 score descending.
    """
    import numpy as np

    bm25, corpus = _get_bm25()

    tokenized_query = query.lower().split()
    scores = bm25.get_scores(tokenized_query)

    # Lấy top_k indices có score cao nhất
    top_indices = np.argsort(scores)[::-1][:top_k]

    results = []
    for idx in top_indices:
        if scores[idx] > 0:
            results.append({
                "content": corpus[idx]["content"],
                "score": float(scores[idx]),
                "metadata": corpus[idx].get("metadata", {}),
            })

    # Đảm bảo sorted descending
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]


if __name__ == "__main__":
    test_queries = [
        "Điều 249 tàng trữ trái phép chất ma tuý",
        "hình phạt tù chung thân",
        "cai nghiện bắt buộc",
    ]
    for q in test_queries:
        print(f"\nQuery: {q}")
        results = lexical_search(q, top_k=3)
        for r in results:
            print(f"  [{r['score']:.3f}] {r['content'][:80]}...")
