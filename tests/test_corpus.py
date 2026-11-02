"""El corpus real debe pasar siempre la validación de la ingesta."""
from pathlib import Path

from ingesta import cargar_corpus
from rag.config import TEMAS

RAIZ = Path(__file__).parent.parent


def test_corpus_real_valida_y_cubre_todos_los_temas():
    docs = cargar_corpus(RAIZ / "corpus")
    assert len(docs) >= 30
    por_tema = {}
    for d in docs:
        assert d.metadata["tema"] in TEMAS
        por_tema.setdefault(d.metadata["tema"], 0)
        por_tema[d.metadata["tema"]] += 1
    assert set(por_tema) == set(TEMAS)
    for tema, n in por_tema.items():
        assert 4 <= n <= 8, f"{tema}: {n} docs"
