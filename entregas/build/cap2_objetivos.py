"""Capitulo 2 - Objetivos.

Atiende C5 (parrafo de entrada antes del primer subtitulo), C6 (2.1 y 2.2) y C8
(objetivo general que declara herramienta, resultado esperado y forma de medirlo).
"""


def escribir(d):
    d.h1("Objetivos")

    d.p(
        "Este capítulo es el puente entre el problema descrito y la innovación que se propone. El "
        "objetivo general expresa el efecto observable que se busca, la tecnología con la que se "
        "persigue y el modo en que se verificará su cumplimiento; los objetivos específicos "
        "descomponen ese propósito en pasos analizables por separado, en infinitivo y asociados a un "
        "resultado comprobable. Los umbrales numéricos que permiten declararlos cumplidos se "
        "detallan en el apartado 3.7."
    )

    d.h2("Objetivo general")

    d.p(
        "Reducir el tiempo y la variabilidad del triaje de reportes ciudadanos de emergencia en "
        "una coordinación municipal de protección civil, mediante el desarrollo y la evaluación "
        "de un producto mínimo viable que clasifique automáticamente cada reporte escrito en "
        "español de México por categoría temática y por nivel de urgencia —empleando un modelo "
        "de lenguaje preentrenado en español (BETO) ajustado mediante transferencia de "
        "aprendizaje— y que presente los reportes ordenados por prioridad en un panel de "
        "atención."
    )

    d.p(
        "El cumplimiento de este objetivo se medirá de forma comparativa. El modelo ajustado se "
        "contrastará con un modelo de referencia clásico sobre el mismo conjunto de prueba y las "
        "mismas particiones, empleando la medida F1 macro y por clase, con atención particular a "
        "la exhaustividad en las clases críticas de persona en riesgo y urgencia alta. Se "
        "verificará además que la calidad del etiquetado alcance un acuerdo sustancial entre "
        "anotadores y que la latencia de la clasificación resulte compatible con el uso "
        "operativo. Los umbrales concretos de cada indicador se establecen en el apartado 3.7."
    )

    d.h2("Objetivos específicos")

    d.numerada([
        "Analizar el estado del arte en clasificación de reportes de emergencia mediante "
        "procesamiento del lenguaje natural y definir, a partir de esa revisión y del trabajo de "
        "campo, las siete categorías temáticas y los tres niveles de urgencia del proyecto, con la "
        "guía de etiquetado que los operacionaliza.",

        "Construir un corpus propio de reportes en español de México, anonimizado y documentado, y "
        "validar su etiquetado mediante el coeficiente kappa de Cohen entre dos anotadores "
        "independientes.",

        "Implementar un modelo de referencia clásico basado en TF-IDF con regresión logística y "
        "máquinas de vectores de soporte, como línea base obligatoria de comparación.",

        "Ajustar mediante transferencia de aprendizaje el modelo BETO para las dos tareas de "
        "clasificación, atendiendo el desbalance entre clases y la calibración de la confianza.",

        "Evaluar comparativamente ambos enfoques sobre las mismas particiones, con precisión, "
        "exhaustividad y medida F1 por clase y macro, matriz de confusión y conteo explícito de "
        "falsos negativos en las clases críticas.",

        "Integrar y desplegar el sistema de extremo a extremo —formulario, clasificador y panel "
        "priorizado—, verificando su funcionamiento y midiendo la latencia de respuesta.",
    ])

