"""Anexo A: instrumento de la encuesta ciudadana y resultados agregados.

Los anexos empiezan en pagina nueva, conservan el estilo del documento y no
computan en la extension de 20 a 30 paginas (instrucciones de UNIR, 2.5).
"""


def escribir(d):
    d.anexo("Instrumento de empatía y resultados de la encuesta ciudadana")

    d.p(
        "Como parte de la etapa de empatía descrita en el apartado 3.1 se aplicó una encuesta "
        "ciudadana anónima mediante un formulario en línea, difundido entre personas que "
        "hubieran vivido o presenciado una emergencia. El instrumento no recoge nombres, "
        "teléfonos ni direcciones, y se respondió con fines exclusivamente académicos. Se "
        "recibieron 42 respuestas. Este anexo reproduce el cuestionario, los resultados "
        "agregados y una selección de respuestas textuales anonimizadas."
    )

    d.h2_sin_numero("A.1 Preguntas del instrumento")

    d.numerada([
        "¿Has vivido o presenciado una emergencia en tu localidad? (opción única)",
        "¿Qué tipo de emergencia? (casillas: inundación, deslave, incendio, caída de poste o "
        "cable, persona en riesgo, otro)",
        "¿Reportaste o intentaste reportar la emergencia? (opción única)",
        "Si reportaste, ¿por qué medio? (casillas: 9-1-1, redes sociales, mensajería "
        "instantánea, en persona, no reporté, otro)",
        "¿Qué fue lo más difícil o frustrante al pedir o dar aviso de ayuda? (texto libre)",
        "¿Supiste si tu reporte fue recibido o atendido? (opción única)",
        "¿Qué tan seguro o segura estabas de que la ayuda llegaría a tiempo? (escala de 1 a 5)",
        "¿Qué te habría gustado que pasara con tu reporte? (texto libre)",
        "Si pudieras pedir una sola cosa a un sistema que recibe estos reportes, ¿cuál sería? "
        "(texto libre)",
    ])

    d.h2_sin_numero("A.2 Resultados agregados")

    d.p(
        "La tabla 9 presenta los tipos de emergencia mencionados por las personas encuestadas. "
        "Al tratarse de una pregunta de opción múltiple, la suma de menciones excede el número de "
        "respuestas del cuestionario."
    )

    d.tabla(
        "Tipos de emergencia mencionados por las personas encuestadas",
        ["Tipo de emergencia", "Menciones"],
        [
            ["Inundación", "17"],
            ["Caída de poste o cable", "17"],
            ["Otro", "11"],
            ["Incendio", "10"],
            ["Persona en riesgo", "10"],
            ["Deslave", "3"],
        ],
        fuente="Elaboración propia con las respuestas del formulario (pregunta de opción "
               "múltiple, n = 42).",
        anchos=[9.0, 4.0],
    )

    d.p(
        "La tabla 10 reúne los indicadores principales del instrumento, a los que remite el apartado "
        "3.1. Las proporciones se calculan sobre el total de 42 respuestas, salvo en la escala de "
        "confianza, donde se indican las respuestas válidas. Los porcentajes se redondean a la unidad."
    )

    d.tabla(
        "Indicadores principales de la encuesta ciudadana (n = 42)",
        ["Indicador", "Resultado"],
        [
            ["Respuestas recogidas", "42"],
            ["Han vivido o presenciado una emergencia", "83 % (35 de 42)"],
            ["Reportaron / lo intentaron sin lograrlo / no reportaron", "50 % / 17 % / 33 %"],
            ["Principal canal de reporte",
             "Llamada al 9-1-1 (22 menciones); uso marginal de medios digitales"],
            ["No supieron si su reporte fue atendido", "8 personas"],
            ["Confianza en que la ayuda llegaría a tiempo (escala 1 a 5)",
             "Media de 2.3; el 64 % la califica con 1 o 2"],
            ["Emergencias más mencionadas", "Inundación (17) y caída de poste o cable (17)"],
        ],
        fuente="Elaboración propia con las respuestas del formulario aplicado.",
        anchos=[9.0, 7.0],
    )

    d.p(
        "En cuanto a la confianza en que la ayuda llegaría a tiempo, medida en una escala de 1 "
        "—nada seguro— a 5 —totalmente seguro—, se obtuvieron 36 respuestas válidas con una media "
        "de 2.3. El 64 % de las personas la calificó con 1 o 2, y solo el 17 % con 4 o 5. Este "
        "resultado es el que se interpreta en el apartado 3.1 como evidencia de la baja confianza "
        "ciudadana en la respuesta institucional."
    )

    d.h2_sin_numero("A.3 Voces de la ciudadanía")

    d.p(
        "Las respuestas de texto libre se transcriben literalmente y sin datos identificatorios. "
        "Sobre lo más difícil o frustrante al pedir ayuda, las personas encuestadas señalaron:"
    )

    d.vineta([
        "«El tiempo de respuesta, la demora para la atención.»",
        "«No contestaban las llamadas.»",
        "«La lentitud con la que atienden y piden datos.»",
        "«La falta de empatía y la cantidad de preguntas aún en medio de la emergencia.»",
        "«Me dijeron que como aún no había nadie en riesgo, atenderían otras prioridades… fue "
        "súper frustrante.»",
    ])

    d.p(
        "Sobre lo que les habría gustado que ocurriera con su reporte y lo que pedirían a un "
        "sistema que los recibe, las respuestas fueron:"
    )

    d.vineta([
        "«Que me indicara si mi reporte tiene prioridad o en qué estatus está.»",
        "«Monitoreo de la cuadrilla asignada a la resolución del incidente.»",
        "«Trazabilidad del estatus del reporte; por ejemplo, si pedí una ambulancia, poder ver "
        "por dónde viene.»",
        "«Que tengan otros medios de comunicación donde no se sature rápido para comunicarse.»",
        "«Aviso a las autoridades y atención por nivel de emergencia.»",
    ])

    d.p(
        "La última cita resulta especialmente pertinente para este trabajo, porque expresa en "
        "palabras de la ciudadanía la función que el sistema propuesto cumple: que la atención se "
        "organice por nivel de emergencia. Las peticiones de trazabilidad y seguimiento, "
        "reiteradas en varias respuestas, quedan registradas como línea de trabajo futuro según "
        "se declaró al delimitar el alcance."
    )
