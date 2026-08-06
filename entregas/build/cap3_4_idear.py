"""3.4 Idear: alternativas de solucion y criterios de valoracion."""


def escribir(d):
    d.h2("Idear")

    d.p(
        "Con la necesidad comprendida y los antecedentes revisados, la etapa de ideación "
        "consiste en abrir el abanico de soluciones posibles antes de comprometerse con una. El "
        "equipo consideró cuatro enfoques capaces, en principio, de resolver la clasificación y "
        "la priorización de reportes, y los valoró con cinco criterios: impacto o precisión "
        "esperada, viabilidad técnica, costo, esfuerzo asumible en el plazo disponible y "
        "alineación con los principios de adopción responsable de la inteligencia artificial, "
        "entendidos en el marco MELDS de Daugherty y Wilson (2018), cuyo pilar de liderazgo "
        "incorpora esa dimensión."
    )

    d.p(
        "La primera alternativa consiste en un sistema de reglas basado en diccionarios de "
        "palabras clave que asignan categoría y urgencia. Su atractivo es la simplicidad: no "
        "requiere datos etiquetados ni entrenamiento, y su comportamiento es completamente "
        "predecible. Su debilidad es justamente lo que el trabajo de campo identificó como "
        "característico del dominio, pues el lenguaje informal, las variantes de escritura y la "
        "negación desbordan cualquier lista de términos, y mantener las reglas al día se vuelve "
        "una tarea sin fin."
    )

    d.p(
        "La segunda alternativa es un modelo clásico de aprendizaje supervisado sobre "
        "representaciones TF-IDF, con regresión logística o máquinas de vectores de soporte. "
        "Ofrece un desempeño razonable con pocos recursos de cómputo, es interpretable y "
        "constituye el enfoque que la literatura hispanohablante del dominio ya ha empleado "
        "(Franco Cantos, 2024). Su limitación es la ausencia de contexto en la representación, "
        "que en este problema afecta precisamente a los casos donde la urgencia depende de la "
        "negación o del entorno de la frase."
    )

    d.p(
        "La tercera alternativa es el ajuste fino de un modelo de lenguaje preentrenado en "
        "español, concretamente BETO, para las dos tareas de clasificación. Es la opción con "
        "mayor impacto esperado, porque aporta representaciones contextuales en la lengua del "
        "corpus, y resulta viable con recursos modestos gracias a la transferencia de "
        "aprendizaje. Su costo es un mayor esfuerzo de implementación y la necesidad de "
        "infraestructura para servir el modelo, además de la exigencia de cuidar el desbalance "
        "y la calibración de la confianza."
    )

    d.p(
        "La cuarta alternativa consiste en delegar la clasificación en un servicio comercial de "
        "inteligencia artificial mediante su interfaz de programación. Reduciría "
        "drásticamente el esfuerzo de desarrollo, pero introduce tres inconvenientes decisivos: "
        "un costo por predicción que compromete la sostenibilidad de la solución en una "
        "coordinación municipal, la salida de los reportes hacia un tercero —incompatible con la "
        "preocupación por la privacidad manifestada en las visitas— y la dependencia de un "
        "proveedor externo. La tabla 5 resume la valoración de las cuatro alternativas."
    )

    d.tabla(
        "Alternativas de solución consideradas y su valoración cualitativa",
        ["N.º", "Enfoque", "Impacto esperado", "Esfuerzo", "Viabilidad"],
        [
            ["1", "Reglas por palabras clave",
             "Bajo: frágil ante el lenguaje informal", "Bajo", "Alta"],
            ["2", "Modelo clásico de línea base (TF-IDF con regresión logística y SVM)",
             "Medio", "Medio", "Alta"],
            ["3", "Transformador en español: ajuste fino de BETO",
             "Alto", "Alto", "Media-alta"],
            ["4", "Servicio de pago administrado de un tercero",
             "Medio-alto", "Bajo", "Baja: costo, dependencia y salida de datos"],
        ],
        anchos=[1.0, 5.6, 3.4, 1.8, 4.2],
    )

    d.p(
        "La lectura de la tabla 5 conduce a una decisión combinada. La alternativa 4 se descarta "
        "porque incumple el principio de trabajar con herramientas abiertas y sin costo por uso, y "
        "porque reduciría la aportación académica a integrar un servicio ajeno; la alternativa 1 "
        "resulta insuficiente por sí sola, aunque conserva utilidad como modo de arranque. Las "
        "alternativas 2 y 3 no compiten sino que se complementan: el modelo clásico se adopta como "
        "línea base obligatoria, porque sin punto de comparación no puede afirmarse que el modelo "
        "neuronal aporte algo, y BETO ajustado como clasificador principal por su mayor impacto "
        "esperado en español."
    )
