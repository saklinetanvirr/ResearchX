import time

import streamlit as st

from chatbot import ResearchX
from config import APP_TITLE


st.set_page_config(
    page_title=APP_TITLE,
    page_icon="⟡",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------- Styling ----------
st.markdown(
    """
    <style>
    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
    }

    /* Centered ResearchX header */
    .researchx-header {
        text-align: center;
        margin: 1rem 0 2.5rem 0;
        padding: 0;
        border: none;
    }

    .researchx-header h1 {
        margin: 0;
        padding: 0;
        font-size: 3rem;
        font-weight: 700;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource
def get_pilot():
    return ResearchX()


pilot = get_pilot()


# ---------- Header ----------
st.markdown(
    f"""
    <div class="researchx-header">
        <h1>⟡ {APP_TITLE}</h1>
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------- Sidebar ----------
with st.sidebar:
    st.header("ResearchX")
    st.caption("Your AI assistant for AI/ML research exploration.")

    st.markdown("### Supported research modes")
    st.markdown(
        """
        - 📘 Concept Explanation
        - 🔎 Research Gap Exploration
        - 🧪 Research Methodology
        - 🗺️ Research Planning
        - 📄 Paper/Topic Analysis
        """
    )

    st.markdown("---")

    st.markdown("### Example questions")

    examples = [
        "What is Retrieval-Augmented Generation?",
        "What research gaps exist in RAG hallucination detection?",
        "How should I evaluate a RAG system?",
        "How can I turn an AI idea into a research plan?",
    ]

    for item in examples:
        st.caption(f"• {item}")

    st.markdown("---")

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# ---------- Helper: word-by-word streaming ----------
def stream_text(text):
    """
    Creates a ChatGPT-like typing effect by displaying
    the generated answer progressively.
    """

    words = text.split(" ")

    for i, word in enumerate(words):
        if i == 0:
            yield word
        else:
            yield " " + word

        # Controls typing speed
        time.sleep(0.025)


# ---------- Chat history ----------
if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:

    role = message["role"]

    with st.chat_message(
        role,
        avatar="🧑‍🎓" if role == "user" else "✨",
    ):

        if role == "user":
            st.markdown(message["content"])

        else:
            result = message["result"]

            # Previously generated answer
            st.markdown(result.answer)

            with st.expander("📋 Research Analysis", expanded=True):

                c1, c2, c3 = st.columns(3)

                c1.metric("Category", result.category)
                c2.metric("Difficulty", result.difficulty)

                c3.metric(
                    "Confidence",
                    f"{result.confidence:.0%}",
                )

                st.markdown("**📝 Summary**")
                st.write(result.summary)

                st.markdown("**🔑 Key Concepts**")
                st.write(", ".join(result.key_concepts))

                if result.research_directions:

                    st.markdown("**🚀 Research Directions**")

                    for direction in result.research_directions:
                        st.markdown(f"- {direction}")

                if result.follow_up_questions:

                    st.markdown("**❓ Follow-up Questions**")

                    for question in result.follow_up_questions:
                        st.markdown(f"- {question}")


# ---------- Input ----------
prompt = st.chat_input(
    "Ask a research question about AI, ML, Generative AI, or research methodology..."
)


if prompt:

    # Store user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    # Display user message
    with st.chat_message(
        "user",
        avatar="🧑‍🎓",
    ):
        st.markdown(prompt)


    # ---------- Generate Assistant Response ----------
    with st.chat_message(
        "assistant",
        avatar="✨",
    ):

        with st.status(
            "ResearchX is analyzing your question...",
            expanded=False,
        ):

            try:
                result = pilot.ask(prompt)

            except Exception as exc:

                st.error(
                    "I couldn't complete the request. "
                    "Please check the API configuration "
                    "or try again later."
                )

                st.exception(exc)
                st.stop()


        # ---------- Streaming Answer ----------
        st.write_stream(
            stream_text(result.answer)
        )


        # ---------- Research Analysis ----------
        with st.expander(
            "📋 Research Analysis",
            expanded=True,
        ):

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "Category",
                result.category,
            )

            c2.metric(
                "Difficulty",
                result.difficulty,
            )

            c3.metric(
                "Confidence",
                f"{result.confidence:.0%}",
            )


            st.markdown("**📝 Summary**")
            st.write(result.summary)


            st.markdown("**🔑 Key Concepts**")
            st.write(", ".join(result.key_concepts))


            if result.research_directions:

                st.markdown(
                    "**🚀 Research Directions**"
                )

                for direction in result.research_directions:
                    st.markdown(
                        f"- {direction}"
                    )


            if result.follow_up_questions:

                st.markdown(
                    "**❓ Follow-up Questions**"
                )

                for question in result.follow_up_questions:
                    st.markdown(
                        f"- {question}"
                    )


    # ---------- Save Assistant Response ----------
    st.session_state.messages.append(
        {
            "role": "assistant",
            "result": result,
        }
    )