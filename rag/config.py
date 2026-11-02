"""Configuración central de DivulgaRAG: temas, modelos y parámetros del RAG."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Tema:
    """Tarjeta temática de la app: identidad visual y preguntas de ejemplo."""

    slug: str
    emoji: str
    titulo: str
    subtitulo: str
    color: str
    preguntas: tuple[str, ...]


TEMAS: dict[str, Tema] = {
    "ia-oceano": Tema(
        slug="ia-oceano",
        emoji="🤖",
        titulo="IA que lee el mar",
        subtitulo="Máquinas que aprenden del océano",
        color="#D6EAF8",
        preguntas=(
            "¿Qué es el machine learning y cómo se usa con el mar?",
            "¿Cómo puede una IA adivinar el pH si el sensor se apaga?",
            "¿Qué hace un volcán en un estudio de inteligencia artificial?",
            "¿Cómo se juntan las medidas del mar y la IA?",
        ),
    ),
    "oceano-acido": Tema(
        slug="oceano-acido",
        emoji="🐚",
        titulo="El océano se vuelve ácido",
        subtitulo="El pH del mar está bajando",
        color="#FADBD8",
        preguntas=(
            "¿El mar se está volviendo ácido de verdad?",
            "¿Qué les pasa a las conchas con el pH más bajo?",
            "¿Cuánto CO₂ absorbe el océano?",
            "¿Por qué se mide el pH en el Estrecho de Gibraltar?",
        ),
    ),
    "antartida": Tema(
        slug="antartida",
        emoji="🐧",
        titulo="Misión Antártida",
        subtitulo="Volcanes, pingüinos y CO₂",
        color="#D5F5E3",
        preguntas=(
            "¿Los pingüinos se tiran pedos?",
            "¿Hay un volcán activo en la Antártida?",
            "¿Puede un volcán abonar el mar con hierro?",
            "¿Qué se ha medido en la Isla Decepción?",
        ),
    ),
    "gases-del-mar": Tema(
        slug="gases-del-mar",
        emoji="🌫️",
        titulo="Los gases del mar",
        subtitulo="CO₂, metano y óxido nitroso",
        color="#E8DAEF",
        preguntas=(
            "¿Qué es el gas de la risa y hay en el mar?",
            "¿Qué gas calienta más el planeta, el CO₂ o el metano?",
            "¿El mar de Baleares suelta metano?",
            "¿Dónde hay más metano, en Doñana o en Baleares?",
        ),
    ),
    "donana-praderas": Tema(
        slug="donana-praderas",
        emoji="🦩",
        titulo="Marismas de Doñana y praderas marinas",
        subtitulo="Humedales y carbono azul",
        color="#FCF3CF",
        preguntas=(
            "¿Qué es el carbono azul?",
            "¿Doñana absorbe o suelta CO₂?",
            "¿Las praderas de Posidonia capturan carbono?",
            "¿Por qué importa cómo se mide en una pradera?",
        ),
    ),
    "ser-oceanografa": Tema(
        slug="ser-oceanografa",
        emoji="🚢",
        titulo="Ser oceanógrafa",
        subtitulo="Campañas, sensores y vida a bordo",
        color="#D1F2EB",
        preguntas=(
            "¿Cómo es una campaña oceanográfica?",
            "¿Qué puede salir mal cuando sales a medir al mar?",
            "¿Qué significa ± en un resultado científico?",
            "¿Qué es el IPCC y por qué importan estos estudios?",
        ),
    ),
}

# Fotos de campaña (locales; si falta un fichero se omite sin error)
FOTOS_DIR = Path("fotos")
FOTOS: dict[str, dict] = {
    "ia-oceano": {
        "tarjeta": "autonomous-monitoring.jpg",
        "galeria": ("instrument-preparation.jpg",),
    },
    "oceano-acido": {
        "tarjeta": "gift-deployment.jpg",
        "galeria": ("gift-mooring-preparation.jpg",),
    },
    "antartida": {
        "tarjeta": "antarctic-volcanic-beach.jpg",
        "galeria": (
            "hesperides-deception.jpg",
            "antarctic-zodiac-water-sampling.jpeg",
            "deception-rosette.jpg",
            "cojohns-aerial.mp4",
        ),
    },
    "gases-del-mar": {
        "tarjeta": "estuarine-monitoring.jpg",
        "galeria": ("mediterranean-campaign.jpg",),
    },
    "donana-praderas": {
        "tarjeta": "cabrera-mooring.jpg",
        "galeria": ("field-research-2015.jpg",),
    },
    "ser-oceanografa": {
        "tarjeta": "ctd-deployment.jpg",
        "galeria": (
            "antarctic-rosette-deck-sampling.jpeg",
            "sensor-maintenance.jpg",
            "scar-2026-oslo-talk.jpeg",
            "antarctic-snowstorm-deck.jpg",
        ),
    },
}


def foto_tarjeta(slug: str) -> Path | None:
    """Ruta de la foto de tarjeta del tema, o None si no existe."""
    nombre = FOTOS.get(slug, {}).get("tarjeta")
    ruta = FOTOS_DIR / nombre if nombre else None
    return ruta if ruta is not None and ruta.is_file() else None


def fotos_galeria(slug: str) -> list[Path]:
    """Rutas existentes de la galería del tema (omite las que faltan)."""
    rutas = (FOTOS_DIR / n for n in FOTOS.get(slug, {}).get("galeria", ()))
    return [r for r in rutas if r.is_file()]


# Modelos y servidor de Ollama (se ejecuta en local)
OLLAMA_URL = "http://localhost:11434"
LLM_MODEL = "qwen3:4b-instruct"
LLM_MODEL_GRANDE = "qwen3:14b"
EMBEDDING_MODEL = "qwen3-embedding:0.6b"

# Rutas de datos
CORPUS_DIR = Path("corpus")
BASE_DIR = Path("bases/divulgarag")
COLECCION = "divulgarag"

# Parámetros de troceado y recuperación
CHUNK_SIZE = 1200
CHUNK_OVERLAP = 150
K_TEMA = 4
K_GLOBAL = 2
TEMPERATURE = 0.3
