"""Capitulo 1 - Introduccion.

Atiende C3 y C7: prosa academica, 2-3 paginas, con contexto, problema,
justificacion, proposito, alcance y estructura, sustentado con estadisticas
oficiales citadas (Cenapred 2024; CNI 2025, 2026; Valdes-Rodriguez 2025).
"""


def escribir(d):
    d.h1("Introducción", salto=False)

    d.p(
        "Este primer capítulo presenta el trabajo al lector y delimita el terreno sobre el "
        "que se construye la propuesta de innovación. Comienza con el contexto de las "
        "emergencias de origen natural en México y, en particular, en el estado de Veracruz; "
        "continúa con el planteamiento del problema concreto que se aborda —el triaje manual "
        "de los reportes ciudadanos— y con su justificación a partir de datos oficiales; y "
        "cierra con la delimitación del alcance y con la explicación de cómo se organiza el "
        "resto del documento."
    )

    d.h2("Contexto y motivación")

    d.p(
        "México es un país expuesto de forma recurrente a fenómenos de origen natural cuyo impacto "
        "social y económico se documenta cada año. Según el Centro Nacional de Prevención de "
        "Desastres, durante 2023 los desastres ocurridos en el país dejaron daños y pérdidas por "
        "88 910 millones de pesos, equivalentes a 0.3 % del producto interno bruto, y 984 "
        "defunciones confirmadas; de esos daños, 98.1 % correspondió a fenómenos "
        "hidrometeorológicos, a los que se asoció también el 52.2 % de las defunciones (Cenapred, "
        "2024)."
    )

    d.p(
        "Veracruz ocupa un lugar destacado en ese panorama. En 2023 concentró 7.0 % de las "
        "defunciones causadas por fenómenos de origen natural y fue escenario de dos de los seis "
        "eventos hidrometeorológicos más costosos del año: la lluvia severa con inundación fluvial "
        "y pluvial de octubre y la tormenta tropical Max de agosto (Cenapred, 2024). La "
        "recurrencia no es excepcional, pues el análisis de las declaratorias de desastre "
        "registradas entre 2003 y 2022 muestra que las afectaciones hidrometeorológicas son un "
        "fenómeno sostenido en el territorio veracruzano (Valdés-Rodríguez, 2025)."
    )

    d.p(
        "Cuando una contingencia ocurre, la ciudadanía acude al canal institucional de emergencia y "
        "las coordinaciones municipales de protección civil se convierten en el primer punto de "
        "contacto con la respuesta del Estado. El volumen de ese canal es considerable: entre enero "
        "y junio de 2026 los Centros de Atención de Llamadas de Emergencia registraron 27 204 813 "
        "llamadas al número único 9-1-1, de las cuales 7 620 591 se canalizaron a alguna "
        "corporación por relacionarse con hechos que ponen en riesgo a las personas; Veracruz "
        "aportó 1 475 239 y se ubicó en el sexto lugar nacional (Centro Nacional de Información, "
        "2026)."
    )

    d.p(
        "Esas cifras describen también la dificultad de fondo. El 72.0 % de las llamadas recibidas en "
        "el país resultó improcedente —llamadas mudas, incompletas, bromas o asuntos ajenos a una "
        "emergencia—, proporción que en Veracruz asciende a 77.3 % (Centro Nacional de Información, "
        "2026)."
    )

    d.p(
        "A esa carga se añade la granularidad de la clasificación. El Catálogo Nacional de Incidentes "
        "de Emergencia comprende siete tipos de incidente, 24 subtipos y 282 incidentes específicos "
        "(Centro Nacional de Información, 2025), y en el primer semestre de 2026 se registraron "
        "llamadas en 206 de ellos. Quien atiende un reporte no resuelve una decisión binaria, sino "
        "una clasificación de grano fino tomada en segundos, y de ahí que el triaje sea un punto "
        "crítico de la cadena de respuesta. La tabla 1 resume estas magnitudes."
    )

    d.tabla(
        "Llamadas de emergencia al número único 9-1-1 en México y en Veracruz, enero–junio de 2026",
        ["Indicador", "Nacional", "Veracruz"],
        [
            ["Llamadas registradas", "27 204 813", "1 475 239"],
            ["Llamadas procedentes (canalizadas a una corporación)", "7 620 591 (28.0 %)", "334 843 (22.7 %)"],
            ["Llamadas improcedentes", "19 584 222 (72.0 %)", "1 140 396 (77.3 %)"],
        ],
        fuente="Elaboración propia con datos abiertos del Centro Nacional de Información (2026).",
        anchos=[8.5, 4.0, 3.5],
    )

    d.h2("Planteamiento del problema")

    d.p(
        "El problema que motiva este trabajo es que el triaje de los reportes ciudadanos de "
        "emergencia se realiza de forma manual y sin un criterio de urgencia documentado, "
        "justo en el momento en que cada minuto cuenta. Los reportes llegan redactados en "
        "lenguaje natural, con las palabras de quien los emite, y alguien debe leerlos, "
        "interpretarlos, decidir a qué área corresponden y establecer qué tan urgentes son. "
        "Cuando decenas o cientos de reportes coinciden durante una contingencia, esa lectura "
        "secuencial se convierte en un cuello de botella."
    )

    d.p(
        "El efecto de ese cuello de botella no es administrativo. Un reporte crítico —por "
        "ejemplo, «hay una persona atrapada y el agua sigue subiendo»— puede permanecer en espera "
        "detrás de reportes menos graves por la única razón de haber llegado después, y en un "
        "dominio donde la variable relevante es el riesgo para la vida el orden de atención "
        "determina consecuencias humanas. A esta limitación de capacidad se añade una de método, "
        "constatada en el trabajo de campo del apartado 3.1: la urgencia se determina hoy según el "
        "criterio individual de cada operadora, sin una regla explícita, de modo que dos reportes "
        "equivalentes pueden recibir prioridades distintas según quién los atienda."
    )

    d.p(
        "El problema puede enunciarse entonces en los siguientes términos: no existe, para el "
        "español de México y en el contexto de una coordinación municipal de protección civil, "
        "un mecanismo que clasifique y ordene automáticamente los reportes ciudadanos según su "
        "nivel de riesgo, de modo que la atención se dirija primero a donde más se necesita y "
        "que el criterio aplicado sea explícito y verificable."
    )

    d.h2("Justificación")

    d.p(
        "La relevancia de atender este problema se sostiene en tres razones. La primera es el "
        "impacto potencial: en un dominio donde el tiempo de respuesta se vincula con la protección "
        "de la vida, reducir el intervalo entre la recepción de un reporte y su atención tiene un "
        "valor social directo. La segunda es la pertinencia tecnológica, pues la clasificación "
        "automática de texto corto es una tarea consolidada del procesamiento del lenguaje natural, "
        "con modelos preentrenados disponibles en español."
    )

    d.p(
        "La tercera razón es la existencia de un vacío específico. La literatura de informática "
        "de crisis ha documentado ampliamente el análisis de mensajes ciudadanos durante "
        "desastres y ha liberado recursos y conjuntos de datos de referencia, aunque "
        "principalmente en inglés y sobre mensajes de redes sociales (Imran et al., 2015; "
        "Alam et al., 2021). Los trabajos disponibles en español para el dominio de emergencias "
        "son escasos, se concentran en otras variedades regionales y no abordan de manera "
        "conjunta la clasificación temática y la estimación de urgencia. Ese vacío es el que "
        "este trabajo aborda, y el apartado 3.3 lo documenta con detalle."
    )

    d.h2("Alcance")

    d.p(
        "El presente trabajo se delimita al desarrollo y la evaluación de un producto mínimo viable "
        "del Sistema Inteligente de Reportes de Emergencia Ciudadana, en adelante SIREC, y no de un "
        "sistema comercial completo ni de un despliegue gubernamental. El foco está en el componente "
        "de inteligencia artificial y en su integración operativa, de modo que la propuesta pueda "
        "demostrarse de principio a fin con un alcance abordable en el tiempo disponible. En "
        "concreto, el alcance comprende los siguientes elementos:"
    )

    d.vineta([
        "Doble clasificación de cada reporte: en siete categorías temáticas —inundación, persona en "
        "riesgo, caída de poste o cable, deslave, incendio, daño estructural y otro— y en tres "
        "niveles de urgencia (alta, media y baja).",
        "Priorización operativa: los reportes se presentan en un panel ordenado por prioridad.",
        "Canal de entrada acotado: un formulario web como única vía de captura, dejando otros "
        "canales como trabajo futuro gracias a una arquitectura desacoplada.",
        "Caso de uso acotado: una coordinación municipal como caso de estudio, sin pretender la "
        "adopción institucional real durante el trabajo.",
    ])

    d.p(
        "Quedan fuera del alcance la atención telefónica y la transcripción de voz, la gestión "
        "administrativa posterior al triaje, el despacho de recursos y el seguimiento del "
        "estatus del reporte por parte del ciudadano. Este último punto merece una mención "
        "explícita porque surgió como necesidad en el trabajo de campo: se registra como "
        "requerimiento de valor y línea futura, sin ampliar el alcance comprometido. La "
        "validación experimental completa, con sus resultados, corresponde al capítulo de "
        "validación y diseño experimental de la memoria final; en esta entrega se documenta su "
        "diseño en el apartado 3.7."
    )

    d.h2("Estructura del documento")

    d.p(
        "El documento se organiza en tres capítulos, seguidos de las referencias bibliográficas y "
        "de un anexo. El capítulo 1 presenta el contexto, el problema, su justificación y el "
        "alcance. El capítulo 2 formula el objetivo general y los objetivos específicos que "
        "conducen a él, junto con la forma en que se medirá su cumplimiento. El capítulo 3 "
        "constituye el núcleo de esta entrega y desarrolla la concepción de la solución mediante "
        "la metodología Design Thinking."
    )

    d.p(
        "Dentro de ese tercer capítulo, el apartado 3.1 documenta la etapa de empatía con los "
        "usuarios; el 3.2 traduce esos hallazgos en un problema accionable, con el criterio de "
        "urgencia y los criterios de desempeño; el 3.3 establece el fundamento teórico y revisa "
        "los trabajos previos para delimitar la brecha; el 3.4 genera y evalúa alternativas; el "
        "3.5 describe el prototipo con su arquitectura y sus pantallas; el 3.6 justifica la "
        "selección mediante una matriz ponderada; y el 3.7 define el protocolo de evaluación. El "
        "anexo A recoge el instrumento de la encuesta ciudadana y sus resultados."
    )
