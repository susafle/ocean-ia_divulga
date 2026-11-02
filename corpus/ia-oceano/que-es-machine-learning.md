---
titulo: ¿Qué es eso del machine learning?
tema: ia-oceano
fuente: "ISO, Aprendizaje automático (AA) https://committee.iso.org/es/inteligencia-artificial/aprendizaje-autom%C3%A1tico · Flecha S. et al. 2022, «pH trends and seasonal cycle in the coastal Balearic Sea reconstructed through machine learning», Scientific Reports 12:12956 https://doi.org/10.1038/s41598-022-17253-5"
---
# ¿Qué es eso del machine learning?

Seguro que has oído hablar de la inteligencia artificial. Dentro de ella hay una idea muy usada en ciencia: el **machine learning**, o **aprendizaje automático** en español.

## La idea en una frase

Según la ISO (la organización internacional que fija normas técnicas), el aprendizaje automático es un tipo de inteligencia artificial que permite a las máquinas aprender de los datos sin necesidad de programarlas explícitamente. Es decir: en lugar de escribir a mano todas las reglas, le das al ordenador muchísimos ejemplos y él busca los patrones por su cuenta.

## Una comparación cotidiana

Piensa en cómo aprendiste a distinguir un perro de un gato. Nadie te dio una lista de reglas. Viste muchos perros y muchos gatos, y tu cerebro sacó el patrón. Un modelo de aprendizaje automático hace algo parecido, pero con números: datos de temperatura, de salinidad, de oxígeno, de pH...

## Y si es «profundo», ¿qué es el deep learning?

El **deep learning** (aprendizaje profundo) es una familia de modelos llamados redes neuronales, que trabajan por capas. Dos tipos aparecen en los estudios de este material:

- Las **redes neuronales recurrentes (RNN)**, usadas en Flecha et al. (2022) para predecir el pH del agua costera de Baleares.
- Las **Bi-LSTM** (memoria a largo-corto plazo bidireccional), usadas también en la Antártida para estimar el CO₂ del agua.

## Cómo se entrenó el modelo del pH

Según el apartado de métodos de Flecha et al. (2022):

- Primero, los datos se promediaron para tener **un valor por día**.
- Después se **normalizaron** (se pusieron todas las variables en una misma escala).
- Probaron cuatro tipos de red: SRNN, LSTM, BD-LSTM y BD-GRU. La mejor fue la **BD-LSTM**, que mira la serie de datos hacia delante y hacia atrás en el tiempo.
- La red tenía una capa oculta con 3 celdas y una ventana de 6 datos. Para dar más seguridad al resultado repitieron el entrenamiento 1000 veces.
- El error fue menor del 1 % y no hubo signos de sobreajuste (que el modelo se aprenda los datos de memoria).

## ¿Y qué pinta el océano en todo esto?

El equipo de OCEAN-IA aplica estas técnicas al mar. Los sensores del mar producen muchísimos datos, y a veces fallan o se apagan. El modelo aprende de la temperatura, la salinidad y el oxígeno para estimar el pH cuando falta. Los datos abiertos y reproducibles, siguiendo los principios **FAIR**, permiten que otros equipos comprueben y reutilicen lo que se hizo.

## ¿Es magia?

No. Un modelo de aprendizaje automático aprende de los datos que le damos, que salen de mediciones reales hechas por personas. Por eso las máquinas ayudan, pero las mediciones en el mar siguen siendo imprescindibles.
