"""Ingesta del corpus de DivulgaRAG: valida los .md y los indexa en Chroma."""

import shutil
from pathlib import Path

import yaml
from chromadb.api.shared_system_client import SharedSystemClient
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from rag.config import (
    BASE_DIR,
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    COLECCION,
    CORPUS_DIR,
    EMBEDDING_MODEL,
    OLLAMA_URL,
    TEMAS,
)

CLAVES_OBLIGATORIAS = ("titulo", "tema", "fuente")


def _separar_frontmatter(texto: str, ruta: Path) -> tuple[dict, str]:
    """Devuelve (frontmatter, cuerpo) o lanza ValueError nombrando el fichero."""
    partes = texto.lstrip("﻿").split("---", 2)
    if len(partes) < 3 or partes[0].strip():
        raise ValueError(f"{ruta}: falta el frontmatter YAML delimitado por '---'")
    try:
        meta = yaml.safe_load(partes[1])
    except yaml.YAMLError as e:
        raise ValueError(f"{ruta}: el frontmatter YAML no es válido ({e})") from e
    if not isinstance(meta, dict):
        raise ValueError(f"{ruta}: el frontmatter YAML debe ser un mapa de claves")
    return meta, partes[2].strip()


def cargar_corpus(corpus_dir: Path) -> list[Document]:
    """Lee todos los .md del corpus y devuelve un Document por fichero."""
    corpus_dir = Path(corpus_dir)
    docs = []
    for ruta in sorted(corpus_dir.rglob("*.md")):
        meta, cuerpo = _separar_frontmatter(ruta.read_text(encoding="utf-8"), ruta)
        faltan = [c for c in CLAVES_OBLIGATORIAS if not meta.get(c)]
        if faltan:
            raise ValueError(f"{ruta}: faltan claves obligatorias en el frontmatter: {', '.join(faltan)}")
        if meta["tema"] not in TEMAS:
            raise ValueError(
                f"{ruta}: tema desconocido '{meta['tema']}' (válidos: {', '.join(TEMAS)})"
            )
        docs.append(
            Document(
                page_content=cuerpo,
                metadata={
                    "tema": meta["tema"],
                    "titulo": str(meta["titulo"]),
                    "fuente": str(meta["fuente"]),
                    "ruta": str(ruta.relative_to(corpus_dir)),
                },
            )
        )
    return docs


def trocear(docs: list[Document]) -> list[Document]:
    """Divide los documentos en trozos conservando la metadata."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    return splitter.split_documents(docs)


def construir_base(corpus_dir: Path, base_dir: Path, embeddings: Embeddings) -> Chroma:
    """Reconstruye desde cero la base Chroma a partir del corpus."""
    base_dir = Path(base_dir)
    # Primero se valida y trocea: si el corpus es inválido, la base previa queda intacta
    docs = cargar_corpus(corpus_dir)
    trozos = trocear(docs)
    if base_dir.exists():
        # Depende de API interna de chromadb 1.5.9: sin vaciar la caché de clientes,
        # Chroma conserva un manejador sobre la base borrada y falla con
        # "attempt to write a readonly database" al reconstruirla en el mismo proceso.
        SharedSystemClient.clear_system_cache()
        shutil.rmtree(base_dir)
    base = Chroma(
        collection_name=COLECCION,
        embedding_function=embeddings,
        persist_directory=str(base_dir),
    )
    if trozos:
        base.add_documents(trozos)
    return base


if __name__ == "__main__":
    from langchain_ollama import OllamaEmbeddings

    emb = OllamaEmbeddings(model=EMBEDDING_MODEL, base_url=OLLAMA_URL)
    docs = cargar_corpus(CORPUS_DIR)
    trozos = trocear(docs)
    construir_base(CORPUS_DIR, BASE_DIR, emb)
    print(f"Documentos: {len(docs)} | Trozos: {len(trozos)}")
