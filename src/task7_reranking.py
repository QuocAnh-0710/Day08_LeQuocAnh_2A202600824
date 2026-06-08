"""
Task 7 — Reranking Module.

Phương pháp: RRF (Reciprocal Rank Fusion)
    RRF(d) = Σ_r 1 / (k + rank_r(d))

    - k = 60 (Cormack et al. 2009): smoothing constant
    - Gộp kết quả từ nhiều ranker không cần calibration score
    - Robust: không bị ảnh hưởng bởi scale khác nhau giữa BM25 và cosine score
    - Đơn giản, không cần API key, hiệu quả cao trong thực tế

Ngoài ra cung cấp sẵn rerank_rrf và rerank_cross_encoder (nếu có API key Jina).
"""

from typing import Optional


def rerank_rrf(
    ranked_lists: list[list[dict]], top_k: int = 5, k: int = 60
) -> list[dict]:
    """
    Reciprocal Rank Fusion — gộp kết quả từ nhiều ranker.

    RRF(d) = Σ 1 / (k + rank_r(d))

    Args:
        ranked_lists: List of ranked result lists (mỗi list từ 1 ranker)
        top_k: Số kết quả cuối cùng
        k: Smoothing constant (mặc định 60 từ paper gốc)

    Returns:
        List of top_k candidates sorted by RRF score descending.
    """
    rrf_scores: dict[str, float] = {}
    content_map: dict[str, dict] = {}

    for ranked_list in ranked_lists:
        for rank, item in enumerate(ranked_list, 1):
            key = item["content"][:200]  # Dùng prefix làm key (tránh key quá dài)
            rrf_scores[key] = rrf_scores.get(key, 0.0) + 1.0 / (k + rank)
            content_map[key] = item

    sorted_items = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)

    results = []
    for content_key, score in sorted_items[:top_k]:
        item = content_map[content_key].copy()
        item["score"] = round(score, 6)
        results.append(item)

    return results


def rerank_cross_encoder(
    query: str,
    candidates: list[dict],
    top_k: int = 5,
    api_key: str = "",
) -> list[dict]:
    """
    Rerank sử dụng Jina Reranker API (nếu có API key).
    Fallback sang RRF nếu không có API key.
    """
    if not api_key:
        # Fallback: trả về candidates theo score hiện tại
        sorted_candidates = sorted(candidates, key=lambda x: x.get("score", 0), reverse=True)
        return sorted_candidates[:top_k]

    import requests

    try:
        response = requests.post(
            "https://api.jina.ai/v1/rerank",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": "jina-reranker-v2-base-multilingual",
                "query": query,
                "documents": [c["content"] for c in candidates],
                "top_n": top_k,
            },
            timeout=30,
        )
        response.raise_for_status()
        reranked = response.json()["results"]
        return [
            {**candidates[r["index"]], "score": round(r["relevance_score"], 4)}
            for r in reranked
        ]
    except Exception as e:
        print(f"  ⚠ Jina API error: {e}, fallback sang score sort")
        sorted_candidates = sorted(candidates, key=lambda x: x.get("score", 0), reverse=True)
        return sorted_candidates[:top_k]


def rerank_mmr(
    candidates: list[dict],
    top_k: int = 5,
    lambda_param: float = 0.7,
) -> list[dict]:
    """
    Maximal Marginal Relevance — giảm trùng lặp, tăng diversity.

    MMR = λ * score - (1-λ) * max_sim_to_selected

    Dùng score hiện có làm proxy cho relevance (không cần embedding).
    """
    if not candidates:
        return []

    selected_indices = []
    remaining = list(range(len(candidates)))

    for _ in range(min(top_k, len(candidates))):
        best_idx = None
        best_mmr = float("-inf")

        for idx in remaining:
            relevance = candidates[idx].get("score", 0.0)

            # Penalty: trùng text với các item đã chọn
            max_overlap = 0.0
            for sel_idx in selected_indices:
                # Tính jaccard overlap đơn giản
                words_a = set(candidates[idx]["content"].lower().split())
                words_b = set(candidates[sel_idx]["content"].lower().split())
                if words_a | words_b:
                    overlap = len(words_a & words_b) / len(words_a | words_b)
                    max_overlap = max(max_overlap, overlap)

            mmr_score = lambda_param * relevance - (1 - lambda_param) * max_overlap

            if mmr_score > best_mmr:
                best_mmr = mmr_score
                best_idx = idx

        if best_idx is not None:
            selected_indices.append(best_idx)
            remaining.remove(best_idx)

    return [candidates[i] for i in selected_indices]


# =============================================================================
# Unified interface
# =============================================================================

def rerank(
    query: str,
    candidates: list[dict],
    top_k: int = 5,
    method: str = "rrf",
) -> list[dict]:
    """
    Unified reranking interface.

    Args:
        query: Câu truy vấn
        candidates: Danh sách candidates từ retrieval
        top_k: Số kết quả sau rerank
        method: 'rrf' | 'mmr' | 'cross_encoder'

    Returns:
        List of top_k reranked candidates.
    """
    if not candidates:
        return []

    if method == "rrf":
        # RRF cần ranked_lists — wrap candidates thành 1 list
        return rerank_rrf([candidates], top_k=top_k)
    elif method == "mmr":
        return rerank_mmr(candidates, top_k=top_k)
    elif method == "cross_encoder":
        import os
        api_key = os.getenv("JINA_API_KEY", "")
        return rerank_cross_encoder(query, candidates, top_k=top_k, api_key=api_key)
    else:
        raise ValueError(f"Unknown rerank method: {method}")


if __name__ == "__main__":
    dummy_candidates = [
        {"content": "Điều 249: Tội tàng trữ trái phép chất ma tuý — phạt tù 1-5 năm", "score": 0.8, "metadata": {}},
        {"content": "Nghệ sĩ X bị bắt vì sử dụng ma tuý tại TP.HCM", "score": 0.7, "metadata": {}},
        {"content": "Hình phạt tù từ 2-7 năm cho tội tàng trữ heroin", "score": 0.6, "metadata": {}},
        {"content": "Python programming tutorial for beginners", "score": 0.4, "metadata": {}},
        {"content": "Luật phòng chống ma tuý 2021 nghiêm cấm sử dụng", "score": 0.75, "metadata": {}},
    ]

    print("=== RRF Reranking ===")
    results = rerank("hình phạt tàng trữ ma tuý", dummy_candidates, top_k=3, method="rrf")
    for r in results:
        print(f"  [{r['score']:.4f}] {r['content'][:70]}")

    print("\n=== MMR Reranking ===")
    results = rerank("hình phạt tàng trữ ma tuý", dummy_candidates, top_k=3, method="mmr")
    for r in results:
        print(f"  [{r['score']:.3f}] {r['content'][:70]}")
