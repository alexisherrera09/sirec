"""3.7 Diseno de la evaluacion (apartado nuevo).

Atiende C14: protocolo comparativo linea base TF-IDF frente a BETO con el mismo
conjunto de datos y particiones reproducibles; metricas por clase y macro; matriz
de confusion; falsos negativos en clases criticas; acuerdo de etiquetado; tiempo
de respuesta; y criterios minimos de exito comprometidos con umbrales.
"""


def escribir(d):
    d.h2("Diseño de la evaluación")

    d.p(
        "Este último apartado define cómo se comprobará que la solución funciona, antes de haberla "
        "evaluado: anticipar el diseño fija los criterios con los que se juzgará el resultado sin "
        "conocerlo, lo que evita ajustar después las expectativas a lo conseguido. Se describen el "
        "protocolo comparativo, las particiones, las métricas, los criterios mínimos de éxito y las "
        "amenazas a la validez; la ejecución y sus resultados corresponden al capítulo de validación "
        "de la memoria final."
    )

    d.h3("Protocolo comparativo y particiones reproducibles")

    d.p(
        "La evaluación es comparativa por diseño. Se contrastan dos enfoques sobre exactamente los "
        "mismos datos: la línea base clásica, que combina la representación TF-IDF con regresión "
        "logística y con máquinas de vectores de soporte, y el modelo BETO ajustado mediante "
        "transferencia de aprendizaje. Ambos resuelven las dos tareas del proyecto y reciben el "
        "mismo texto de entrada, con idéntico preprocesamiento, para que la diferencia observada sea "
        "atribuible al modelo y no al tratamiento de los datos."
    )

    d.p(
        "El corpus se divide en tres particiones estratificadas por clase, con proporciones "
        "aproximadas de 70 % para entrenamiento, 15 % para validación y 15 % para prueba. La "
        "estratificación es necesaria porque las clases críticas son minoritarias y una división "
        "aleatoria simple podría dejarlas sin representación suficiente en la prueba. Las "
        "particiones se generan una sola vez con una semilla fija que se documenta en el "
        "repositorio, y se reutilizan sin modificación en todos los experimentos, de modo que "
        "cualquier persona pueda reproducir los mismos conjuntos."
    )

    d.p(
        "Tres reglas adicionales protegen la validez de la comparación: el conjunto de prueba se "
        "compone solo de reportes reales, se emplea una única vez al final —las decisiones de ajuste "
        "se toman sobre la partición de validación— y ningún reporte aparece en más de una partición, "
        "comprobación necesaria porque un mismo hecho puede reportarse en términos casi idénticos."
    )

    d.h3("Métricas seleccionadas")

    d.p(
        "El desempeño se reporta con precisión, exhaustividad y medida F1 por clase, agregadas "
        "mediante promedio macro, que otorga igual importancia a cada clase con independencia de su "
        "frecuencia (Sokolova y Lapalme, 2009). Se descarta la exactitud global como métrica "
        "principal porque, con clases desbalanceadas, un modelo puede exhibirla elevada mientras "
        "falla sistemáticamente en las clases que más importan."
    )

    d.p(
        "A las métricas agregadas se añaden dos instrumentos de diagnóstico: la matriz de confusión "
        "de cada tarea, que permite identificar qué clases se confunden entre sí y no solo cuánto se "
        "falla, y el conteo absoluto de falsos negativos en las clases críticas —reportes de persona "
        "en riesgo clasificados como otra categoría y reportes de urgencia alta clasificados con "
        "urgencia menor—. Se reporta el número de casos y no solo la proporción, porque en conjuntos "
        "pequeños un porcentaje bajo puede ocultar sucesos graves."
    )

    d.p(
        "La evaluación incorpora además dos dimensiones ajenas al modelo: la calidad del etiquetado, "
        "medida con el coeficiente kappa de Cohen entre dos anotadores independientes que aplican la "
        "guía sobre una misma muestra (Cohen, 1960), y el tiempo de respuesta de extremo a extremo, "
        "desde el envío del formulario hasta la aparición del reporte en el panel, reportando la "
        "mediana y el percentil 95 en lugar del promedio."
    )

    d.h3("Criterios mínimos de éxito")

    d.p(
        "La tabla 8 fija los umbrales que permitirán declarar cumplido cada objetivo. Son "
        "compromisos asumidos antes de ejecutar la evaluación, de manera que el resultado sea "
        "verificable y no interpretable: cuando un indicador no alcance su umbral, el capítulo de "
        "validación deberá documentarlo como tal y discutir la causa, en lugar de reformular el "
        "criterio."
    )

    d.tabla(
        "Criterios mínimos de éxito de la evaluación",
        ["Indicador", "Umbral comprometido", "Justificación del umbral"],
        [
            ["F1 macro en la clasificación temática (7 clases)",
             "≥ 0.75 y al menos 5 puntos porcentuales sobre la mejor línea base",
             "La mejora debe ser apreciable para justificar el enfoque neuronal"],
            ["F1 macro en la clasificación de urgencia (3 clases)",
             "≥ 0.70, superando a la mejor línea base",
             "Tarea más subjetiva; umbral menor, pero se exige la mejora"],
            ["Exhaustividad en la categoría «persona en riesgo»", "≥ 0.90",
             "Es la clase donde omitir un caso tiene la consecuencia más grave"],
            ["Exhaustividad en el nivel «urgencia alta»", "≥ 0.90",
             "Determina el orden de atención de los casos con riesgo para la vida"],
            ["Falsos negativos graves (urgencia alta clasificada como baja)",
             "0 casos en la prueba",
             "Un salto de dos niveles sepulta un caso crítico al final de la lista"],
            ["Acuerdo entre anotadores (kappa de Cohen), ambas tareas", "≥ 0.60",
             "Umbral convencional de acuerdo sustancial (Landis y Koch, 1977)"],
            ["Latencia de extremo a extremo, percentil 95",
             "≤ 3 s, clasificación por debajo de 1.5 s",
             "El reporte debe priorizarse sin espera perceptible"],
            ["Reportes reales asignados a la categoría «otro»", "≤ 15 % de la prueba",
             "Un valor mayor indicaría que las siete categorías no cubren el flujo real"],
        ],
        pt_cuerpo=9.0,
        anchos=[5.0, 4.6, 6.4],
    )

    d.p(
        "Conviene declarar por anticipado las amenazas a la validez de este diseño. La principal es "
        "el tamaño del corpus, que al construirse manualmente será muy inferior a los conjuntos "
        "consolidados del área (Alam et al., 2021), lo que obliga a acompañar cada comparación del "
        "tamaño de la clase en la prueba; la segunda, que los datos provienen de fuentes públicas y "
        "no del canal institucional; y la tercera, el uso de ejemplos sintéticos en el entrenamiento, "
        "frente al que mantener la prueba enteramente real es la salvaguarda adoptada. Si el kappa "
        "resultara inferior al umbral, la conclusión correcta no sería descartar el enfoque, sino "
        "revisar la guía y reetiquetar."
    )
