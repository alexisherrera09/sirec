"""3.3.2 Trabajos previos (estado del arte).

Atiende C10: por cada trabajo se declara problema, contexto, idioma, datos,
tamano, etiquetado, herramientas, modelos, metricas, resultados, limitaciones y
relacion con SIREC. La tabla comparativa aparece al final como sintesis y el
apartado cierra con la brecha. Cuando una fuente no reporta un dato, se declara
como no reportado en lugar de estimarlo.
"""


def escribir(d):
    d.h3("Trabajos previos")

    d.p(
        "La revisión se organiza de lo general a lo particular: los trabajos que consolidaron el "
        "problema y produjeron los recursos de referencia del área, los que abordaron la "
        "clasificación con modelos neuronales y, por último, los dos antecedentes más próximos por "
        "lengua y dominio, ambos latinoamericanos. De cada uno se indica el problema atendido, el "
        "contexto y el idioma, los datos y su etiquetado, los modelos y métricas, los resultados y "
        "limitaciones, y su relación con este trabajo."
    )

    d.p(
        "El trabajo de Imran et al. (2015) es el punto de partida obligado: una revisión "
        "sistemática, publicada en ACM Computing Surveys, del procesamiento de mensajes de redes "
        "sociales durante emergencias masivas. No propone un sistema, sino que organiza el campo, "
        "identifica las etapas de la cadena de procesamiento —recolección, filtrado, clasificación, "
        "extracción y agregación— y señala los problemas abiertos, entre ellos la escasez de "
        "conjuntos etiquetados y la dificultad de operar en tiempo real. Su contexto es "
        "mayoritariamente anglófono y su unidad de análisis es el mensaje público, no el reporte "
        "dirigido a una autoridad; por su naturaleza no aporta corpus ni métricas propias. Su valor "
        "para SIREC es de encuadre y de vocabulario conceptual."
    )

    d.p(
        "En la línea de los recursos, Olteanu et al. (2014) presentaron CrisisLex, un léxico para "
        "recolectar y filtrar mensajes de crisis en inglés. Partieron de mensajes de varias crisis "
        "anotados manualmente por un lingüista y un especialista en gestión de emergencias, y "
        "produjeron un recurso de alrededor de 7 200 términos organizados en 23 categorías "
        "informativas, combinando anotación experta con trabajo colaborativo."
    )

    d.p(
        "El resultado reportado es una mejora sustancial de la exhaustividad en la recolección al "
        "añadir el léxico a las palabras clave elegidas por expertos. Su limitación frente a este "
        "trabajo es doble: opera en la fase de filtrado y no en la asignación de urgencia, y su "
        "naturaleza léxica lo hace dependiente del idioma y de la variedad regional."
    )

    d.p(
        "Alam et al. (2021) abordaron la fragmentación de los conjuntos de datos del área. Su "
        "trabajo, CrisisBench, consolida ocho fuentes anotadas en un punto de referencia común, con "
        "aproximadamente 166 100 mensajes para determinar si un mensaje es informativo y 141 500 "
        "para la clasificación de categorías humanitarias, unificando etiquetas heterogéneas y "
        "fijando particiones estándar."
    )

    d.p(
        "Los autores comparan modelos clásicos y basados en transformadores sobre esas particiones y "
        "muestran que un conjunto consolidado permite entrenar modelos más sólidos. Sus limitaciones "
        "aquí son el idioma, predominantemente inglés, y las etiquetas, que corresponden a categorías "
        "humanitarias y no a un criterio de urgencia operativa municipal; su aportación metodológica, "
        "en cambio, es directa, pues la práctica de fijar particiones reproducibles y comparar contra "
        "líneas base sobre los mismos datos es la que adopta el apartado 3.7."
    )

    d.p(
        "En cuanto a los modelos, Nguyen et al. (2016) aplicaron redes neuronales convolucionales a "
        "la clasificación de mensajes de crisis en inglés, en tareas binarias y multiclase, sobre "
        "datos de eventos reales. Su resultado principal es que los modelos neuronales superan a "
        "los métodos basados en rasgos diseñados manualmente y eliminan la necesidad de esa "
        "ingeniería, lo que reduce el trabajo de adaptación al cambiar de dominio o de evento. Sus "
        "limitaciones son las de la generación anterior a los modelos preentrenados: la "
        "representación no es contextual y el desempeño depende de contar con suficientes ejemplos "
        "etiquetados del evento. Para SIREC constituye la continuidad argumental que el ajuste fino "
        "lleva un paso más allá."
    )

    d.p(
        "El antecedente más próximo por dominio es el de Paltin et al. (2025), quienes desarrollaron "
        "un modelo para el servicio de emergencias ECU 911 de Ecuador que clasifica los incidentes e "
        "infiere su prioridad. Opera sobre transcripciones de llamadas en español y combina "
        "procesamiento del lenguaje natural con modelado semántico basado en ontologías y reglas "
        "lógicas, de modo que la asignación de prioridad resulta explicable a partir de las "
        "relaciones declaradas. Su fortaleza es esa trazabilidad, valiosa donde la decisión debe "
        "justificarse; sus limitaciones son que el paradigma es simbólico —generalizar ante "
        "expresiones no previstas depende de la cobertura de la ontología—, que la entrada es voz "
        "transcrita y que la variedad del español es la ecuatoriana."
    )

    d.p(
        "El segundo antecedente regional es el de Franco Cantos (2024), una tesis de maestría que "
        "construyó un modelo para identificar publicaciones de emergencia en la red social X para "
        "el caso de Ecuador. El autor conformó un corpus propio en español ecuatoriano, lo etiquetó "
        "manualmente y entrenó modelos clásicos sobre representaciones TF-IDF —regresión logística "
        "y máquinas de vectores de soporte—, evaluando con las métricas habituales de "
        "clasificación."
    )

    d.p(
        "La tarea resuelta es binaria, distinguir si una publicación corresponde o no a una "
        "emergencia, de modo que no aborda la categoría temática con varias clases ni el nivel de "
        "urgencia. El propio trabajo señala como línea futura la incorporación de modelos basados en "
        "transformadores, recomendación que este proyecto retoma. Su relación con SIREC es doble: "
        "evidencia que un corpus propio en español, aunque modesto, permite entrenar clasificadores "
        "útiles, y sitúa el modelo clásico TF-IDF como la línea base razonable de comparación. La "
        "tabla 4 sintetiza la comparación y añade la posición de la propuesta."
    )

    d.tabla(
        "Síntesis comparativa de los trabajos previos revisados",
        ["Trabajo", "Problema y contexto", "Idioma y datos", "Modelos y métricas",
         "Limitaciones frente a SIREC"],
        [
            ["Imran et al. (2015)",
             "Revisión del procesamiento de mensajes en emergencias masivas",
             "Inglés; sin corpus propio",
             "No aplica; sistematiza métodos",
             "No es solución operativa; no aborda urgencia ni español de México"],
            ["Olteanu et al. (2014)",
             "Recolección y filtrado de mensajes de crisis con léxico",
             "Inglés; ≈7 200 términos en 23 categorías",
             "Enfoque léxico; mejora la exhaustividad al recolectar",
             "Actúa en el filtrado, no en la urgencia; dependiente del idioma"],
            ["Nguyen et al. (2016)",
             "Clasificación binaria y multiclase de mensajes de crisis",
             "Inglés; datos de eventos reales",
             "Redes convolucionales; superan rasgos manuales",
             "Representación no contextual; español no contemplado"],
            ["Alam et al. (2021)",
             "Consolidación de conjuntos de datos en un punto de referencia",
             "Inglés; ≈166 100 y ≈141 500 mensajes de ocho fuentes",
             "Clásicos y transformadores con particiones estándar",
             "Etiquetas humanitarias, no de urgencia operativa"],
            ["Paltin et al. (2025)",
             "Clasificación e inferencia de prioridad en el ECU 911",
             "Español de Ecuador; transcripciones de llamadas (tamaño no reportado)",
             "PLN con ontologías y reglas; prioridad explicable",
             "Paradigma simbólico; entrada de voz; otra variedad del español"],
            ["Franco Cantos (2024)",
             "Identificación de publicaciones de emergencia en la red social X",
             "Español de Ecuador; corpus propio etiquetado a mano",
             "TF-IDF con regresión logística y SVM",
             "Tarea binaria; sin categoría ni urgencia; recomienda transformadores"],
            ["SIREC (propuesta)",
             "Doble clasificación y priorización en una coordinación municipal",
             "Español de México; corpus propio anonimizado, prueba 100 % real",
             "BETO ajustado frente a línea base TF-IDF; F1, kappa y latencia",
             "—"],
        ],
        pt_cuerpo=9.0,
        anchos=[2.6, 3.4, 3.5, 3.3, 3.7],
    )

    d.p(
        "Los trabajos revisados confirman la relevancia del problema y aportan piezas valiosas: un "
        "marco conceptual consolidado, recursos y conjuntos de datos de referencia, evidencia de que "
        "los modelos que aprenden representaciones superan a los basados en rasgos manuales, y dos "
        "experiencias hispanohablantes en el dominio. Ninguno, sin embargo, resuelve el problema "
        "planteado en este documento."
    )

    d.p(
        "La brecha se sitúa en la intersección de cuatro condiciones que ningún antecedente satisface "
        "a la vez. La primera es la doble clasificación por categoría temática y por nivel de urgencia "
        "sobre el mismo reporte, cuando los trabajos disponibles resuelven una tarea binaria, una "
        "clasificación temática o una inferencia de prioridad por reglas. La segunda es la variedad "
        "lingüística, pues el español de México no está representado en los corpus del área."
    )

    d.p(
        "La tercera es el canal y el destinatario, ya que aquí se trata de reportes escritos dirigidos "
        "a una autoridad municipal cuyo resultado debe integrarse en el flujo de trabajo de quien "
        "atiende. La cuarta es la existencia de un criterio de urgencia explícito y medido: ninguno de "
        "los trabajos reporta el acuerdo entre anotadores sobre esa asignación."
    )

