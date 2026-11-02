"""Modo profe (barra lateral): modelo, temperatura, reinicio, re-indexado y tablet."""

import json
import socket
import urllib.request
from io import BytesIO

import streamlit as st

from rag.config import BASE_DIR, CORPUS_DIR, EMBEDDING_MODEL, LLM_MODEL, LLM_MODEL_GRANDE, OLLAMA_URL, TEMPERATURE


def _tags() -> dict:
    with urllib.request.urlopen(f"{OLLAMA_URL}/api/tags", timeout=3) as r:
        return json.load(r)


def ollama_disponible() -> bool:
    """True si el servidor de Ollama responde."""
    try:
        _tags()
        return True
    except Exception:
        return False


def modelos_instalados() -> list[str]:
    """Nombres de los modelos instalados en Ollama (vacío si no responde)."""
    try:
        return [m["name"] for m in _tags().get("models", [])]
    except Exception:
        return []


def ip_local() -> str:
    """IP de la máquina en la red local (127.0.0.1 si no se puede averiguar)."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))
        return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        s.close()


def _qr_png(url: str) -> bytes | None:
    try:
        import qrcode  # opcional
    except ImportError:
        return None
    buf = BytesIO()
    qrcode.make(url).save(buf, format="PNG")
    return buf.getvalue()


def _reindexar() -> None:
    from langchain_ollama import OllamaEmbeddings

    from ingesta import construir_base

    emb = OllamaEmbeddings(model=EMBEDDING_MODEL, base_url=OLLAMA_URL)
    with st.spinner("Re-indexando el corpus… (puede tardar un par de minutos)"):
        try:
            construir_base(CORPUS_DIR, BASE_DIR, emb)
        except Exception as e:
            st.error(f"No se pudo re-indexar: {e}")
            return
    st.session_state.pop("_base", None)
    st.success("Corpus re-indexado.")


def render() -> dict:
    """Dibuja el panel del profe y devuelve {'modelo', 'temperatura'}."""
    with st.sidebar:
        st.header("🧑‍🏫 Modo profe")
        opciones = [LLM_MODEL]
        if any(m == LLM_MODEL_GRANDE or m.startswith(LLM_MODEL_GRANDE + ":") for m in modelos_instalados()):
            opciones.append(LLM_MODEL_GRANDE)
        modelo = st.selectbox("Modelo", opciones, index=0)
        temperatura = st.slider("Temperatura", 0.0, 1.0, TEMPERATURE, 0.05)
        if st.button("Reiniciar conversación", key="reiniciar"):
            st.session_state["historial"] = {}
            st.session_state["tema"] = None
            st.rerun()
        if st.button("Re-indexar corpus", key="reindexar"):
            _reindexar()
        puerto = st.get_option("server.port") or 8501
        with st.expander("📱 Conectar una tablet", expanded=False):
            url = f"http://{ip_local()}:{puerto}"
            st.code(url, language=None)
            png = _qr_png(url)
            if png:
                st.image(png, width=200)
    return {"modelo": modelo, "temperatura": temperatura}
