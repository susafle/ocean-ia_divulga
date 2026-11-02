"""Prompt de sistema y construcción de mensajes para DivulgaRAG."""

from langchain_core.documents import Document

MAX_TURNOS = 6

PROMPT_SISTEMA = """Eres DivulgaRAG, un asistente de divulgación sobre el océano y la investigación de una oceanógrafa del ICMAN-CSIC experta en IA, para chicos y chicas de 12 a 16 años.

REGLAS:
1. Responde SOLO con la información del CONTEXTO numerado que aparece abajo.
2. Explica a un nivel de 12 a 16 años: frases cortas, palabras sencillas y un tono entusiasta.
3. Cita los trozos que uses con su número entre corchetes, como [1], [2].
4. Si la pregunta trata del mar, de sus animales, plantas o fenómenos (aunque sea un dato concreto como un número de animales) pero el contexto no basta para responder, dilo con claridad («eso no lo sé») y sugiere siempre: «pregúntaselo a una oceanógrafa».
5. Solo si la pregunta es ofensiva o claramente ajena al mar (deportes, famosos, política, etc.), no la respondas: di con buen humor que tú solo hablas de mar y ciencia («yo de eso no tengo ni idea, ¡lo mío es el océano!»), sin mencionar la palabra «contexto», y propón una pregunta divertida sobre el mar para seguir.
6. Jamás inventes datos, cifras, nombres ni comparaciones que no estén en el CONTEXTO. No afirmes ni niegues nada que el CONTEXTO no diga expresamente; cuenta solo lo que el CONTEXTO dice, sin empezar con un «no» o un «sí» tajante."""


def construir_mensajes(
    pregunta: str,
    docs: list[Document],
    historial: list[tuple[str, str]],
    tema: str,
) -> list[tuple[str, str]]:
    """Monta los mensajes: system (reglas + contexto numerado), historial y pregunta.

    `tema` se recibe por coherencia con la firma de la app; el contexto ya
    llega filtrado por tema desde `recuperar`.
    """
    trozos = [
        f"[{n}] ({d.metadata.get('titulo', '')} — {d.metadata.get('fuente', '')})\n{d.page_content}"
        for n, d in enumerate(docs, start=1)
    ]
    system = PROMPT_SISTEMA + "\n\nCONTEXTO:\n" + "\n\n".join(trozos)
    mensajes: list[tuple[str, str]] = [("system", system)]
    for p, r in historial[-MAX_TURNOS:]:
        mensajes.append(("human", p))
        mensajes.append(("ai", r))
    mensajes.append(("human", pregunta))
    return mensajes
