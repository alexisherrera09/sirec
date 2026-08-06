"""Anexo B: mapa de empatia y criterio operativo de urgencia.

Recoge el detalle tabulado al que remiten los apartados 3.1 y 3.2. Los anexos no
computan en la extension de 20 a 30 paginas (instrucciones de UNIR, 2.5).
"""


def escribir(d):
    d.anexo("Mapa de empatía y criterio operativo de urgencia")

    d.p(
        "Este anexo reúne el detalle tabulado de dos instrumentos elaborados en la etapa de "
        "desarrollo conceptual: el mapa de empatía de los dos perfiles de usuario, al que remite el "
        "apartado 3.1, y el criterio operativo con el que se asigna el nivel de urgencia a cada "
        "reporte, al que remite el apartado 3.2. Ambos se presentan aquí para no interrumpir la "
        "argumentación del cuerpo del documento."
    )

    d.h2_sin_numero("B.1 Mapa de empatía")

    d.tabla(
        "Mapa de empatía de los usuarios de SIREC",
        ["Usuario", "Dolores", "Beneficios esperados"],
        [
            ["Operador de protección civil",
             "Leer decenas de reportes uno por uno; riesgo de que un caso crítico quede sepultado "
             "por el orden de llegada; fatiga y decisiones bajo presión de tiempo; falta de un "
             "criterio común de urgencia",
             "Recibir los reportes ya ordenados por prioridad; ahorrar tiempo de lectura; reducir "
             "el riesgo de omitir un caso grave; concentrar el esfuerzo en decidir y despachar"],
            ["Ciudadano reportante",
             "Esperas largas y llamadas que no se contestan, el dolor más citado; muchas preguntas "
             "en plena emergencia; criterios de prioridad poco claros; incertidumbre sobre si el "
             "reporte fue recibido; baja confianza en que la ayuda llegará a tiempo",
             "Que un reporte con riesgo para la vida se atienda con prioridad; recibir confirmación "
             "y seguimiento del estatus; contar con un canal accesible que no dependa solo de la "
             "línea telefónica saturada"],
        ],
        fuente="Elaboración propia a partir del análisis del proceso, las visitas presenciales y "
               "las respuestas del formulario ciudadano.",
        anchos=[3.2, 6.4, 6.4],
    )

    d.h2_sin_numero("B.2 Criterio operativo de urgencia")

    d.tabla(
        "Criterio operativo de asignación del nivel de urgencia",
        ["Nivel", "Definición operativa", "Ejemplos de frontera"],
        [
            ["Alta",
             "Riesgo inminente para la vida o la integridad física de una o más personas",
             "Persona atrapada en una vivienda inundada; incendio con gente en el interior; persona "
             "herida en la vía pública; cable energizado caído sobre una persona"],
            ["Media",
             "Afectación relevante de bienes o servicios, o situación que puede escalar, sin "
             "peligro inmediato para las personas",
             "Vehículo volcado sin personas atrapadas; vivienda con daño estructural sin ocupantes "
             "en riesgo; poste caído que obstruye la circulación"],
            ["Baja",
             "Incidente menor o aviso de carácter informativo, sin afectación clara a personas",
             "Encharcamiento en la vía pública; cable colgando sin contacto; acumulación de basura "
             "tras la lluvia"],
        ],
        fuente="Elaboración propia; el criterio completo, con más ejemplos de frontera, se "
               "documenta en la guía de etiquetado del proyecto.",
        anchos=[1.8, 6.1, 8.1],
    )

    d.p(
        "El principio rector que acompaña a este criterio, aplicado por los anotadores ante la duda "
        "entre dos niveles, consiste en asignar el nivel superior cuando existen personas "
        "expuestas. Esta regla asimétrica es deliberada y coherente con el tratamiento que el "
        "apartado 3.7 da a los falsos negativos en las clases críticas."
    )
