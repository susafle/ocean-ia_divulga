"""Vista de chat: conversación por tema con preguntas sugeridas y fuentes."""

import urllib.error

import streamlit as st

from rag import generacion
from rag.config import Tema, foto_tarjeta, fotos_galeria

# Solo fallos de red; ollama.ResponseError (modelo inexistente, etc.) va al error genérico.
ERRORES_CONEXION: tuple[type[BaseException], ...] = (ConnectionError, urllib.error.URLError)
try:
    import httpx

    ERRORES_CONEXION += (httpx.TransportError,)
except ImportError:  # pragma: no cover
    pass

MENSAJE_SIN_CONEXION = (
    "Se ha perdido la conexión con Ollama. Comprueba que sigue abierto "
    "(`ollama serve`) y vuelve a preguntar."
)


def _mostrar_fuentes(fuentes: list[str]) -> None:
    if not fuentes:
        return
    with st.expander("📄 ¿De dónde sale esta respuesta?"):
        for fuente in fuentes:
            st.markdown(f"- {fuente}")


def _banner(tema: Tema) -> None:
    st.markdown(
        f'<div style="background:{tema.color};border-radius:1rem;padding:1rem 1.5rem;'
        f'margin-bottom:1rem;border:2px solid #14609E;">'
        f'<span style="font-size:2.4rem">{tema.emoji}</span> '
        f'<span style="font-size:1.8rem;font-weight:700;color:#0B2C5F">{tema.titulo}</span>'
        f'<div style="font-size:1.1rem;color:#0B2540">{tema.subtitulo}</div></div>',
        unsafe_allow_html=True,
    )


def _galeria(tema: Tema) -> None:
    rutas = fotos_galeria(tema.slug)
    if not rutas:
        return
    with st.expander("📸 Fotos de campaña"):
        columnas = st.columns(2)
        for i, ruta in enumerate(rutas):
            with columnas[i % 2]:
                if ruta.suffix.lower() == ".mp4":
                    st.video(str(ruta))
                else:
                    st.image(str(ruta), use_container_width=True)


def render(base, tema: Tema, modelo: str | None = None, temperatura: float | None = None) -> None:
    """Dibuja el chat del tema dado y atiende una pregunta nueva si la hay."""
    historiales = st.session_state.setdefault("historial", {})
    historial = historiales.setdefault(tema.slug, [])

    if st.button("← Volver a los temas", key="volver"):
        st.session_state["tema"] = None
        st.rerun()

    foto = foto_tarjeta(tema.slug)
    if foto:
        col_banner, col_foto = st.columns([3, 1], vertical_alignment="center")
        with col_banner:
            _banner(tema)
        with col_foto:
            st.image(str(foto), use_container_width=True)
    else:
        _banner(tema)

    pregunta = None
    if not historial:
        st.markdown("**Prueba con una de estas preguntas:**")
        for i, sugerida in enumerate(tema.preguntas):
            if st.button(sugerida, key=f"sug-{tema.slug}-{i}", use_container_width=True):
                pregunta = sugerida

    _galeria(tema)

    for mensaje in historial:
        with st.chat_message(mensaje["rol"], avatar=tema.emoji if mensaje["rol"] == "assistant" else None):
            st.markdown(mensaje["texto"])
            if mensaje["rol"] == "assistant":
                _mostrar_fuentes(mensaje.get("fuentes", []))

    escrita = st.chat_input("Escribe tu pregunta…")
    pregunta = generacion.limpiar_pregunta(escrita) or pregunta
    if not pregunta:
        return

    pares = [
        (historial[i]["texto"], historial[i + 1]["texto"])
        for i in range(0, len(historial) - 1, 2)
    ]
    with st.chat_message("user"):
        st.markdown(pregunta)
    with st.chat_message("assistant", avatar=tema.emoji):
        try:
            kwargs = {}
            if modelo:
                kwargs["modelo"] = modelo
            if temperatura is not None:
                kwargs["temperatura"] = temperatura
            docs, stream = generacion.responder_stream(base, pregunta, tema.slug, pares, **kwargs)
            texto = st.write_stream(stream)
        except ERRORES_CONEXION:
            st.error(MENSAJE_SIN_CONEXION)
            return
        except Exception as e:
            st.error(f"Algo ha fallado generando la respuesta: {type(e).__name__}: {e}")
            return
        fuentes = generacion.fuentes_numeradas(docs)
        _mostrar_fuentes(fuentes)
    historial.append({"rol": "user", "texto": pregunta})
    historial.append({"rol": "assistant", "texto": texto, "fuentes": fuentes})
