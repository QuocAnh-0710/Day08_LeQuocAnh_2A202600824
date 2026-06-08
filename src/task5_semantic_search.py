"""
Task 5 — Semantic Search Module.

Dense retrieval sử dụng ChromaDB + all-MiniLM-L6-v2 embeddings.
Query embedding → cosine similarity → top_k results sorted descending.
"""

from pathlib import Path

_CHROMA_DIR = Path(__file__).parent.parent / "data" / "chroma_db"
_COLLECTION_NAME = "DrugLawDocs"
_EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Lazy-load để tránh import chậm khi test
_collection = None


def _get_collection():
    global _collection
    if _collection is None:
        import chromadb
        from chromadb.utils import embedding_functions

        if not _CHROMA_DIR.exists():
            raise RuntimeError(
                "ChromaDB chưa được tạo. Chạy task4_chunking_indexing.run_pipeline() trước."
            )

        client = chromadb.PersistentClient(path=str(_CHROMA_DIR))
        ef = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=_EMBEDDING_MODEL
        )
        _collection = client.get_collection(
            name=_COLLECTION_NAME, embedding_function=ef
        )
    return _collection


def semantic_search(query: str, top_k: int = 10) -> list[dict]:
    """
    Tìm kiếm ngữ nghĩa sử dụng vector cosine similarity.

    Args:
        query: Câu truy vấn
        top_k: Số lượng kết quả tối đa

    Returns:
        List of {'content': str, 'score': float, 'metadata': dict}
        Sorted by score descending.
    """
    collection = _get_collection()

    results = collection.query(
        query_texts=[query],
        n_results=min(top_k, collection.count()),
        include=["documents", "metadatas", "distances"],
    )

    output = []
    if results["documents"] and results["documents"][0]:
        for doc, meta, dist in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        ):
            # ChromaDB distance (cosine) → similarity: score = 1 - distance
            score = max(0.0, 1.0 - dist)
            output.append({
                "content": doc,
                "score": round(score, 4),
                "metadata": meta or {},
            })

    # Đảm bảo sorted descending
    output.sort(key=lambda x: x["score"], reverse=True)
    return output[:top_k]


if __name__ == "__main__":
    test_queries = [
        "hình phạt cho tội tàng trữ ma tuý",
        "cai nghiện ma tuý bắt buộc",
        "nghệ sĩ bị bắt vì ma tuý",
    ]
    for q in test_queries:
        print(f"\nQuery: {q}")
        results = semantic_search(q, top_k=3)
        for r in results:
            print(f"  [{r['score']:.3f}] {r['content'][:80]}...")
