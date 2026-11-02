"""Tests del motor de recuperación (Chroma real en tmp_path, embeddings falsos)."""

import pytest

from ingesta import construir_base
from rag.config import K_GLOBAL, K_TEMA
from rag.motor import abrir_base, recuperar


def _doc(tema: str, titulo: str, cuerpo: str) -> str:
    return f"---\ntitulo: {titulo}\ntema: {tema}\nfuente: https://ejemplo.org/x\n---\n{cuerpo}\n"


def _corpus(raiz):
    """Corpus sintético: 5 docs de antártida, 2 de gases y 2 de acidez."""
    textos = {
        "antartida": [f"pinguinos volcan hielo antartida isla numero{i}" for i in range(5)],
        "gases-del-mar": [
            "metano gas mar baleares emision metano",
            "metano gas oxido nitroso mar metano",
        ],
        "oceano-acido": [
            "ph conchas acido carbonato calcio",
            "ph acidificacion co2 absorbe oceano",
        ],
    }
    for tema, cuerpos in textos.items():
        carpeta = raiz / tema
        carpeta.mkdir(parents=True)
        for i, cuerpo in enumerate(cuerpos):
            (carpeta / f"d{i}.md").write_text(_doc(tema, f"{tema} {i}", cuerpo), encoding="utf-8")
    return raiz


@pytest.fixture
def base(tmp_path, embeddings_falsos):
    corpus = _corpus(tmp_path / "corpus")
    construir_base(corpus, tmp_path / "base", embeddings_falsos)
    return abrir_base(tmp_path / "base", embeddings_falsos)


def test_recuperar_prioriza_tema_con_fallback_global(base):
    # La pregunta se parece más a los docs de gases, pero el tema activo es antártida
    docs = recuperar(base, "metano gas mar", "antartida")
    temas = [d.metadata["tema"] for d in docs]
    assert len(docs) <= K_TEMA + K_GLOBAL
    assert temas[:K_TEMA] == ["antartida"] * K_TEMA
    assert any(t != "antartida" for t in temas)


def test_recuperar_sin_duplicados(base):
    docs = recuperar(base, "pinguinos volcan hielo", "antartida")
    claves = [(d.metadata["ruta"], d.page_content[:80]) for d in docs]
    assert len(claves) == len(set(claves))


def test_abrir_base_inexistente(tmp_path):
    with pytest.raises(FileNotFoundError, match="ingesta"):
        abrir_base(tmp_path / "no_existe")
