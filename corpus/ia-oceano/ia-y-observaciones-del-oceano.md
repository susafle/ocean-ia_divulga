---
titulo: Mar e inteligencia artificial, cómo se combinan
tema: ia-oceano
fuente: "Flecha S. et al. 2022, «pH trends and seasonal cycle in the coastal Balearic Sea reconstructed through machine learning», Scientific Reports 12:12956 https://doi.org/10.1038/s41598-022-17253-5 · Flecha S. et al. 2025, «Integrated meteocean and seismic dataset for AI-based seawater CO2 estimation at Deception Island, Antarctica», Scientific Data 13:38 https://doi.org/10.1038/s41597-025-06351-4 · Flecha S. et al. 2025, Ocean Science 21:1515 https://os.copernicus.org/articles/21/1515/2025/"
---
# Mar e inteligencia artificial: cómo se combinan

Esta línea de trabajo se llama **OCEAN-IA**: inteligencia artificial y aprendizaje automático aplicados al océano. Los estudios de este tema tienen una idea común: juntar muchos años de medidas del océano con modelos de inteligencia artificial para entender mejor cómo cambia. No se usa la IA en lugar de medir. Se usa porque medir es difícil.

## ¿Qué datos se mezclan?

En los tres estudios aparecen variables de tres tipos:

- **Oceanográficas**: temperatura, salinidad, pH, oxígeno, clorofila.
- **Meteorológicas**: viento, temperatura del aire, radiación del sol.
- **Geofísicas**: por ejemplo, señales sísmicas, las vibraciones del suelo de un volcán.

## ¿Para qué sirve?

Medir el mar es caro y difícil. Hay lugares remotos, sensores que se averían y épocas en las que no se pudo medir. En Flecha et al. (2022), los autores explican que el mantenimiento de estaciones fijas tiene costes, riesgos de mal tiempo, fallos del sensor y errores humanos, y por eso los huecos en las series son frecuentes. La IA aprende de las variables que sí se midieron y ayuda a estimar las que faltan.

## Tres ejemplos de los artículos

1. **Rellenar huecos de pH** en Baleares con una red BD-LSTM (error menor del 1 %).
2. **Estimar el CO₂ del agua en la Antártida** con datos meteorológicos, oceánicos y sísmicos (conjunto de datos de febrero de 2025).
3. **Ordenar qué variables controlan el N₂O** en la costa de Baleares: la temperatura pesó un 65 %.

Cada uno está contado con detalle en otra ficha de este tema.

## Datos abiertos

Los datos de Isla Decepción se publicaron en *Scientific Data* con acceso abierto y siguiendo los principios FAIR (fáciles de encontrar, accesibles, interoperables y reutilizables). Así otros equipos pueden probar sus propios modelos.

## Resumen para llevarte

- Se combinan observaciones del mar, del tiempo y del suelo con deep learning.
- Sirve para rellenar huecos y estimar variables difíciles de medir.
- La IA ayuda, pero necesita datos reales medidos en el mar.
