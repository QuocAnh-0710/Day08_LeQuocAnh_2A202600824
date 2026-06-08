"""
Task 4 — Chunking & Indexing vào Vector Store.

Chunking strategy: RecursiveCharacterTextSplitter
- CHUNK_SIZE=500: Phù hợp với văn bản pháp luật tiếng Việt, đủ context mà không quá dài
- CHUNK_OVERLAP=50: 10% overlap giúp tránh mất context ở ranh giới chunk
- Separators: ưu tiên tách theo paragraph/câu để giữ ngữ nghĩa

Embedding model: sentence-transformers/all-MiniLM-L6-v2 (384 dim)
- Nhẹ, nhanh, hỗ trợ tiếng Việt đủ tốt cho demo
- Đã cài sẵn không cần download nhiều

Vector Store: ChromaDB (local persistence)
- Không cần Docker, dễ setup
- Hỗ trợ semantic search built-in
- Corpus cũng được lưu sang JSON để Task 6 (BM25) dùng lại
"""

import json
from pathlib import Path

STANDARDIZED_DIR = Path(__file__).parent.parent / "data" / "standardized"
CHROMA_DIR = Path(__file__).parent.parent / "data" / "chroma_db"
CORPUS_FILE = Path(__file__).parent.parent / "data" / "corpus.json"

# =============================================================================
# CONFIGURATION
# =============================================================================

# RecursiveCharacterTextSplitter: an toàn, robust với mọi loại text
CHUNK_SIZE = 500        # 500 chars phù hợp cho văn bản pháp luật
CHUNK_OVERLAP = 50      # 10% overlap tránh mất context ở ranh giới
CHUNKING_METHOD = "recursive"

# all-MiniLM-L6-v2: nhẹ (80MB), nhanh, đủ tốt cho tiếng Việt
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
EMBEDDING_DIM = 384

VECTOR_STORE = "chromadb"
COLLECTION_NAME = "DrugLawDocs"


# =============================================================================
# IMPLEMENTATION
# =============================================================================

def load_documents() -> list[dict]:
    """
    Đọc toàn bộ markdown files từ data/standardized/.

    Returns:
        List of {'content': str, 'metadata': {'source': str, 'type': str}}
    """
    documents = []
    if not STANDARDIZED_DIR.exists():
        return documents

    for md_file in STANDARDIZED_DIR.rglob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        if len(content.strip()) < 100:
            continue
        doc_type = "legal" if "legal" in str(md_file) else "news"
        documents.append({
            "content": content,
            "metadata": {
                "source": md_file.name,
                "type": doc_type,
                "path": str(md_file.relative_to(STANDARDIZED_DIR)),
            },
        })

    return documents


def chunk_documents(documents: list[dict]) -> list[dict]:
    """
    Chunk documents sử dụng RecursiveCharacterTextSplitter.

    Returns:
        List of {'content': str, 'metadata': dict} — mỗi item là 1 chunk
    """
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""],
    )

    chunks = []
    for doc in documents:
        splits = splitter.split_text(doc["content"])
        for i, chunk_text in enumerate(splits):
            if len(chunk_text.strip()) < 20:
                continue
            chunks.append({
                "content": chunk_text.strip(),
                "metadata": {**doc["metadata"], "chunk_index": i},
            })

    return chunks


def get_chroma_client():
    """Kết nối ChromaDB persistent client."""
    import chromadb

    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return client


def get_embedding_function():
    """Trả về embedding function cho ChromaDB."""
    from chromadb.utils import embedding_functions

    return embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=EMBEDDING_MODEL
    )


def index_to_vectorstore(chunks: list[dict]):
    """Lưu chunks vào ChromaDB với embedding."""
    client = get_chroma_client()
    ef = get_embedding_function()

    # Xóa collection cũ nếu có để tránh duplicate
    try:
        client.delete_collection(name=COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        embedding_function=ef,
        metadata={"hnsw:space": "cosine"},
    )

    # Batch insert
    batch_size = 50
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i : i + batch_size]
        collection.add(
            documents=[c["content"] for c in batch],
            metadatas=[c["metadata"] for c in batch],
            ids=[f"chunk_{i + j}" for j in range(len(batch))],
        )

    return collection


def save_corpus_for_bm25(chunks: list[dict]):
    """Lưu corpus ra JSON để Task 6 (BM25) dùng."""
    CORPUS_FILE.parent.mkdir(parents=True, exist_ok=True)
    CORPUS_FILE.write_text(
        json.dumps(chunks, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def run_pipeline():
    """Chạy toàn bộ pipeline: load → chunk → index."""
    print("=" * 60)
    print("Task 4: Chunking & Indexing")
    print(f"  Chunking: {CHUNKING_METHOD} (size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})")
    print(f"  Embedding: {EMBEDDING_MODEL} (dim={EMBEDDING_DIM})")
    print(f"  Vector Store: {VECTOR_STORE}")
    print("=" * 60)

    docs = load_documents()
    print(f"\n✓ Loaded {len(docs)} documents")
    if not docs:
        print("  ⚠ Không có documents, chạy Task 1-3 trước!")
        return

    chunks = chunk_documents(docs)
    print(f"✓ Created {len(chunks)} chunks")

    print("✓ Indexing to ChromaDB (sẽ mất ít phút lần đầu)...")
    index_to_vectorstore(chunks)
    print(f"  → Saved to: {CHROMA_DIR}")

    save_corpus_for_bm25(chunks)
    print(f"✓ Saved corpus to: {CORPUS_FILE}")


if __name__ == "__main__":
    run_pipeline()
