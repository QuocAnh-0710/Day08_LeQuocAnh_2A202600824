"""
Task 10 — Generation Có Citation.

Pipeline:
    1. Retrieve chunks (Task 9)
    2. Reorder để tránh "lost in the middle" (Liu et al. 2023)
    3. Format context với source labels
    4. Call LLM (Anthropic Claude) với SYSTEM_PROMPT yêu cầu citation
    5. Return answer + sources

Cấu hình generation:
    - top_k=5: đủ evidence mà không gây lost in the middle
    - temperature=0.3: RAG cần factual, ít sáng tạo
    - max_tokens=1024: đủ cho câu trả lời đầy đủ có citation
"""

import os

from dotenv import load_dotenv

load_dotenv()

from .task9_retrieval_pipeline import retrieve

# =============================================================================
# CONFIGURATION
# =============================================================================

TOP_K = 5          # Số chunks đưa vào context
TEMPERATURE = 0.3  # Thấp = factual, không hallucinate
MAX_TOKENS = 1024  # Đủ cho câu trả lời đầy đủ

SYSTEM_PROMPT = """Trả lời câu hỏi bằng tiếng Việt một cách toàn diện.
Với mỗi thông tin, ngay lập tức chèn citation trong ngoặc vuông dẫn đến nguồn cụ thể
(ví dụ: [Luật Phòng chống ma tuý 2021, Điều 3] hoặc [VnExpress, 2024]).

Nếu thông tin không có trong context được cung cấp, hãy nói:
'Tôi không thể xác minh thông tin này từ nguồn hiện có' thay vì đoán.

Quy tắc:
- Chỉ dùng thông tin từ context được cung cấp
- Mọi thông tin thực tế PHẢI có citation
- Nếu context không đủ, nói rõ
- Trả lời có cấu trúc rõ ràng"""


# =============================================================================
# DOCUMENT REORDERING (tránh lost in the middle)
# =============================================================================

def reorder_for_llm(chunks: list[dict]) -> list[dict]:
    """
    Sắp xếp chunks để tránh "lost in the middle" effect.

    LLM nhớ tốt đầu và cuối prompt, quên thông tin ở giữa.
    Strategy: quan trọng nhất ở đầu, kém nhất ở giữa, quan trọng nhì ở cuối.

    Input (by score):   [1, 2, 3, 4, 5]  (index 0 = best)
    Output:             [1, 3, 5, 4, 2]
    → best ở đầu, worst ở giữa, second-best ở cuối

    Args:
        chunks: List sorted by score descending

    Returns:
        Reordered list để maximize LLM attention.
    """
    if len(chunks) <= 2:
        return chunks

    # Tách thành odd và even indices
    # Odd positions (0, 2, 4, ...) → đặt ở đầu (ascending)
    # Even positions (1, 3, 5, ...) → đặt ở cuối (descending — quan trọng hơn cuối)
    first_half = chunks[::2]           # [0, 2, 4, ...]  — important first
    second_half = chunks[1::2][::-1]   # [..3, 1] reversed — second-best last

    return first_half + second_half


# =============================================================================
# CONTEXT FORMATTING
# =============================================================================

def format_context(chunks: list[dict]) -> str:
    """
    Format chunks thành context string cho prompt.
    Mỗi chunk có label source để LLM cite.

    Returns:
        Formatted context string với source labels.
    """
    context_parts = []
    for i, chunk in enumerate(chunks, 1):
        metadata = chunk.get("metadata", {})
        source = metadata.get("source", f"Source {i}")
        # Loại bỏ extension để label gọn hơn
        source_label = source.replace(".md", "").replace(".docx", "")
        doc_type = metadata.get("type", "unknown")

        context_parts.append(
            f"[Document {i} | Source: {source_label} | Type: {doc_type}]\n"
            f"{chunk['content']}"
        )

    return "\n\n---\n\n".join(context_parts)


# =============================================================================
# GENERATION
# =============================================================================

def generate_with_citation(query: str, top_k: int = TOP_K) -> dict:
    """
    End-to-end RAG generation có citation dùng Anthropic Claude.

    Returns:
        {
            'answer': str,           # Câu trả lời có citation
            'sources': list[dict],   # Các chunks đã dùng
            'retrieval_source': str  # 'hybrid' hoặc 'pageindex'
        }
    """
    # Step 1: Retrieve
    chunks = retrieve(query, top_k=top_k)

    if not chunks:
        return {
            "answer": "Tôi không thể xác minh thông tin này từ nguồn hiện có.",
            "sources": [],
            "retrieval_source": "none",
        }

    # Step 2: Reorder để tránh lost in the middle
    reordered = reorder_for_llm(chunks)

    # Step 3: Format context
    context = format_context(reordered)

    # Step 4: Build prompt
    user_message = (
        f"Context:\n{context}\n\n"
        f"---\n\n"
        f"Câu hỏi: {query}"
    )

    # Step 5: Call LLM
    retrieval_source = chunks[0].get("source", "hybrid") if chunks else "none"

    try:
        from groq import Groq

        api_key = os.getenv("GROQ_API_KEY", "")
        if not api_key:
            return {
                "answer": (
                    "GROQ_API_KEY chưa được set. Điền key vào file .env.\n\n"
                    "Context đã retrieve:\n\n" + context[:500] + "..."
                ),
                "sources": chunks,
                "retrieval_source": retrieval_source,
            }

        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # Free, nhanh, đủ tốt cho RAG
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
        )
        answer = response.choices[0].message.content

    except ImportError:
        answer = f"[groq package chưa cài: pip install groq]\n\nContext:\n{context[:800]}"
    except Exception as e:
        answer = f"[Generation error: {e}]\n\nContext:\n{context[:800]}"

    return {
        "answer": answer,
        "sources": chunks,
        "retrieval_source": retrieval_source,
    }


if __name__ == "__main__":
    test_queries = [
        "Hình phạt cho tội tàng trữ trái phép chất ma tuý theo pháp luật Việt Nam?",
        "Những nghệ sĩ nào đã bị bắt vì liên quan tới ma tuý?",
    ]

    for q in test_queries:
        print(f"\n{'=' * 70}")
        print(f"Q: {q}")
        print("=" * 70)
        result = generate_with_citation(q)
        print(f"\nA: {result['answer'][:500]}")
        print(f"\n[Sources: {len(result['sources'])} chunks | via {result['retrieval_source']}]")
