"""Tests de la ingesta del corpus (Chroma real en tmp_path, embeddings falsos)."""

from pathlib import Path

import pytest
from langchain_chroma import Chroma

from ingesta import cargar_corpus, construir_base, trocear
from rag.config import COLECCION


def _escribir(corpus: Path, tema_dir: str, nombre: str, texto: str) -> Path:
    carpeta = corpus / tema_dir
    carpeta.mkdir(parents=True, exist_ok=True)
    ruta = carpeta / nombre
    ruta.write_text(texto, encoding="utf-8")
    return ruta


def _doc(tema: str, cuerpo: str, titulo: str = "Un titulo") -> str:
    return (
        f"---\ntitulo: {titulo}\ntema: {tema}\nfuente: https://ejemplo.org/x\n---\n"
        f"{cuerpo}\n"
    )


def test_cargar_corpus_lee_frontmatter(tmp_path):
    _escribir(tmp_path, "ia-oceano", "doc.md", _doc("ia-oceano", "Texto sobre redes neuronales."))
    docs = cargar_corpus(tmp_path)
    assert len(docs) == 1
    d = docs[0]
    assert d.metadata["tema"] == "ia-oceano"
    assert d.metadata["titulo"] == "Un titulo"
    assert d.metadata["fuente"] == "https://ejemplo.org/x"
    assert d.metadata["ruta"] == str(Path("ia-oceano") / "doc.md")
    assert "---" not in d.page_content
    assert "titulo:" not in d.page_content
    assert "redes neuronales" in d.page_content


def test_frontmatter_invalido_nombra_fichero(tmp_path):
    _escribir(
        tmp_path, "ia-oceano", "roto.md",
        "---\ntitulo: Sin fuente\ntema: ia-oceano\n---\nTexto\n",
    )
    with pytest.raises(ValueError, match="roto.md"):
        cargar_corpus(tmp_path)


def test_tema_desconocido_nombra_fichero(tmp_path):
    _escribir(tmp_path, "marte", "marciano.md", _doc("marte", "Texto"))
    with pytest.raises(ValueError, match="marciano.md"):
        cargar_corpus(tmp_path)


def test_yaml_invalido_nombra_fichero(tmp_path):
    _escribir(tmp_path, "ia-oceano", "yaml_malo.md", "---\ntitulo: [sin cerrar\n---\nTexto\n")
    with pytest.raises(ValueError, match="yaml_malo.md"):
        cargar_corpus(tmp_path)


def test_sin_frontmatter_nombra_fichero(tmp_path):
    _escribir(tmp_path, "ia-oceano", "plano.md", "Solo texto, sin frontmatter\n")
    with pytest.raises(ValueError, match="plano.md"):
        cargar_corpus(tmp_path)


def test_trocear_conserva_metadata(tmp_path):
    _escribir(tmp_path, "ia-oceano", "largo.md", _doc("ia-oceano", "Palabra " * 600))
    trozos = trocear(cargar_corpus(tmp_path))
    assert len(trozos) > 1
    assert all(t.metadata["tema"] == "ia-oceano" for t in trozos)


def test_construir_base_recupera_por_tema(tmp_path, embeddings_falsos):
    corpus = tmp_path / "corpus"
    _escribir(corpus, "antartida", "a.md", _doc("antartida", "Pinguinos y volcanes en la Antartida."))
    _escribir(corpus, "ia-oceano", "b.md", _doc("ia-oceano", "Aprendizaje automatico para el oceano."))
    base = construir_base(corpus, tmp_path / "base", embeddings_falsos)
    res = base.similarity_search("aprendizaje automatico oceano", k=1, filter={"tema": "antartida"})
    assert len(res) == 1
    assert res[0].metadata["tema"] == "antartida"


def test_corpus_invalido_conserva_base_previa(tmp_path, embeddings_falsos):
    corpus = tmp_path / "corpus"
    _escribir(corpus, "antartida", "a.md", _doc("antartida", "Pinguinos."))
    destino = tmp_path / "base"
    construir_base(corpus, destino, embeddings_falsos)
    _escribir(corpus, "antartida", "roto.md", "sin frontmatter\n")
    with pytest.raises(ValueError, match="roto.md"):
        construir_base(corpus, destino, embeddings_falsos)
    assert destino.exists()
    (corpus / "antartida" / "roto.md").unlink()
    base = Chroma(
        collection_name=COLECCION,
        embedding_function=embeddings_falsos,
        persist_directory=str(destino),
    )
    assert len(base.get()["ids"]) == 1


def test_construir_base_reemplaza_base_previa(tmp_path, embeddings_falsos):
    corpus = tmp_path / "corpus"
    _escribir(corpus, "antartida", "a.md", _doc("antartida", "Pinguinos."))
    destino = tmp_path / "base"
    construir_base(corpus, destino, embeddings_falsos)
    base = construir_base(corpus, destino, embeddings_falsos)
    assert len(base.get()["ids"]) == 1
