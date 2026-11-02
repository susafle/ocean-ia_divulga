---
titulo: Cuando el sensor se apaga, la IA adivina el pH
tema: ia-oceano
fuente: "Flecha S. et al. 2022, «pH trends and seasonal cycle in the coastal Balearic Sea reconstructed through machine learning», Scientific Reports 12:12956 (artículo completo, acceso abierto CC BY) https://doi.org/10.1038/s41598-022-17253-5"
---
# Cuando el sensor se apaga, la IA adivina el pH

Imagina que tienes un termómetro en tu balcón que apunta la temperatura cada hora, pero a veces se queda sin pilas. Tendrás huecos en tus datos. En el mar pasa lo mismo, solo que los sensores trabajan bajo el agua. Sus datos tienen huecos inevitables.

## El estudio

En 2022, el equipo de OCEAN-IA publicó en *Scientific Reports* un trabajo sobre la costa de las islas Baleares (Mar Mediterráneo occidental). Usaron **sensores autónomos** en **dos sitios costeros**: la Bahía de Palma (pH medido cada hora desde diciembre de 2018) y el Parque Nacional de Cabrera (desde noviembre de 2019). Los datos llegan hasta diciembre de 2021. Los sensores medían pH, temperatura, salinidad y oxígeno disuelto.

En Cabrera hubo un hueco grande, de diciembre de 2019 a junio de 2020. El sensor se estropeó y la reparación se alargó por el confinamiento de la COVID-19.

## ¿Qué hicieron con la IA?

Entrenaron **redes neuronales recurrentes (RNN)**, un tipo de modelo de aprendizaje automático. La que mejor funcionó fue una **BD-LSTM** (memoria a corto y largo plazo bidireccional), que mira la serie de datos hacia delante y hacia atrás en el tiempo. En los dos sitios el error fue **menor del 1 %**, tanto en los datos de entrenamiento como en los de validación, y sin señales de sobreajuste.

- En **Cabrera** rellenaron el hueco de 2019-2020.
- En la **Bahía de Palma** reconstruyeron el pH desde 2012. Allí las otras variables se medían desde octubre de 2012, mucho antes que el pH. Así lograron unos nueve años de pH para calcular una tendencia.

## Los números

- La tendencia del pH en la Bahía de Palma es de **−0,0020 ± 0,00054 unidades de pH por año**. Los autores la presentan como la primera estimación de tendencia de pH en el mar costero balear.
- Con un ajuste lineal sencillo salía −0,0025 ± 0,00053 por año, pero lo descartaron porque introducía un sesgo.
- El pH cambia con las estaciones: sube hasta **8,18 en invierno** y baja hasta **7,91 en verano**.
- La temperatura del agua subió **0,035 ± 0,008 °C por año** (2012-2021). La salinidad bajó **0,059 ± 0,002 unidades por año**.
- La bajada de pH que se esperaría solo por el CO₂ de la atmósfera (2013-2021) es de 0,0025 ± 0,0002 por año. Por eso los autores concluyen que el CO₂ atmosférico es el principal responsable de la bajada del pH en esta costa.

Para comparar: en el artículo se citan estimaciones del Mediterráneo abierto de −0,003 a −0,0044 por año, y de −0,0013 a −0,0026 en el océano abierto. La tendencia balear queda en el rango de esas observaciones.

## ¿Por qué es útil?

El método permite obtener tendencias de pH cuando solo hay pocas medidas de pH, pero sí otras variables. Así se pueden rellenar los huecos de las series de sensores. Los autores piden más investigación para confirmar estas tendencias regionales.

## Ojo con las cifras

La serie de pH medida es corta y la tendencia sale de datos en parte reconstruidos. En el artículo el ajuste tiene R² = 0,1, es decir, explica poco de la variación diaria. Por eso hablamos de una estimación y no de una verdad cerrada.

## Para pensar

La IA no inventa datos de la nada: aprende de relaciones entre variables medidas de verdad. Por eso es importante que alguien siga midiendo en el mar. Cuantos más datos buenos, mejor puede aprender el modelo.
