"""Pregúntale al océano: app de taller (Streamlit, RAG local con Ollama)."""

import streamlit as st

from interfaz import chat, estilos, portada, profe
from rag import motor
from rag.config import TEMAS

st.set_page_config(
    page_title="Pregúntale al océano",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="collapsed",
)
estilos.inyectar_css()
estilos.cabecera()

if not profe.ollama_disponible():
    st.error(
        "No encuentro Ollama. Ábrelo o ejecuta `ollama serve` en una terminal "
        "y recarga la página."
    )
    st.stop()

if st.session_state.get("_base") is None:
    try:
        st.session_state["_base"] = motor.abrir_base()
    except FileNotFoundError:
        st.error("Falta la base: ejecuta .venv/bin/python ingesta.py")
        st.stop()
base = st.session_state["_base"]

ajustes = profe.render()

slug = st.session_state.get("tema")
if slug in TEMAS:
    chat.render(base, TEMAS[slug], ajustes["modelo"], ajustes["temperatura"])
else:
    portada.render()
