"""3.6 Seleccion de prototipo.

Atiende C12: la matriz se rotula y se explica; se declaran criterios, pesos,
escala, quien realizo la valoracion y con que evidencia se asignaron los valores.
"""


def escribir(d):
    d.h2("Selección de prototipo")

    d.p(
        "La selección de prototipo justifica, mediante una matriz de criterios ponderados, cuál "
        "de las alternativas conviene desarrollar y validar. Antes de presentar los resultados es "
        "necesario declarar cómo se construyó la matriz, porque de ello depende que sus "
        "conclusiones sean interpretables: qué criterios se emplearon y con qué peso, qué escala "
        "se aplicó, quién asignó las puntuaciones y sobre qué evidencia."
    )

    d.p(
        "Los cinco criterios provienen de las restricciones documentadas en las etapas "
        "anteriores. El impacto o precisión esperada recibe el mayor peso, 30 %, porque el valor "
        "del sistema depende de que la clasificación sea correcta, en particular en las clases "
        "críticas. La viabilidad técnica y el costo reciben 20 % cada uno: la primera porque una "
        "solución inviable en el plazo disponible no es una solución, y el segundo porque el "
        "destinatario es una coordinación municipal con presupuesto acotado. La adopción "
        "responsable de la inteligencia artificial y el esfuerzo asumible reciben 15 % cada uno."
    )

    d.p(
        "La escala de valoración va de 1 a 5, donde 1 es la condición menos favorable. En el criterio "
        "de costo un valor alto significa menor costo, de modo que todos los criterios se leen en el "
        "mismo sentido; el puntaje final es la suma de las valoraciones multiplicadas por el peso de "
        "cada criterio."
    )

    d.p(
        "Las puntuaciones fueron asignadas por consenso entre los tres integrantes del equipo en "
        "una sesión dedicada a ello: cada integrante propuso un valor y, cuando la discrepancia "
        "superó un punto, se discutió hasta acordar una cifra única. La evidencia que las respaldó "
        "fue de tres tipos: el trabajo de campo y la encuesta para el impacto esperado, la revisión "
        "de antecedentes del apartado 3.3 para la precisión atribuible a cada enfoque, y las "
        "condiciones reales del proyecto —infraestructura, plazo y ausencia de presupuesto— para "
        "viabilidad, costo y esfuerzo. La tabla 7 presenta el resultado."
    )

    d.tabla(
        "Matriz de selección ponderada de las alternativas de solución",
        ["Criterio (peso)", "1. Reglas por palabras clave", "2. Línea base clásica",
         "3. MVP funcional con BETO", "4. Servicio de pago"],
        [
            ["Impacto y precisión esperada (30 %)", "2", "3", "5", "4"],
            ["Viabilidad técnica (20 %)", "5", "5", "4", "3"],
            ["Costo, donde mayor es mejor (20 %)", "5", "5", "4", "1"],
            ["Adopción responsable de la IA (15 %)", "3", "4", "5", "2"],
            ["Esfuerzo asumible en el plazo (15 %)", "5", "4", "3", "4"],
            ["Puntaje ponderado", "3.65", "4.05", "4.40", "2.90"],
        ],
        fuente="Elaboración propia; escala de 1 (menos favorable) a 5 (más favorable), "
               "valorada por consenso de los tres integrantes del equipo.",
        anchos=[5.4, 2.7, 2.6, 2.9, 2.4],
    )

    d.p(
        "La tabla 7 confirma la decisión anticipada en el apartado anterior. El producto mínimo "
        "viable con BETO obtiene el puntaje más alto, 4.40, porque compensa su mayor esfuerzo de "
        "implementación con la mejor valoración en los dos criterios de mayor peso combinado: el "
        "impacto esperado y la adopción responsable, esta última favorecida por ejecutarse en "
        "infraestructura propia y sin envío de datos a terceros. La línea base clásica queda en "
        "segundo lugar con 4.05, resultado coherente con su papel en el proyecto."
    )

    d.p(
        "El servicio de pago obtiene el puntaje más bajo, 2.90, penalizado por el costo por "
        "predicción y la dependencia externa, y las reglas por palabras clave alcanzan 3.65 gracias a "
        "su viabilidad y costo nulo, aunque su impacto insuficiente las descarta como solución "
        "principal. Conviene reconocer que estas valoraciones son juicios expertos del equipo y no "
        "mediciones: su función es hacer explícito y discutible el razonamiento de la decisión."
    )

    d.p(
        "En consecuencia, se selecciona el producto mínimo viable web con BETO como modelo principal, "
        "servido por el microservicio de clasificación, acompañado de la línea base clásica como "
        "referencia obligatoria y con un panel del operador ordenado por urgencia. La comprobación "
        "empírica de esta elección corresponde a la evaluación que se describe a continuación."
    )
