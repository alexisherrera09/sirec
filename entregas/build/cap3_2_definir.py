"""3.2 Definir: reto, categorias, criterio de urgencia, corpus y criterios de desempeno."""


def escribir(d):
    d.h2("Definir")

    d.p(
        "Definir consiste en transformar los hallazgos de la etapa anterior en un problema claro "
        "y accionable, lo bastante concreto para poder resolverse y lo bastante medible para "
        "poder evaluarse. Este apartado formula primero el reto en términos de preguntas de "
        "diseño, después precisa las clases que el sistema debe distinguir y el criterio con el "
        "que se asigna la urgencia, a continuación documenta el origen del corpus con el que se "
        "entrenará el modelo y, por último, traduce cada necesidad detectada en un requerimiento "
        "con su criterio de desempeño."
    )

    d.h3("Formulación del reto")

    d.p(
        "El reto se formuló mediante enunciados del tipo «¿Cómo podríamos…?», una técnica que obliga "
        "a expresar el problema como una posibilidad de diseño y no como una queja. El equipo redactó "
        "cinco enunciados a partir de los dolores documentados."
    )

    d.p(
        "Los dos primeros abordan el cuello de botella y el orden de atención: cómo clasificar "
        "automáticamente cada reporte por tema y urgencia para que el operador no deba leerlos uno "
        "por uno, y cómo ordenarlos para que las situaciones con vidas en riesgo aparezcan siempre "
        "primero. Los tres restantes trasladan al plano técnico las restricciones detectadas: cómo "
        "maximizar la exhaustividad en las clases críticas, cómo construir y validar un corpus en "
        "español de México cuando no existe uno público, y cómo ofrecer la clasificación en tiempo "
        "real sin exponer datos sensibles ni depender de servicios de pago."
    )

    d.h3("Categorías temáticas y criterio de urgencia")

    d.p(
        "El sistema resuelve dos clasificaciones sobre un mismo texto: una asigna la categoría "
        "temática del incidente, con siete valores posibles, y otra el nivel de urgencia, con tres. "
        "La separación responde a que son decisiones de naturaleza distinta, pues la categoría "
        "determina qué área debe atender el reporte y la urgencia en qué orden se atiende; un mismo "
        "tema puede presentarse con niveles muy diferentes, de modo que tratarlas como una sola "
        "etiqueta compuesta sería menos informativo."
    )

    d.p(
        "Las siete categorías temáticas son inundación, persona en riesgo, caída de poste o "
        "cable, deslave, incendio, daño estructural y otro. Su elección no es arbitraria: "
        "recoge los tipos de emergencia más mencionados por las personas encuestadas y coincide "
        "con incidentes que el canal oficial registra de forma habitual en Veracruz, como "
        "cables colgando, caída de poste, incendio de casa habitación, árbol caído, inundaciones "
        "y derrumbes (Centro Nacional de Información, 2026). La categoría «otro» funciona como "
        "clase de reserva y permite medir cuánto del flujo real queda fuera del alcance "
        "temático del prototipo."
    )

    d.p(
        "El criterio de urgencia se define en función del riesgo para las personas, y el anexo B lo "
        "documenta con su definición operativa y ejemplos de frontera. La urgencia es alta cuando "
        "existe riesgo inminente para la vida o la integridad física, como una persona atrapada o "
        "un incendio con gente dentro; es media cuando hay una afectación relevante o una situación "
        "que puede escalar sin peligro inmediato, como un vehículo volcado sin personas atrapadas; "
        "y es baja en incidentes menores o informativos, como un encharcamiento. El principio "
        "rector, aplicado ante la duda, es que si hay personas expuestas se asigna el nivel "
        "superior."
    )

    d.p(
        "Ese criterio cumple una función que va más allá de la exposición: al fijar por escrito qué "
        "cuenta como urgencia alta, convierte en regla explícita aquello que hoy depende del juicio "
        "de cada operadora. El mismo texto reciben los anotadores del corpus, de modo que el acuerdo "
        "entre ellos, medido con el coeficiente kappa, estima hasta qué punto el criterio es "
        "reproducible."
    )

    d.h3("Origen y composición del corpus")

    d.p(
        "Como no existe un corpus público de reportes de emergencia en español de México para "
        "este dominio, el equipo construye uno propio. Los reportes reales proceden de fuentes "
        "públicas relativas a contingencias ocurridas en Veracruz, en particular publicaciones "
        "en redes sociales y notas de prensa que citan textualmente reportes ciudadanos, y se "
        "anonimizan antes de su uso mediante la eliminación de nombres, números telefónicos y "
        "direcciones exactas. Esta decisión responde también a la preocupación por la privacidad "
        "que manifestaron las instituciones visitadas."
    )

    d.p(
        "Ese conjunto se complementa con reportes sintéticos, declarados explícitamente como tales, "
        "cuya única función es reforzar la cobertura de las clases menos frecuentes durante el "
        "entrenamiento. La regla que el proyecto se impone es estricta: en ningún caso se evalúa el "
        "modelo con datos sintéticos, de modo que el conjunto de prueba es enteramente real. Su "
        "proporción y distribución por clase se reportan en el capítulo de metodología de la memoria "
        "final."
    )

    d.h3("De la necesidad al criterio de desempeño")

    d.p(
        "El último paso de esta etapa consiste en garantizar que ninguna necesidad quede sin una "
        "forma de comprobar que fue atendida. La tabla 3 recorre los hallazgos del apartado 3.1, "
        "los traduce en un requerimiento del sistema y asocia a cada uno un criterio de "
        "desempeño verificable, además de una prioridad que orientó el orden de construcción del "
        "prototipo."
    )

    d.tabla(
        "Trazabilidad entre necesidad detectada, requerimiento y criterio de desempeño",
        ["Necesidad detectada", "Requerimiento", "Criterio de desempeño", "Prioridad"],
        [
            ["Un caso crítico no puede quedar sepultado por el orden de llegada",
             "Priorizar por urgencia y por la categoría de persona en riesgo",
             "Exhaustividad alta en clases críticas, sin fugas hacia urgencia baja", "Alta"],
            ["El operador pierde tiempo leyendo todos los reportes",
             "Clasificar tema y urgencia al ingresar el reporte",
             "F1 por clase y macro superior a la del modelo de referencia", "Alta"],
            ["Los reportes usan el registro informal del español de México",
             "Modelo preentrenado en español ajustado con datos del dominio",
             "Mejora de la F1 macro frente a la línea base clásica", "Media"],
            ["Las etiquetas deben ser objetivas y reproducibles",
             "Guía de etiquetado explícita y doble anotación independiente",
             "Kappa de Cohen igual o superior a 0.60", "Alta"],
            ["La clasificación debe llegar a tiempo para ser útil",
             "Clasificación en línea al momento de la captura",
             "Latencia por debajo del umbral definido en 3.7", "Media"],
            ["No debe depender de servicios de pago ni exponer datos sensibles",
             "Modelos abiertos en infraestructura propia",
             "Costo nulo por predicción y sin envío de datos a terceros", "Media"],
        ],
        anchos=[4.3, 4.0, 5.2, 1.6],
    )

    d.p(
        "La tabla 3 opera como contrato interno del proyecto, pues cada fila enlaza una observación "
        "de campo con un indicador que se medirá en la evaluación. Conviene notar que dos de los "
        "seis criterios no dependen del modelo sino del método y de la arquitectura: el acuerdo "
        "entre anotadores y la independencia de servicios de pago no se resuelven con más "
        "entrenamiento."
    )
