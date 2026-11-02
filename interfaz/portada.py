"""Portada: rejilla de misiones científicas (una tarjeta-botón por tema)."""

import streamlit as st

from rag.config import TEMAS, foto_tarjeta


def render() -> None:
    """Muestra las tarjetas de tema; al pulsar una, fija el tema y recarga."""
    st.markdown(
        '<div class="titulo-portada">Elige una misión científica</div>',
        unsafe_allow_html=True,
    )
    temas = list(TEMAS.values())
    for inicio in range(0, len(temas), 3):
        columnas = st.columns(3)
        for columna, tema in zip(columnas, temas[inicio : inicio + 3]):
            with columna:
                with st.container(key=f"tarjeta-{tema.slug}"):
                    foto = foto_tarjeta(tema.slug)
                    if foto:
                        st.image(str(foto), use_container_width=True)
                    etiqueta = f"{tema.emoji}\n{tema.titulo}\n{tema.subtitulo}"
                    if st.button(etiqueta, key=f"btn-{tema.slug}", use_container_width=True):
                        st.session_state["tema"] = tema.slug
                        st.rerun()
