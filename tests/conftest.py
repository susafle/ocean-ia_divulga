"""Utilidades compartidas de los tests: embeddings deterministas sin red."""

import hashlib
import math
import re

import pytest
from langchain_core.embeddings import Embeddings

DIM = 32


class EmbeddingsFalsos(Embeddings):
    """Embeddings deterministas: bolsa de palabras hasheada a 32 dimensiones.

    Los textos que comparten palabras producen vectores cercanos.
    """

    def _vector(self, texto: str) -> list[float]:
        v = [0.0] * DIM
        for token in re.findall(r"\w+", texto.lower()):
            h = int(hashlib.md5(token.encode("utf-8")).hexdigest(), 16)
            v[h % DIM] += 1.0
        norma = math.sqrt(sum(x * x for x in v))
        if norma == 0:
            v[0] = 1.0
            return v
        return [x / norma for x in v]

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self._vector(t) for t in texts]

    def embed_query(self, text: str) -> list[float]:
        return self._vector(text)


@pytest.fixture
def embeddings_falsos() -> EmbeddingsFalsos:
    return EmbeddingsFalsos()
