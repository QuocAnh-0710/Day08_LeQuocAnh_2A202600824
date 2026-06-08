"""
DrugLaw RAG Chatbot — Group Project
Streamlit UI với conversation memory, citation, và source viewer.
"""

import sys
from pathlib import Path

import streamlit as st

# Thêm project root vào sys.path
sys.path.insert(0, str(Path(__file__).parent))

# =====================================================================
# Page config
# =====================================================================
st.set_page_config(
    page_title="DrugLaw RAG Chatbot",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =====================================================================
# CSS tuỳ chỉnh
# =====================================================================
st.markdown("""
<style>
.badge-legal {
    background: #c0392b; color: #fff !important;
    padding: 2px 8px; border-radius: 10px;
    font-size: 0.72em; font-weight: 600; margin-left: 6px; vertical-align: middle;
}
.badge-news {
    background: #1a7f4b; color: #fff !important;
    padding: 2px 8px; border-radius: 10px;
    font-size: 0.72em; font-weight: 600; margin-left: 6px; vertical-align: middle;
}
</style>
""", unsafe_allow_html=True)

# =====================================================================
# Sidebar
# =====================================================================
with st.sidebar:
    st.title("⚖️ DrugLaw Chatbot")
    st.caption("RAG Pipeline v2 — Day 8")

    st.divider()

    top_k = st.slider("Số chunks retrieval (top_k)", 3, 10, 5)
    score_threshold = st.slider("Ngưỡng fallback PageIndex", 0.05, 0.50, 0.15, 0.01)
    use_memory = st.toggle("Conversation memory", value=True)

    st.divider()
    st.markdown("**Pipeline:**")
    st.markdown("🔍 Semantic Search (ChromaDB)")
    st.markdown("📝 Lexical Search (BM25)")
    st.markdown("🔀 RRF Reranking")
    st.markdown("🤖 Claude Generation")

    st.divider()
    if st.button("🗑️ Xoá lịch sử chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.caption("Nhóm bài tập — VinUni AI Lab Day 8")

# =====================================================================
# Session state
# =====================================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# =====================================================================
# Header
# =====================================================================
st.title("⚖️ Hỏi đáp Pháp luật Ma tuý & Tin tức Nghệ sĩ")
st.caption(
    "Chatbot RAG trả lời câu hỏi về **pháp luật Việt Nam về ma tuý** và "
    "**tin tức nghệ sĩ liên quan** — mọi thông tin đều có trích dẫn nguồn."
)

# =====================================================================
# Gợi ý câu hỏi (lần đầu truy cập)
# =====================================================================
if not st.session_state.messages:
    st.markdown("### 💡 Thử hỏi:")
    cols = st.columns(2)
    example_questions = [
        "Hình phạt tàng trữ trái phép heroin theo Điều 249 là bao nhiêu năm tù?",
        "Ca sĩ Chi Dân bị đề nghị truy tố về tội gì?",
        "Miu Lê bị bắt trong hoàn cảnh nào?",
        "Cai nghiện ma tuý bắt buộc kéo dài bao lâu?",
        "Rapper Bình Gold bị bắt vì lý do gì?",
        "Luật Phòng chống ma tuý 2021 nghiêm cấm những hành vi nào?",
    ]
    for i, q in enumerate(example_questions):
        col = cols[i % 2]
        if col.button(q, key=f"ex_{i}", use_container_width=True):
            st.session_state.pending_question = q
            st.rerun()

# =====================================================================
# Hiển thị lịch sử hội thoại
# =====================================================================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

        if msg["role"] == "assistant" and msg.get("sources"):
            sources = msg["sources"]
            retrieval_src = msg.get("retrieval_source", "hybrid")

            with st.expander(
                f"📚 {len(sources)} nguồn được sử dụng | via `{retrieval_src}`",
                expanded=False,
            ):
                for i, src in enumerate(sources, 1):
                    meta = src.get("metadata", {})
                    doc_type = meta.get("type", "unknown")
                    source_name = meta.get("source", f"Source {i}").replace(".md", "")
                    score = src.get("score", 0)
                    is_legal = doc_type == "legal"
                    badge_class = "badge-legal" if is_legal else "badge-news"
                    icon = "📜" if is_legal else "📰"
                    label = "Pháp luật" if is_legal else "Tin tức"
                    snippet = src["content"][:220]
                    if len(src["content"]) > 220:
                        snippet += "…"

                    with st.container(border=True):
                        col_title, col_score = st.columns([5, 1])
                        with col_title:
                            st.markdown(
                                f'{icon} **[{i}] {source_name}** '
                                f'<span class="{badge_class}">{label}</span>',
                                unsafe_allow_html=True,
                            )
                        with col_score:
                            st.caption(f"🎯 {score:.3f}")
                        st.caption(snippet)

# =====================================================================
# Hàm build query với conversation context
# =====================================================================
def build_query_with_memory(user_input: str) -> str:
    """Thêm context hội thoại vào query nếu bật conversation memory."""
    if not use_memory or len(st.session_state.messages) < 2:
        return user_input

    # Lấy tối đa 2 lượt trước (Q+A)
    recent = []
    history = st.session_state.messages[-4:]  # last 4 = 2 Q+A pairs
    for m in history:
        if m["role"] == "user":
            recent.append(f"Q: {m['content']}")
        elif m["role"] == "assistant":
            recent.append(f"A: {m['content'][:200]}...")

    context_str = "\n".join(recent)
    return (
        f"[Ngữ cảnh hội thoại trước]\n{context_str}\n\n"
        f"[Câu hỏi hiện tại]\n{user_input}"
    )


# =====================================================================
# Xử lý câu hỏi từ button gợi ý
# =====================================================================
if "pending_question" in st.session_state:
    user_input = st.session_state.pop("pending_question")
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    process_query = True
else:
    process_query = False
    user_input = None

# =====================================================================
# Chat input
# =====================================================================
chat_input = st.chat_input("Nhập câu hỏi về pháp luật ma tuý hoặc nghệ sĩ liên quan...")

if chat_input:
    user_input = chat_input
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    process_query = True

# =====================================================================
# Generate response
# =====================================================================
if process_query and user_input:
    from src.task10_generation import generate_with_citation

    with st.chat_message("assistant"):
        status_placeholder = st.empty()

        with st.spinner("🔍 Đang tìm kiếm tài liệu liên quan..."):
            query_with_context = build_query_with_memory(user_input)
            status_placeholder.info("📚 Đang chạy hybrid search (semantic + BM25)...")

            result = generate_with_citation(query_with_context, top_k=top_k)

        status_placeholder.empty()

        answer = result["answer"]
        sources = result["sources"]
        retrieval_source = result.get("retrieval_source", "hybrid")

        st.markdown(answer)

        if sources:
            with st.expander(
                f"📚 {len(sources)} nguồn được sử dụng | via `{retrieval_source}`",
                expanded=True,
            ):
                for i, src in enumerate(sources, 1):
                    meta = src.get("metadata", {})
                    doc_type = meta.get("type", "unknown")
                    source_name = meta.get("source", f"Source {i}").replace(".md", "")
                    score = src.get("score", 0)
                    is_legal = doc_type == "legal"
                    badge_class = "badge-legal" if is_legal else "badge-news"
                    icon = "📜" if is_legal else "📰"
                    label = "Pháp luật" if is_legal else "Tin tức"
                    snippet = src["content"][:220]
                    if len(src["content"]) > 220:
                        snippet += "…"

                    with st.container(border=True):
                        col_title, col_score = st.columns([5, 1])
                        with col_title:
                            st.markdown(
                                f'{icon} **[{i}] {source_name}** '
                                f'<span class="{badge_class}">{label}</span>',
                                unsafe_allow_html=True,
                            )
                        with col_score:
                            st.caption(f"🎯 {score:.3f}")
                        st.caption(snippet)
        else:
            st.warning("⚠️ Không tìm thấy tài liệu liên quan.")

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": sources,
        "retrieval_source": retrieval_source,
    })
