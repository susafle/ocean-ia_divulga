"""Estilos y cabecera de DivulgaRAG. Sin recursos externos: funciona sin conexión."""

import streamlit as st

from rag.config import TEMAS

_CSS_BASE = """
html, body, .stApp, [class*="st-"]:not([data-testid="stIconMaterial"]) {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
        "Helvetica Neue", Arial, "Apple Color Emoji", "Segoe UI Emoji", sans-serif;
}
.stApp { background: #F4F9FC; color: #0B2540; font-size: 1.15rem; }
p, li, label, .stMarkdown, [data-testid="stChatMessageContent"] {
    font-size: 1.15rem; line-height: 1.6; color: #0B2540;
}
.block-container { max-width: 1200px; padding-top: 1.5rem; }

.cabecera-oceano {
    background: linear-gradient(135deg, #0B2C5F 0%, #14609E 55%, #1B8FB5 100%);
    color: #FFFFFF; border-radius: 1.2rem; padding: 1.4rem 2rem;
    margin-bottom: 1.5rem; box-shadow: 0 4px 14px rgba(11, 44, 95, 0.25);
}
.cabecera-oceano h1 {
    color: #FFFFFF; font-size: 2.6rem; margin: 0; padding: 0; line-height: 1.2;
}
.cabecera-oceano p {
    color: #E3F2FA; font-size: 1.2rem; margin: 0.3rem 0 0 0;
}

.titulo-portada {
    font-size: 2.1rem; font-weight: 700; color: #0B2C5F;
    text-align: center; margin: 0.5rem 0 1.2rem 0;
}

.stButton > button, .stFormSubmitButton > button {
    font-size: 1.15rem; padding: 0.75rem 1.2rem; border-radius: 0.9rem;
    border: 2px solid #14609E; color: #0B2540; background: #FFFFFF;
    min-height: 3rem; font-weight: 600; transition: transform 0.1s;
}
.stButton > button:hover { transform: translateY(-2px); border-color: #0B2C5F; }
.stButton > button p { font-size: 1.15rem; }

/* Tarjetas de la portada: botón alto con emoji grande, título y subtítulo */
[class*="st-key-tarjeta-"] .stButton > button {
    min-height: 11rem; border-radius: 1.2rem; border-width: 3px;
    white-space: pre-line; line-height: 1.35; padding: 1rem;
}
[class*="st-key-tarjeta-"] .stButton > button p {
    font-size: 1.3rem; white-space: pre-line;
}
[class*="st-key-tarjeta-"] .stButton > button p::first-line { font-size: 3.4rem; }
[class*="st-key-tarjeta-"] img {
    border-radius: 1.2rem; aspect-ratio: 16 / 9; object-fit: cover;
}
"""


def _css_tarjetas() -> str:
    """Una regla por tema: tinta la tarjeta con su color pastel."""
    return "\n".join(
        f".st-key-tarjeta-{t.slug} .stButton > button "
        f"{{ background: {t.color}; border-color: #14609E; }}"
        for t in TEMAS.values()
    )


def inyectar_css() -> None:
    """Inyecta el CSS de la app (una sola vez por ejecución)."""
    st.markdown(f"<style>{_CSS_BASE}\n{_css_tarjetas()}</style>", unsafe_allow_html=True)


def cabecera() -> None:
    """Banner superior con degradado azul marino."""
    st.markdown(
        '<div class="cabecera-oceano">'
        "<h1>🌊🤖 Pregúntale al océano</h1>"
        "<p>Investigación OCEAN-IA · Susana Flecha · ICMAN-CSIC</p>"
        "</div>",
        unsafe_allow_html=True,
    )
