# DivulgaRAG

Una app de chat para talleres de divulgación sobre el océano, pensada para chicos y chicas de 12 a 16 años. Responde en español, con un tono cercano, **solo con lo que dice un corpus de textos revisados** (no se inventa nada) y **cita siempre sus fuentes**. Funciona **sin internet**: el modelo de lenguaje corre en tu propio ordenador con [Ollama](https://ollama.com).

El corpus incluido recoge la investigación de la Dra. **Susana Flecha** (ICMAN-CSIC) sobre el océano: gases de efecto invernadero en el mar, acidificación, praderas de Posidonia, la Antártida, inteligencia artificial aplicada al océano y cómo es el trabajo de una oceanógrafa. Está organizado en seis temas, cada uno con preguntas de ejemplo para arrancar la conversación. Cualquier divulgador/a puede sustituirlo por su propio material (ver «Editar el corpus»).

Tecnología: Streamlit + LangChain + Chroma (RAG), Ollama con `qwen3:4b-instruct` (texto) y `qwen3-embedding:0.6b` (embeddings).

## Requisitos

- **Python 3.12**
- **Ollama** instalado y en marcha ([ollama.com/download](https://ollama.com/download)), con los dos modelos descargados (la primera vez hace falta internet):

  ```bash
  ollama pull qwen3:4b-instruct
  ollama pull qwen3-embedding:0.6b
  ```

- Opcional: el modelo `qwen3:14b` (`ollama pull qwen3:14b`) aparece en el modo profe como opción de mayor calidad si el equipo lo aguanta.

## Puesta en marcha

Todo se instala en un entorno virtual dentro del proyecto; no toca el Python del sistema.

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python ingesta.py          # solo la primera vez (y cada vez que cambies el corpus)
.venv/bin/streamlit run app.py
```

Se abre en <http://localhost:8501>. La ingesta lee los `.md` de `corpus/`, los trocea y crea la base vectorial en `bases/divulgarag/` (necesita Ollama arrancado).

El código QR del modo profe es opcional: viene de los paquetes `qrcode` y `pillow` de `requirements.txt`; si no están instalados, la app funciona igual y solo se muestra la URL en texto.

## Conectar una tablet (o varios móviles)

Útil para que el alumnado use la app desde tablets mientras el portátil hace de servidor. No hace falta internet, solo que todos estén en la misma red.

1. Crea un **punto de acceso (hotspot)** con tu móvil, o usa cualquier Wi-Fi local.
2. Conecta el portátil y la tablet a esa misma red.
3. Arranca la app escuchando en todas las interfaces:

   ```bash
   .venv/bin/streamlit run app.py --server.address 0.0.0.0
   ```

4. En el portátil, abre la barra lateral (**Modo profe**) y despliega **«Conectar una tablet»**: muestra la URL (del tipo `http://192.168.x.x:8501`) y un código QR.
5. En la tablet, escribe esa URL en el navegador o escanea el QR.

Si no carga: comprueba que ambos dispositivos están en la misma red y que el cortafuegos del portátil permite conexiones entrantes al puerto 8501.

## Antes del taller

Haz siempre un ensayo general en las mismas condiciones del taller:

- [ ] **Apaga el Wi-Fi** del portátil (o trabaja solo con el hotspot, sin datos), con **Ollama ya arrancado**. La app debe cargar y responder.
- [ ] Prueba una pregunta de cada tema (los botones de la portada traen ejemplos).
- [ ] Prueba una pregunta gamberra («¿Los pingüinos se tiran pedos?»), una ajena al mar («¿Quién ganó la liga?») y una del mar que no esté en el corpus («¿Cuántos tiburones hay en el Mediterráneo?»): debe responder sobre el guano y el metano, redirigir con simpatía al océano, y decir «pregúntaselo a una oceanógrafa», respectivamente, sin inventar.
- [ ] Si usas tablet: conéctala con la URL o el QR y haz una pregunta desde ella.
- [ ] Comprueba el tiempo de respuesta: con `qwen3:4b-instruct` el primer texto debe aparecer en pocos segundos. Si va lento, cierra otras aplicaciones.

## Modo profe

La barra lateral permite: elegir el modelo, ajustar la temperatura (más baja = respuestas más fieles al corpus), reiniciar la conversación, **re-indexar el corpus** con un botón y ver la URL/QR para la tablet.

## Editar el corpus y re-indexar

El corpus son ficheros Markdown en `corpus/<tema>/`. Cada fichero empieza con una cabecera YAML con tres claves obligatorias:

```markdown
---
titulo: ¿Los pingüinos se tiran pedos? El metano del guano
tema: antartida
fuente: Autoría, año, revista o web y enlace
---
# Título

Texto divulgativo…
```

- `tema` debe ser uno de los definidos en `rag/config.py` (`TEMAS`). Para añadir o cambiar temas, edita ese diccionario (título, emoji, color y preguntas de ejemplo).
- `fuente` es lo que verá el alumnado como cita bajo cada respuesta: sé preciso y marca lo que no hayas podido verificar.
- Escribe pensando en el nivel de 12 a 16 años y no incluyas nada que no puedas respaldar con la fuente: la app solo sabe lo que está en el corpus.

Tras cualquier cambio, **re-indexa**: con el botón «Re-indexar corpus» del modo profe, o desde la terminal con

```bash
.venv/bin/python ingesta.py
```

La ingesta valida los ficheros y avisa, nombrando el fichero, si falta la cabecera o una clave. Si añades PDFs de artículos en `fuentes_pdf/`, sirven como material de consulta para redactar nuevos documentos del corpus (los PDFs no se versionan).

## Estructura del repositorio

```
app.py            Punto de entrada de Streamlit: comprueba Ollama y la base, y enruta portada/chat
ingesta.py        Valida el corpus, lo trocea y construye la base Chroma
requirements.txt  Dependencias fijadas (+ qrcode/pillow opcionales)
corpus/           Documentos .md por tema (antartida, donana-praderas, gases-del-mar, ia-oceano, oceano-acido, ser-oceanografa)
bases/            Base vectorial generada (no se versiona)
rag/
  config.py       Temas, preguntas de ejemplo, modelos, tamaño de trozos y K
  motor.py        Apertura de la base y recuperación por tema (con respaldo global)
  prompts.py      Prompt de sistema y construcción de mensajes
  generacion.py   Respuesta en streaming con Ollama y fuentes
interfaz/
  estilos.py      CSS de la app
  portada.py      Portada con las temáticas
  chat.py         Chat por tema con fuentes
  profe.py        Modo profe (barra lateral)
tests/            Tests con pytest (.venv/bin/python -m pytest tests/ -q)
.streamlit/       Configuración (sin telemetría de uso)
```

## Créditos

Contenido científico basado en la investigación de la Dra. Susana Flecha, Instituto de Ciencias Marinas de Andalucía (ICMAN-CSIC). Los textos del corpus resumen trabajos publicados; consulta las fuentes citadas en cada documento para los detalles y la información completa.

## Licencia

El código de este repositorio se publica bajo licencia [MIT](LICENSE). Los documentos divulgativos de `corpus/` se publican bajo [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.es): puedes reutilizarlos y adaptarlos acreditando a **Susana Flecha Saura (ICMAN-CSIC)** y a las fuentes citadas en cada documento.
