from __future__ import annotations

import os
from typing import Final

import streamlit as st
from openai import OpenAI
from streamlit.errors import StreamlitSecretNotFoundError


DEFAULT_MODEL: Final[str] = "deepseek-v4-flash"
MAX_INPUT_WORDS: Final[int] = 200


def get_secret(name: str) -> str | None:
    try:
        secret_value = st.secrets[name]
    except (StreamlitSecretNotFoundError, KeyError, FileNotFoundError):
        secret_value = None
    if secret_value:
        return str(secret_value)
    return os.getenv(name)


def get_api_key() -> str | None:
    return get_secret("DEEPSEEK_API_KEY")


def get_model() -> str:
    return get_secret("DEEPSEEK_MODEL") or DEFAULT_MODEL


def build_prompt(idea: str, max_words: int) -> str:
    return f"""
You are a professional content writer.

Task:
- Write a complete article in English.
- The only inputs are the idea and the maximum word count.
- The article must be clear, readable, and include an introduction, body, and conclusion.
- The total length must not exceed {max_words} words.
- Do not include process explanations.
- Return only the final article content in Markdown format.

Idea:
{idea.strip()}
""".strip()


def generate_article(idea: str, max_words: int, api_key: str, model: str) -> str:
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You write polished Vietnamese articles and follow output constraints exactly.",
            },
            {
                "role": "user",
                "content": build_prompt(idea=idea, max_words=max_words),
            },
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content or ""


st.set_page_config(
    page_title="AI Article Writer",
    page_icon="",
    layout="centered",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@400;500;700&display=swap');

    :root {
        --paper: #f6f1e7;
        --ink: #1f1a17;
        --muted: #6f675e;
        --line: #d9d0c2;
        --accent: #8a2e24;
    }

    .stApp {
        background:
            linear-gradient(180deg, rgba(255,255,255,0.58), rgba(255,255,255,0.58)),
            radial-gradient(circle at top left, #fbf7ef, var(--paper));
        color: var(--ink);
    }

    .block-container {
        max-width: 760px;
        padding-top: 3rem;
        padding-bottom: 4rem;
    }

    h1, h2, h3, p, label, div, span, textarea, input, button {
        font-family: "Noto Serif JP", serif !important;
    }

    .jp-shell {
        border-top: 1px solid var(--line);
        border-bottom: 1px solid var(--line);
        padding: 1.4rem 0 1.2rem 0;
        margin-bottom: 2rem;
    }

    .jp-title {
        font-size: 2rem;
        font-weight: 600;
        letter-spacing: 0.02em;
        color: var(--ink);
        margin: 0;
    }

    .jp-subtitle {
        color: var(--muted);
        font-size: 0.98rem;
        margin-top: 0.35rem;
    }

    .stTextArea textarea,
    .stNumberInput input {
        background: rgba(255, 255, 255, 0.55) !important;
        border: 1px solid var(--line) !important;
        border-radius: 0 !important;
        color: var(--ink) !important;
    }

    .stTextArea textarea:focus,
    .stNumberInput input:focus {
        border-color: var(--accent) !important;
        box-shadow: none !important;
    }

    .stButton > button,
    .stDownloadButton > button {
        background: var(--ink) !important;
        color: #f8f3ea !important;
        border: 1px solid var(--ink) !important;
        border-radius: 0 !important;
        min-height: 2.9rem;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {
        background: var(--accent) !important;
        border-color: var(--accent) !important;
    }

    .stMarkdown h2 {
        border-top: 1px solid var(--line);
        padding-top: 1rem;
        margin-top: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <section class="jp-shell">
        <p class="jp-title">AI Article Writer</p>
        <p class="jp-subtitle">A minimal interface for turning an idea into a complete article.</p>
    </section>
    """,
    unsafe_allow_html=True,
)

idea = st.text_area(
    "Idea",
    placeholder="Example: Write an article about the benefits of email marketing for small businesses",
    height=180,
    max_chars=3000,
)
max_words = st.number_input(
    "Max words",
    min_value=100,
    max_value=5000,
    value=300,
    step=100,
)

api_key = get_api_key()
model = get_model()

st.caption(f"Model: `{model}`")

if st.button("Generate article", type="primary", use_container_width=True):
    if not api_key:
        st.error("DEEPSEEK_API_KEY was not found in Streamlit secrets or environment variables.")
    elif not idea.strip():
        st.error("Enter an idea before generating.")
    elif len(idea.split()) > MAX_INPUT_WORDS:
        st.error(f"The idea is too long. Keep it under {MAX_INPUT_WORDS} words.")
    else:
        with st.spinner("Generating article..."):
            try:
                article = generate_article(
                    idea=idea,
                    max_words=int(max_words),
                    api_key=api_key,
                    model=model,
                )
            except Exception as exc:  # noqa: BLE001
                st.exception(exc)
            else:
                st.subheader("Article")
                st.markdown(article)
                st.download_button(
                    "Download Markdown",
                    data=article,
                    file_name="article.md",
                    mime="text/markdown",
                    use_container_width=True,
                )
