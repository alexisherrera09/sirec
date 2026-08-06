"""3.5 Prototipar.

Atiende C13: figura propia de arquitectura con entradas, salidas y conexiones;
wireframes de las pantallas principales; y explicacion de como se presentan
prioridad, confianza, errores y casos que requieren revision humana.
"""

import os

FIG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figuras")


def escribir(d):
    d.h2("Prototipar")

    d.p(
        "Prototipar consiste en construir una primera versión del producto que permita poner a "
        "prueba las hipótesis del proyecto. Para SIREC se eligió un prototipo de alta fidelidad, "
        "es decir, un producto mínimo viable funcional de extremo a extremo, y no un conjunto de "
        "bocetos estáticos. La justificación es directa: el valor de la propuesta depende de "
        "comprobar que un reporte real puede clasificarse y priorizarse en el momento en que se "
        "recibe, y eso solo puede evidenciarse con un sistema que efectivamente funcione."
    )

    d.h3("Arquitectura del prototipo")

    d.p(
        "El prototipo se organiza en cinco módulos con responsabilidades delimitadas, "
        "comunicados mediante interfaces explícitas. La figura 1 muestra esa arquitectura con las "
        "entradas y salidas rotuladas sobre cada conexión, de modo que puede seguirse el recorrido "
        "completo de un reporte desde su captura hasta su aparición en el panel de atención."
    )

    d.figura(
        "Arquitectura del prototipo de SIREC, con módulos, entradas, salidas y conexiones",
        os.path.join(FIG, "arquitectura.png"),
        ancho_cm=16.0,
    )

    d.p(
        "El recorrido comienza en el módulo 1, un formulario público donde el ciudadano describe la "
        "emergencia en texto libre, sin catálogos que elegir. El módulo 2 es la interfaz de "
        "programación desarrollada en .NET 8, que recibe el reporte, lo persiste y orquesta la "
        "clasificación. El módulo 3 es el microservicio escrito en Python con FastAPI, que expone el "
        "modelo BETO ajustado y la línea base clásica y devuelve la categoría, el nivel de urgencia y "
        "la confianza de cada predicción."
    )

    d.p(
        "El módulo 4 es la base de datos PostgreSQL, que almacena el reporte, las etiquetas "
        "asignadas, la confianza y la traza de las correcciones humanas posteriores. El módulo 5 es "
        "el panel del operador, que consulta los reportes ya ordenados por prioridad. La separación "
        "del clasificador en un servicio independiente permite sustituir el modelo sin modificar la "
        "aplicación e incorporar en el futuro otros canales de entrada. Además, todo el "
        "procesamiento ocurre en infraestructura propia, de modo que el texto del reporte no se "
        "envía a terceros: es la respuesta directa a la reticencia que las instituciones visitadas "
        "manifestaron sobre el manejo de información sensible."
    )

    d.h3("Pantallas principales")

    d.p(
        "El prototipo tiene dos pantallas, una por cada usuario identificado en la etapa de "
        "empatía. La figura 2 presenta el formulario de captura destinado al ciudadano, cuyo "
        "diseño responde al dolor más citado en la encuesta: la exigencia de responder muchas "
        "preguntas en plena emergencia. Por eso el campo principal es un área de texto libre y "
        "los demás datos son opcionales."
    )

    d.figura(
        "Formulario público de captura del reporte ciudadano",
        os.path.join(FIG, "formulario.png"),
        ancho_cm=10.0,
    )

    d.p(
        "Tras el envío, la pantalla confirma la recepción e informa de la clasificación asignada, lo "
        "que atiende parcialmente la incertidumbre sobre si el reporte fue recibido, aunque el "
        "seguimiento posterior del estatus queda fuera del alcance de esta versión. La figura 3 "
        "muestra el panel del operador, donde se materializa la aportación central del sistema."
    )

    d.figura(
        "Panel del operador con los reportes ordenados por prioridad",
        os.path.join(FIG, "panel.png"),
        ancho_cm=16.0,
    )

    d.p(
        "El panel presenta los reportes en una sola lista ordenada por urgencia y, dentro de cada "
        "nivel, por antigüedad, de modo que la lista ya expresa la decisión de qué leer primero. La "
        "tabla 6 resume las funcionalidades del prototipo, el usuario al que sirve cada una y el "
        "beneficio que obtiene."
    )

    d.tabla(
        "Funcionalidades del prototipo, usuario destinatario y beneficio",
        ["Funcionalidad", "Usuario", "Beneficio"],
        [
            ["Enviar un reporte en lenguaje natural", "Ciudadano reportante",
             "Comunicar la emergencia sin formatos rígidos ni catálogos"],
            ["Clasificar tema y urgencia al momento de la captura", "Sistema, en favor del operador",
             "Evita la lectura y el triaje manual de cada reporte"],
            ["Consultar los reportes ordenados por prioridad", "Operador de protección civil",
             "Atiende primero lo más crítico, con independencia del orden de llegada"],
            ["Consultar el detalle de un reporte", "Operador de protección civil",
             "Decide y despacha con el contexto completo del caso"],
            ["Corregir la clasificación de un reporte", "Operador de protección civil",
             "Conserva el control de la decisión y genera traza de retroalimentación"],
        ],
        anchos=[5.4, 3.6, 7.0],
    )

    d.h3("Presentación de la prioridad, la confianza y la revisión humana")

    d.p(
        "La forma en que el panel comunica sus resultados es parte del diseño, porque de ella depende "
        "que el operador pueda confiar en el sistema sin delegarle la decisión. La prioridad se "
        "comunica por triple redundancia —el orden de la lista, una etiqueta textual con el nivel y "
        "una franja de color en el costado del renglón—, lo que evita depender exclusivamente del "
        "color y favorece la accesibilidad."
    )

    d.p(
        "La confianza del modelo se muestra junto a cada predicción, en valor numérico y en una "
        "barra proporcional. Su función es permitir al operador calibrar cuánto apoyarse en la "
        "sugerencia: una clasificación con confianza alta puede aceptarse sin más, mientras que "
        "una confianza baja invita a leer el texto completo antes de decidir. Para que esta "
        "señal sea honesta, el modelo requiere un procedimiento de calibración posterior al "
        "entrenamiento, según se explicó en el fundamento teórico (Guo et al., 2017)."
    )

    d.p(
        "Cuando la confianza queda por debajo de un umbral configurable, el reporte se marca para "
        "revisión humana sin alterar su posición en la lista: solo se advierte que la sugerencia "
        "automática es débil. El mecanismo reconoce una restricción que el proyecto asume desde el "
        "principio, y es que la decisión final sobre una emergencia debe permanecer en manos de una "
        "persona."
    )

    d.p(
        "El tratamiento de los errores sigue la misma lógica de precaución. Ante un fallo del "
        "microservicio de clasificación, el reporte se guarda íntegro y se muestra en el panel sin "
        "etiquetas, marcado como pendiente de clasificar, en lugar de descartarse o de recibir "
        "una etiqueta arbitraria: perder un reporte es un riesgo inaceptable, mientras que "
        "mostrarlo sin clasificar solo devuelve al operador a su situación actual. En sentido "
        "inverso, ante la duda entre dos niveles de urgencia, la guía de etiquetado obliga a "
        "elegir el superior, criterio que se refleja también en el comportamiento del sistema."
    )

    d.p(
        "Por último, cada corrección del operador queda registrada junto con la predicción original. "
        "Esa traza permite auditar el comportamiento del modelo en operación y constituye la fuente "
        "natural de ejemplos para reentrenarlo con datos del propio contexto de uso."
    )
