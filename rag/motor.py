"""Motor de recuperación de DivulgaRAG: búsqueda por tema con apoyo global."""

from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_ollama import OllamaEmbeddings

from rag.config import BASE_DIR, COLECCION, EMBEDDING_MODEL, K_GLOBAL, K_TEMA, OLLAMA_URL


def abrir_base(base_dir: Path = BASE_DIR, embeddings: Embeddings | None = None) -> Chroma:
    """Abre la base Chroma persistida; falla con un mensaje claro si no existe."""
    base_dir = Path(base_dir)
    if not base_dir.exists():
        raise FileNotFoundError(
            f"No existe la base en '{base_dir}'. Ejecuta primero la ingesta: .venv/bin/python ingesta.py"
        )
    if embeddings is None:
        embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL, base_url=OLLAMA_URL)
    return Chroma(
        collection_name=COLECCION,
        embedding_function=embeddings,
        persist_directory=str(base_dir),
    )


def recuperar(base: Chroma, pregunta: str, tema: str) -> list[Document]:
    """Devuelve los trozos del tema activo y, después, los mejores globales.

    Se piden K_TEMA resultados filtrados por tema y K_GLOBAL sin filtro; se
    eliminan duplicados conservando el orden (primero los del tema).
    """
    del_tema = base.similarity_search(pregunta, k=K_TEMA, filter={"tema": tema})
    globales = base.similarity_search(pregunta, k=K_GLOBAL)
    vistos: set[tuple[str, str]] = set()
    resultado: list[Document] = []
    for doc in del_tema + globales:
        clave = (doc.metadata.get("ruta", ""), doc.page_content[:80])
        if clave not in vistos:
            vistos.add(clave)
            resultado.append(doc)
    return resultado
