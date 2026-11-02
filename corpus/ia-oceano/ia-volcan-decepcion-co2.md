---
titulo: La IA que usa un volcán para medir CO₂
tema: ia-oceano
fuente: Flecha S. et al. 2025, "Integrated meteocean and seismic dataset for AI-based seawater CO2 estimation at Deception Island, Antarctica", Scientific Data 13:38 (abstract, acceso abierto) https://doi.org/10.1038/s41597-025-06351-4
---
# La IA que usa un volcán para medir CO₂

¿Se puede estimar el CO₂ del agua del mar usando también los temblores de un volcán? Parece una locura, pero es justo lo que probó el equipo en la Antártida.

## El sitio: Isla Decepción

Isla Decepción es una isla volcánica antártica (te la presento mejor en el tema «Misión Antártida»). En febrero de 2025 se recogió allí un conjunto de datos muy completo, publicado en la revista *Scientific Data*.

## Qué se midió

El conjunto de datos integra:

- la **pCO₂ superficial** del agua (una medida de cuánto CO₂ hay disuelto),
- temperatura y salinidad del agua,
- viento,
- temperatura del aire,
- radiación solar,
- marea,
- **señales sísmicas** (las vibraciones del suelo del volcán).

## La inteligencia artificial

Con esos datos entrenaron una red neuronal **Bi-LSTM** (memoria a largo-corto plazo bidireccional). Es un tipo de red que procesa secuencias de datos en el tiempo, como leer una frase entera para entender una palabra. La red procesó secuencias con varias variables a la vez («multivariantes») para **estimar la pCO₂**.

Para comprobar que funcionaba, la validaron con **cinco particiones de validación cruzada**: repitieron la prueba cinco veces, apartando cada vez una parte distinta de los datos para ver si el modelo acertaba con datos que no había visto. Los datos finales incluyen valores medidos y valores estimados.

## ¿Por qué meter señales sísmicas?

Es un volcán activo, y los autores integraron en un único conjunto variables meteorológicas, oceánicas y geofísicas. El resumen público no dice cuánto pesa cada variable en el modelo, así que no podemos afirmar cuál ayudó más.

## Datos para todo el mundo

Los datos y su procesamiento siguen los principios **FAIR**: fáciles de encontrar, accesibles, interoperables y reutilizables. Cualquier equipo científico puede usarlos para probar sus propios modelos.

## Idea clave

Mantener un sensor de CO₂ en la Antártida no es fácil. Si la IA aprende de variables más sencillas de registrar (viento, marea, temperatura...), puede ayudar a estimar el CO₂ del agua. Es un ejemplo de cómo se combinan el mar y la IA, que tienes explicado en otra ficha de este tema.
