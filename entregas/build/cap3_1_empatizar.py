"""3.1 Empatizar.

Vinetas de hallazgos convertidas a prosa (C11), subsecciones numeradas (C6) y
tablas interpretadas desde el texto (C11). El detalle tabulado del mapa de
empatia se traslada al anexo B para no inflar el cuerpo del documento.
"""


def escribir(d):
    d.h2("Empatizar")

    d.p(
        "La etapa de empatía persigue conocer al usuario final antes de proponerle una solución: "
        "sus necesidades, sus frustraciones y las condiciones en que trabaja o pide ayuda. En el "
        "caso de SIREC concurren dos usuarios con posiciones muy distintas frente al mismo suceso: "
        "la persona que reporta una emergencia y quien la recibe y decide qué hacer con ella. Este "
        "apartado describe las técnicas empleadas para comprender a ambos, los perfiles "
        "resultantes, el mapa de empatía y los hallazgos que orientaron el resto del trabajo."
    )

    d.h3("Técnicas empleadas y perfiles de usuario")

    d.p(
        "El equipo combinó tres técnicas complementarias. La primera fue el análisis del proceso y "
        "la observación documental del triaje manual en una coordinación municipal de protección "
        "civil, junto con la revisión de reportes ciudadanos reales publicados durante contingencias "
        "pasadas en Veracruz, tomados de redes sociales y de notas de prensa que los citan "
        "textualmente. La segunda fue una encuesta ciudadana anónima aplicada mediante un "
        "formulario en línea. La tercera consistió en dos visitas presenciales a instancias que "
        "reciben y priorizan reportes de emergencia."
    )

    d.p(
        "Esta combinación responde a una limitación del acceso al campo: las instituciones de "
        "emergencia no facilitan el detalle de su operación interna, de modo que la voz del operador "
        "se reconstruyó a partir de la observación y de las visitas. La tabla 2 sintetiza los dos "
        "perfiles con los que se trabajó."
    )

    d.tabla(
        "Perfiles de usuario considerados en la etapa de empatía",
        ["Actor", "Perfil y rol", "Contexto de uso", "Método de estudio"],
        [
            ["Operador de protección civil",
             "Personal que recibe, lee y despacha los reportes; decide la prioridad de atención "
             "bajo presión de tiempo",
             "Sala de coordinación durante una contingencia, con alto volumen simultáneo de "
             "reportes",
             "Análisis del proceso, observación documental y dos visitas presenciales"],
            ["Ciudadano reportante",
             "Persona afectada o testigo que describe la emergencia con sus propias palabras",
             "En campo, en situación de estrés, con redacción informal y modismos del español de "
             "México",
             "Revisión de reportes públicos reales y encuesta anónima (n = 42)"],
        ],
        anchos=[3.2, 4.3, 4.3, 4.2],
    )

    d.p(
        "La tabla 2 hace explícita una asimetría que condiciona el diseño: el ciudadano produce el "
        "texto en condiciones adversas y sin formato, mientras que el operador debe interpretarlo "
        "con rapidez. La solución no puede exigir al ciudadano que escriba mejor ni al operador que "
        "lea más rápido, sino que debe intervenir en el punto intermedio, ordenando la entrada antes "
        "de que llegue a la vista humana."
    )

    d.h3("Acercamiento presencial a las autoridades de emergencia")

    d.p(
        "Durante la semana del 13 de julio de 2026 el equipo realizó dos visitas presenciales a "
        "instancias que hoy reciben y priorizan reportes de emergencia: la Unidad de Protección "
        "Civil de la Alcaldía Venustiano Carranza, en la Ciudad de México, y la Comandancia de la "
        "Policía Municipal de Veracruz. El propósito era conocer, de la voz del usuario final, cómo "
        "se determina en la práctica el nivel de urgencia de cada reporte que ingresa."
    )

    d.p(
        "En ambos casos se explicó que existe un sistema donde las operadoras registran las urgencias "
        "y, a partir de ese registro, se despachan las patrullas o los servicios. Sin embargo, de los "
        "comentarios del personal se desprende que son las propias operadoras quienes determinan el "
        "nivel de urgencia de forma subjetiva, con base en la conversación con quien reporta y sin un "
        "criterio estandarizado explícito; al intentar profundizar en las herramientas empleadas, se "
        "mostraron renuentes por razones de privacidad institucional."
    )

    d.p(
        "El acercamiento no permitió documentar un procedimiento formal, pero constituye un hallazgo "
        "central: la urgencia depende hoy del criterio individual de cada operadora y no de una regla "
        "reproducible. Esa ausencia es la necesidad que SIREC cubre mediante una guía de etiquetado "
        "explícita y un criterio validado entre anotadores, y la reticencia observada confirma la "
        "pertinencia de trabajar solo con datos anonimizados. Como limitación, el acceso restringido "
        "impidió cuantificar tiempos de triaje de la práctica actual, de modo que los criterios de "
        "éxito del apartado 3.7 se definen sobre el desempeño del sistema."
    )

    d.h3("Resultados de la encuesta ciudadana")

    d.p(
        "Para incorporar la voz del usuario final se aplicó una encuesta anónima mediante un "
        "formulario en línea, difundido entre personas que hubieran vivido o presenciado una "
        "emergencia. El instrumento consta de nueve preguntas, no recoge datos personales y se "
        "reproduce íntegro en el anexo A junto con la tabla de indicadores. Se obtuvieron 42 "
        "respuestas, de las cuales 35 corresponden a personas con experiencia directa."
    )

    d.p(
        "Los resultados confirman el problema desde la perspectiva de quien reporta. El canal "
        "telefónico es hoy prácticamente el único empleado —22 menciones corresponden a la llamada "
        "al 9-1-1—, lo que respalda habilitar un formulario web como vía alterna de captura; la "
        "confianza en la respuesta es baja, con una media de 2.3 sobre 5 y casi dos tercios de las "
        "calificaciones en los dos valores inferiores; y las emergencias más mencionadas "
        "—inundación y caída de poste o cable— coinciden con los incidentes que el canal oficial "
        "registra con más frecuencia en Veracruz, donde en el primer semestre de 2026 se "
        "contabilizaron 1 123 llamadas por cables colgando y 376 por caída de poste (Centro "
        "Nacional de Información, 2026)."
    )

    d.p(
        "Conviene acotar el alcance de esta evidencia: es una muestra no probabilística, obtenida por "
        "difusión abierta del formulario, por lo que sus resultados no son generalizables. Su función "
        "es cualitativa —identificar dolores y expectativas reales que orienten el diseño—, no "
        "estimar parámetros poblacionales."
    )

    d.h3("Mapa de empatía")

    d.p(
        "A partir de las tres técnicas descritas se construyó el mapa de empatía que recoge el "
        "anexo B. El operador declara como dolores la lectura de decenas de reportes uno por uno, el "
        "riesgo de que un caso crítico quede sepultado por el orden de llegada y la falta de un "
        "criterio común de urgencia; espera recibir los reportes ya ordenados por prioridad. El "
        "ciudadano señala las esperas y las llamadas sin respuesta, el exceso de preguntas en plena "
        "emergencia y la incertidumbre sobre la recepción de su reporte; espera que un caso con "
        "riesgo para la vida se atienda primero y poder seguir su estatus."
    )

    d.p(
        "El contraste entre ambos perfiles revela que comparten una misma necesidad expresada de "
        "formas distintas, pues tanto el operador como el ciudadano piden que el orden de atención "
        "refleje el riesgo. Esa coincidencia justifica que la priorización automática sea el centro "
        "de la propuesta."
    )

    d.h3("Hallazgos clave")

    d.p(
        "El primer hallazgo es que el operador no necesita otra bandeja de mensajes, sino una lista "
        "ya ordenada por riesgo: las herramientas que se limitan a concentrar reportes le trasladan "
        "el trabajo de leerlos todos, que es el cuello de botella observado. El valor de la solución "
        "reside, por tanto, en la decisión de orden que entrega."
    )

    d.p(
        "El segundo hallazgo señala cuál es la señal de urgencia determinante: la presencia de "
        "personas en peligro. De ello se desprende una consecuencia técnica que atraviesa todo el "
        "trabajo, y es que el error más costoso no es una confusión temática cualquiera, sino un "
        "falso negativo en las clases críticas; por eso la evaluación del apartado 3.7 privilegia la "
        "exhaustividad en esas clases. El tercero se refiere al lenguaje: los reportes reales "
        "emplean registro informal y modismos del español de México, escritos con prisa y sin "
        "corrección, lo que orienta la solución hacia un modelo preentrenado en español y ajustado "
        "con datos del propio dominio."
    )

    d.p(
        "El cuarto hallazgo proviene de las visitas presenciales: la urgencia se fija hoy de manera "
        "subjetiva y sin criterio documentado, lo que convierte la guía de etiquetado del proyecto "
        "en un aporte por sí mismo, más allá del modelo. El quinto es una necesidad que el producto "
        "mínimo viable no cubre, pues varias personas encuestadas pidieron seguimiento y "
        "trazabilidad del estatus de su reporte; se registra como requerimiento de valor y línea de "
        "trabajo futuro, sin ampliar el alcance comprometido."
    )
