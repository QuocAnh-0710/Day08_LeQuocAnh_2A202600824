"""
Task 9 — Retrieval Pipeline Hoàn Chỉnh.

Pipeline:
    Query
      ├→ Semantic Search (Task 5)  → dense_results
      ├→ Lexical Search  (Task 6)  → sparse_results
      │
      ├→ Merge bằng RRF (Task 7)   → merged_results
      │
      └→ Nếu top score < threshold:
            └→ Fallback PageIndex (Task 8) → fallback_results
"""

from .task5_semantic_search import semantic_search
from .task6_lexical_search import lexical_search
from .task7_reranking import rerank_rrf
from .task8_pageindex_vectorless import pageindex_search

SCORE_THRESHOLD = 0.01   # RRF score tự nhiên nhỏ (~0.016–0.033); 0.01 = chỉ fallback khi rỗng
DEFAULT_TOP_K = 5


def retrieve(
    query: str,
    top_k: int = DEFAULT_TOP_K,
    score_threshold: float = SCORE_THRESHOLD,
    use_reranking: bool = True,
) -> list[dict]:
    """
    Retrieval pipeline hoàn chỉnh với hybrid search + fallback.

    Args:
        query: Câu truy vấn
        top_k: Số kết quả cuối cùng
        score_threshold: Ngưỡng RRF score tối thiểu
        use_reranking: Có dùng RRF để merge không

    Returns:
        List of {'content': str, 'score': float, 'metadata': dict, 'source': str}
        source: 'hybrid' hoặc 'pageindex'
    """
    try:
        dense_results = semantic_search(query, top_k=top_k * 2)
    except Exception:
        dense_results = []

    try:
        sparse_results = lexical_search(query, top_k=top_k * 2)
    except Exception:
        sparse_results = []

    # Merge bằng RRF nếu có kết quả từ ít nhất 1 source
    merged = []
    if dense_results or sparse_results:
        ranked_lists = []
        if dense_results:
            ranked_lists.append(dense_results)
        if sparse_results:
            ranked_lists.append(sparse_results)

        if use_reranking:
            merged = rerank_rrf(ranked_lists, top_k=top_k * 2)
        else:
            # Simple merge: kết hợp và dedup
            seen = set()
            for item in (dense_results + sparse_results):
                key = item["content"][:100]
                if key not in seen:
                    seen.add(key)
                    merged.append(item)

    # Tag source
    for item in merged:
        item["source"] = "hybrid"

    # Kiểm tra threshold
    best_score = merged[0]["score"] if merged else 0.0
    if not merged or best_score < score_threshold:
        print(
            f"  ⚠ Hybrid score ({best_score:.4f}) < threshold ({score_threshold}). "
            f"Fallback → PageIndex"
        )
        fallback = pageindex_search(query, top_k=top_k)
        if fallback:
            return fallback
        # Nếu fallback cũng rỗng, trả về hybrid (có thể rỗng)
        return merged[:top_k]

    return merged[:top_k]


if __name__ == "__main__":
    test_queries = [
        "Hình phạt cho tội tàng trữ trái phép chất ma tuý",
        "Nghệ sĩ nào bị bắt vì sử dụng ma tuý",
        "Luật phòng chống ma tuý 2021 quy định về cai nghiện",
        "xyzabc123nonsense",  # Query obscure → test fallback
    ]

    for q in test_queries:
        print(f"\nQuery: {q}")
        print("-" * 60)
        results = retrieve(q, top_k=3)
        for i, r in enumerate(results, 1):
            print(f"  {i}. [{r['score']:.4f}] [{r['source']}] {r['content'][:70]}...")
