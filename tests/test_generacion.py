"""Tests de prompts, limpieza de preguntas y fuentes (sin Ollama)."""

from langchain_core.documents import Document

from rag.generacion import fuentes_numeradas, limpiar_pregunta
from rag.prompts import PROMPT_SISTEMA, construir_mensajes


def _doc(titulo: str, fuente: str, texto: str = "texto") -> Document:
    return Document(page_content=texto, metadata={"titulo": titulo, "fuente": fuente})


def test_construir_mensajes_numera_contexto_y_reglas():
    docs = [_doc("Pinguinos", "Prensa A", "uno"), _doc("pH", "Paper B", "dos")]
    msgs = construir_mensajes("¿Qué es el pH?", docs, [], "oceano-acido")
    rol, system = msgs[0]
    assert rol == "system"
    assert "[1] (Pinguinos — Prensa A)\nuno" in system
    assert "[2] (pH — Paper B)\ndos" in system
    assert "oceanógrafa" in system and "inventes" in system
    assert PROMPT_SISTEMA in system
    assert msgs[-1] == ("human", "¿Qué es el pH?")


def test_historial_limitado_a_seis_turnos():
    hist = [(f"p{i}", f"r{i}") for i in range(10)]
    msgs = construir_mensajes("nueva", [], hist, "antartida")
    # system + 6 turnos * 2 mensajes + pregunta
    assert len(msgs) == 1 + 12 + 1
    assert msgs[1] == ("human", "p4") and msgs[2] == ("ai", "r4")


def test_limpiar_pregunta_vacia():
    assert limpiar_pregunta("   ") is None
    assert limpiar_pregunta(" ¿Qué es el pH? ") == "¿Qué es el pH?"


def test_fuentes_numeradas_alineadas_con_el_contexto():
    docs = [_doc("A", "x", "uno"), _doc("B", "y", "dos"), _doc("A", "x", "tres")]
    lineas = fuentes_numeradas(docs)
    assert lineas == ["[1] A — x", "[2] B — y", "[3] A — x"]
    system = construir_mensajes("p", docs, [], "antartida")[0][1]
    for n, linea in enumerate(lineas, start=1):
        cabecera = linea.split(" ", 1)[1]
        assert f"[{n}] ({cabecera})\n" in system
