"""Smoke tests de la app con AppTest (motor y Ollama simulados)."""

import pytest
from streamlit.testing.v1 import AppTest

from pathlib import Path

from rag.config import TEMAS

RAIZ = Path(__file__).resolve().parent.parent


@pytest.fixture
def app_simulada(monkeypatch):
    import interfaz.profe as profe
    import rag.generacion as generacion
    import rag.motor as motor

    monkeypatch.setattr(profe, "ollama_disponible", lambda: True)
    monkeypatch.setattr(profe, "modelos_instalados", lambda: [])
    monkeypatch.setattr(motor, "abrir_base", lambda *a, **k: None)
    monkeypatch.setattr(generacion, "responder_stream", lambda *a, **k: ([], iter(["hola"])))
    return monkeypatch


def _app() -> AppTest:
    return AppTest.from_file(str(RAIZ / "app.py"), default_timeout=30)


def test_portada_muestra_6_temas(app_simulada):
    at = _app().run()
    assert not at.exception
    botones = [b for b in at.button if b.key and b.key.startswith("btn-")]
    assert len(botones) == len(TEMAS) == 6


def test_sin_base_muestra_instruccion(app_simulada):
    import rag.motor as motor

    def sin_base(*a, **k):
        raise FileNotFoundError("Falta la base: ejecuta la ingesta")

    app_simulada.setattr(motor, "abrir_base", sin_base)
    at = _app().run()
    assert "ingesta" in at.error[0].value


def test_sin_ollama_muestra_error(app_simulada):
    import interfaz.profe as profe

    app_simulada.setattr(profe, "ollama_disponible", lambda: False)
    at = _app().run()
    assert "ollama serve" in at.error[0].value


def test_pregunta_sugerida_responde_y_volver(app_simulada):
    at = _app().run()
    at.button(key="btn-antartida").click().run()
    assert at.session_state["tema"] == "antartida"
    sugeridas = [b for b in at.button if b.key and b.key.startswith("sug-")]
    assert len(sugeridas) == 4
    sugeridas[0].click().run()
    assert not at.exception
    mensajes = [m.markdown[0].value for m in at.chat_message if m.markdown]
    assert "hola" in mensajes
    assert len(at.session_state["historial"]["antartida"]) == 2
    at.button(key="volver").click().run()
    assert at.session_state["tema"] is None


def test_pregunta_vacia_ignorada(app_simulada):
    at = _app().run()
    at.button(key="btn-antartida").click().run()
    at.chat_input[0].set_value("   ").run()
    assert not at.session_state["historial"].get("antartida")


def test_error_de_conexion_en_espanol(app_simulada):
    import rag.generacion as generacion

    def roto():
        raise ConnectionError("boom")
        yield ""

    app_simulada.setattr(generacion, "responder_stream", lambda *a, **k: ([], roto()))
    at = _app().run()
    at.button(key="btn-antartida").click().run()
    at.chat_input[0].set_value("hola").run()
    assert any("Se ha perdido la conexión con Ollama" in e.value for e in at.error)
    assert not at.session_state["historial"].get("antartida")


def test_error_no_de_conexion_es_generico(app_simulada):
    import rag.generacion as generacion

    def roto():
        raise ValueError("fallo raro")
        yield ""

    app_simulada.setattr(generacion, "responder_stream", lambda *a, **k: ([], roto()))
    at = _app().run()
    at.button(key="btn-antartida").click().run()
    at.chat_input[0].set_value("hola").run()
    textos = [e.value for e in at.error]
    assert any("Algo ha fallado" in t and "ValueError" in t for t in textos)
    assert not any("conexión con Ollama" in t for t in textos)
    assert not at.session_state["historial"].get("antartida")
