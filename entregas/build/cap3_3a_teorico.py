"""3.3 Investigacion de antecedentes - 3.3.1 Fundamento teorico.

Atiende C9: prosa academica con citas que cubre representacion de texto, TF-IDF,
regresion logistica, SVM, clasificacion multiclase, Transformers, BERT, BETO,
tokenizacion, ajuste fino, desbalance, calibracion, metricas y acuerdo entre
evaluadores, ligando cada concepto con la decision de diseno de SIREC que lo usa.
"""


def escribir(d):
    d.h2("Investigación de antecedentes")

    d.p(
        "Este apartado conecta el problema con el conocimiento existente en dos movimientos. "
        "Primero establece el fundamento teórico que sustenta las decisiones técnicas del "
        "proyecto, recorriendo la representación del texto, los modelos de clasificación clásicos "
        "y neuronales, y los instrumentos con los que se mide tanto la calidad de las etiquetas "
        "como el desempeño del sistema. Después revisa los trabajos previos que han abordado "
        "problemas equivalentes, para cerrar con la identificación de la brecha que SIREC cubre."
    )

    d.h3("Fundamento teórico")

    d.p(
        "La tarea que resuelve SIREC pertenece a la clasificación automática de texto, una de las "
        "aplicaciones más consolidadas del procesamiento del lenguaje natural. Formalmente, "
        "clasificar consiste en asignar a un documento una etiqueta tomada de un conjunto finito y "
        "predefinido, a partir de un modelo aprendido de ejemplos previamente etiquetados (Manning "
        "et al., 2008). Aquí el documento es un reporte de pocas oraciones y el problema se "
        "resuelve como dos clasificaciones independientes sobre el mismo texto: una de siete clases "
        "para la categoría temática y otra de tres para el nivel de urgencia."
    )

    d.p(
        "El primer requisito es representar el texto de una forma que un algoritmo pueda procesar. "
        "La representación clásica es la bolsa de palabras, que describe cada documento por la "
        "presencia o frecuencia de sus términos y descarta el orden. Sobre ella, el esquema de "
        "ponderación TF-IDF asigna a cada término un peso que crece con su frecuencia en el "
        "documento y decrece con su frecuencia en la colección, de modo que las palabras muy "
        "repartidas pierden influencia y las distintivas la ganan (Salton y Buckley, 1988). Es una "
        "representación dispersa, interpretable y económica de calcular."
    )

    d.p(
        "Su limitación resulta especialmente relevante en este dominio. Al prescindir del orden y "
        "tratar cada término como un símbolo independiente, TF-IDF no distingue entre «no hay "
        "personas atrapadas» y «hay personas atrapadas» más allá de la presencia del adverbio, ni "
        "reconoce como equivalentes dos formas de decir lo mismo con palabras distintas. En un "
        "corpus con registro informal y erratas, cada variante de escritura constituye además un "
        "término nuevo, lo que fragmenta la señal."
    )

    d.p(
        "Sobre esta representación operan los modelos clásicos que el proyecto emplea como línea "
        "base. La regresión logística modela la probabilidad de cada clase mediante una "
        "combinación lineal de los pesos de los términos transformada por una función logística, y "
        "su extensión multinomial trata directamente problemas de más de dos clases. Las máquinas "
        "de vectores de soporte buscan el hiperplano que separa las clases con el mayor margen "
        "posible (Cortes y Vapnik, 1995) y han mostrado un desempeño sólido en categorización de "
        "texto, donde los rasgos son numerosos y los vectores dispersos (Joachims, 1998)."
    )

    d.p(
        "En problemas multiclase, estos modelos se extienden mediante estrategias de descomposición "
        "—uno contra el resto— o formulaciones multinomiales que estiman una distribución sobre todas "
        "las clases. La distinción determina si el modelo entrega una puntuación comparable entre "
        "clases, condición necesaria para ordenar los reportes por prioridad."
    )

    d.p(
        "El segundo enfoque proviene del aprendizaje profundo aplicado al lenguaje. La arquitectura "
        "Transformer sustituyó la recurrencia por un mecanismo de atención que relaciona todas las "
        "posiciones de una secuencia entre sí, lo que permite capturar dependencias a distancia y "
        "paralelizar el entrenamiento (Vaswani et al., 2017). Sobre ella, BERT introdujo el "
        "preentrenamiento bidireccional profundo mediante tareas autosupervisadas sobre grandes "
        "volúmenes de texto sin etiquetar (Devlin et al., 2019). La diferencia esencial respecto de "
        "TF-IDF es que produce representaciones contextuales: el vector de una palabra depende de "
        "las que la rodean, propiedad decisiva cuando la negación y el contexto determinan la "
        "urgencia."
    )

    d.p(
        "Un modelo preentrenado en inglés, sin embargo, no resuelve un problema en español. BETO es "
        "un modelo de la familia BERT preentrenado con un corpus extenso en español, con resultados "
        "competitivos en tareas de esa lengua (Cañete et al., 2020). Su disponibilidad como modelo "
        "abierto es determinante aquí por dos razones: permite trabajar en la lengua del corpus y "
        "hace posible ejecutar la clasificación en infraestructura propia, sin enviar los reportes "
        "a terceros, lo que responde a la preocupación por la privacidad recogida en el trabajo de "
        "campo."
    )

    d.p(
        "Estos modelos no operan sobre palabras completas sino sobre subpalabras. Los algoritmos de "
        "tokenización de subpalabras, como la codificación por pares de bytes (Sennrich et al., "
        "2016) y las implementaciones independientes del idioma que la generalizan (Kudo y "
        "Richardson, 2018), descomponen cada término en unidades frecuentes, de modo que una "
        "palabra desconocida se representa como combinación de fragmentos conocidos en lugar de "
        "perderse. Con modismos, abreviaturas y erratas, esta propiedad reduce el problema del "
        "vocabulario fuera de rango que afecta a las representaciones clásicas."
    )

    d.p(
        "El aprovechamiento del modelo preentrenado para una tarea concreta se realiza mediante "
        "transferencia de aprendizaje. El procedimiento habitual, el ajuste fino, añade una capa de "
        "clasificación sobre la representación del modelo y continúa el entrenamiento con los datos "
        "etiquetados de la tarea, actualizando los pesos preentrenados con una tasa de aprendizaje "
        "reducida (Howard y Ruder, 2018). Requiere órdenes de magnitud menos ejemplos que entrenar "
        "desde cero —decisivo cuando el corpus se construye a mano— y hoy es un estándar de la "
        "práctica gracias a las bibliotecas que agrupan modelos y rutinas de ajuste (Wolf et al., "
        "2020)."
    )

    d.p(
        "Un problema que este dominio impone de manera inevitable es el desbalance entre clases: "
        "las emergencias más graves son, afortunadamente, las menos frecuentes, de modo que las "
        "clases críticas están subrepresentadas en cualquier muestra natural. El desbalance sesga a "
        "los clasificadores hacia las clases mayoritarias y degrada su desempeño en las "
        "minoritarias (Japkowicz y Stephen, 2002); entre las estrategias para atenuarlo están el "
        "remuestreo, la generación de ejemplos sintéticos de las clases escasas (Chawla et al., "
        "2002) y la ponderación de la función de pérdida. En SIREC el problema se agrava porque la "
        "clase minoritaria es precisamente la que no puede fallar."
    )

    d.p(
        "Cuando la salida del modelo se muestra a una persona, además de acertar la clase importa "
        "que la confianza asociada sea creíble. Las redes neuronales profundas tienden a estar mal "
        "calibradas y a producir probabilidades más altas que su acierto real, aunque existen "
        "procedimientos posteriores al entrenamiento que corrigen ese sesgo (Guo et al., 2017). "
        "Para el panel del operador la propiedad es funcional: la confianza es el criterio con el "
        "que se decide qué predicciones se marcan para revisión humana, de modo que una confianza "
        "inflada convertiría ese mecanismo en un adorno."
    )

    d.p(
        "La evaluación del desempeño se apoya en métricas derivadas de la matriz de confusión. La "
        "precisión indica qué proporción de las predicciones de una clase es correcta; la "
        "exhaustividad, qué proporción de los casos reales de esa clase fue recuperada; y la medida "
        "F1 resume ambas en su media armónica. En problemas multiclase se calculan por clase y se "
        "agregan: el promedio macro otorga igual peso a cada clase con independencia de su "
        "frecuencia, a diferencia del micro, que favorece a las clases numerosas (Sokolova y "
        "Lapalme, 2009). La elección tiene consecuencias operativas, pues un sistema que acertara "
        "todos los encharcamientos y fallara todas las personas atrapadas exhibiría una exactitud "
        "elevada y sería inservible."
    )

    d.p(
        "Finalmente, ninguna de estas métricas tiene sentido si las etiquetas contra las que se "
        "comparan no son confiables. La concordancia entre anotadores humanos se mide con el "
        "coeficiente kappa de Cohen, que descuenta el acuerdo atribuible al azar (Cohen, 1960); sus "
        "valores se interpretan mediante escalas convencionales que sitúan el acuerdo sustancial "
        "por encima de 0.60 (Landis y Koch, 1977), si bien la literatura advierte que esos cortes "
        "son orientativos y deben leerse junto con la guía de anotación (Artstein y Poesio, 2008). "
        "Si la urgencia se asigna hoy de forma subjetiva, medir ese acuerdo es la evidencia de que "
        "el criterio propuesto resulta comunicable y reproducible."
    )
