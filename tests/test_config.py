def test_temas_completos():
    from rag.config import TEMAS, Tema
    assert set(TEMAS) == {"ia-oceano", "oceano-acido", "antartida",
                          "gases-del-mar", "donana-praderas", "ser-oceanografa"}
    for slug, t in TEMAS.items():
        assert isinstance(t, Tema) and t.slug == slug
        assert t.emoji and t.titulo and t.subtitulo and t.color.startswith("#")
