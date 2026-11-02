"""Generación de respuestas en streaming con Ollama."""

from collections.abc import Iterator

from langchain_chroma import Chroma
from langchain_core.documents import Document

from rag.config import LLM_MODEL, OLLAMA_URL, TEMPERATURE
from rag.motor import recuperar
from rag.prompts import construir_mensajes


def limpiar_pregunta(texto: str) -> str | None:
    """Quita espacios sobrantes; devuelve None si la pregunta queda vacía."""
    limpio = (texto or "").strip()
    return limpio or None


def fuentes_numeradas(docs: list[Document]) -> list[str]:
    """Una línea '[n] titulo — fuente' por trozo, con la misma numeración que
    `construir_mensajes` (sin deduplicar: el [2] del texto es el [2] de la lista)."""
    return [
        f"[{n}] {d.metadata.get('titulo', '')} — {d.metadata.get('fuente', '')}"
        for n, d in enumerate(docs, start=1)
    ]


def responder_stream(
    base: Chroma,
    pregunta: str,
    tema: str,
    historial: list[tuple[str, str]],
    modelo: str = LLM_MODEL,
    temperatura: float = TEMPERATURE,
) -> tuple[list[Document], Iterator[str]]:
    """Recupera el contexto y devuelve (docs, stream de fragmentos de texto)."""
    docs = recuperar(base, pregunta, tema)
    mensajes = construir_mensajes(pregunta, docs, historial, tema)

    def _stream() -> Iterator[str]:
        # Import diferido: los tests y la UI sin generar no tocan Ollama.
        from langchain_ollama import ChatOllama

        llm = ChatOllama(model=modelo, base_url=OLLAMA_URL, temperature=temperatura)
        for chunk in llm.stream(mensajes):
            yield chunk.content

    return docs, _stream()
