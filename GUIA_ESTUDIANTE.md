# Guía para estudiantes — Replicar SIREC desde cero, paso a paso

> **Para quién es esto:** para alguien de **primer semestre** que nunca ha tocado inteligencia
> artificial. No necesitas saber nada previo. Vamos a construir juntos, desde cero, un sistema que
> lee reportes de emergencia y decide **de qué son** y **qué tan urgentes** son.
>
> **Cómo leer esta guía:** cada vez que aparece un concepto de IA lo marcamos con un número, así:
> aprendizaje automático <sup>[[2]](#c2)</sup>. Ese número te lleva al **[Diccionario de conceptos](#diccionario-de-conceptos-de-ia-usados)**
> al final, donde está explicado en una frase. Al terminar verás la **lista completa de conceptos**
> que usamos: todos aparecen numerados, para que compruebes que ninguno se quedó fuera.

---

## Antes de empezar: ¿qué problema resolvemos?

Durante una tormenta, la oficina de Protección Civil recibe **cientos de mensajes** de ciudadanos al
mismo tiempo. Alguien tiene que leerlos uno por uno para decidir cuál es más urgente. Eso es lento, y
en una emergencia cada minuto cuenta.

Queremos que una **inteligencia artificial** <sup>[[1]](#c1)</sup> lea cada mensaje y le ponga dos
etiquetas automáticamente: su **categoría** (inundación, incendio, persona en riesgo, etc.) y su
**urgencia** (alta, media, baja). A eso se le llama **clasificación** <sup>[[4]](#c4)</sup>, y como
trabajamos con texto escrito por personas, entra en el campo del **procesamiento de lenguaje natural
(PLN)** <sup>[[3]](#c3)</sup>.

La idea central: en lugar de escribir a mano miles de reglas ("si dice *agua* entonces es
inundación"), le mostramos al programa **muchos ejemplos ya resueltos** y dejamos que **aprenda solo**
los patrones. Eso es el **aprendizaje automático** <sup>[[2]](#c2)</sup>.

**Lo que vas a necesitar instalar** (todo gratis):
- **Python 3.11 o superior** (usamos 3.13).
- **Git** (para descargar el proyecto).
- Una cuenta de **Google** (para usar Google Colab, que nos presta una computadora potente gratis).

```bash
git clone https://github.com/alexisherrera22/sirec.git
cd sirec/datos-modelo
```

---

## Paso 1 — Conseguir los ejemplos (el corpus)

Un modelo de IA aprende de ejemplos. Al conjunto de todos los textos de ejemplo se le llama
**corpus** <sup>[[5]](#c5)</sup>. **¿Por qué?** Porque sin ejemplos, no hay de dónde aprender: es
como pedirle a alguien que reconozca perros sin haberle mostrado nunca un perro.

En SIREC juntamos **400 reportes reales** de emergencias (de redes sociales y prensa). Un paso
obligatorio antes de guardarlos es la **anonimización** <sup>[[8]](#c8)</sup>: quitar nombres,
teléfonos y direcciones. **¿Por qué?** Por ética y privacidad — nunca debemos exponer datos
personales de la gente.

Luego, un humano lee cada reporte y le pone su categoría y urgencia correctas. A eso se le llama
**etiquetar** <sup>[[7]](#c7)</sup>, y a la persona que lo hace, **anotador** <sup>[[10]](#c10)</sup>.
Estas etiquetas son la "respuesta correcta" de la que el modelo aprenderá.

> **Problema real:** conseguir reportes reales es difícil y lento. Para tener más ejemplos de
> práctica, generamos **900 reportes sintéticos** <sup>[[9]](#c9)</sup> (inventados por nosotros,
> declarados como tales). **Regla de oro:** los sintéticos **solo sirven para entrenar, nunca para
> calificar** al modelo. Calificar con datos inventados daría notas falsas.

Archivos: `corpus_etiquetado.csv` (400 reales) y `corpus_sintetico.csv` (900 sintéticos).

---

## Paso 2 — Comprobar que las etiquetas son confiables (kappa)

Aquí hay una trampa sutil: si **una sola persona** etiqueta todo, ¿cómo sabemos que sus etiquetas son
objetivas y no su opinión personal? Para demostrarlo, **dos anotadores** etiquetan **los mismos 180
reportes por separado, sin verse**, y medimos qué tanto coinciden con un número llamado
**kappa de Cohen** <sup>[[11]](#c11)</sup>.

**¿Por qué es importante?** Porque si dos personas coinciden mucho, las etiquetas son objetivas
(cualquiera llegaría a lo mismo). Si coinciden poco, las etiquetas son subjetivas y poco confiables.

```bash
py calcular_kappa.py --entrada kappa_ricardo.csv kappa_nahum.csv
```

Nuestro resultado: **categoría κ = 0.70** (buen acuerdo) y **urgencia κ = 0.31** (acuerdo bajo — la
urgencia es más difícil de juzgar). Como la urgencia salió baja, una **tercera persona** resolvió los
desacuerdos uno por uno; a eso se le llama **adjudicación** <sup>[[12]](#c12)</sup>.

```bash
py generar_adjudicacion.py      # arma la lista de desacuerdos a resolver
py consolidar_adjudicacion.py   # con las decisiones, crea el conjunto final
```

El resultado son **180 reportes con etiqueta de consenso**, la máxima calidad posible. A ese conjunto
lo llamamos **gold** ("de oro") <sup>[[13]](#c13)</sup>: `gold_kappa.csv`.

---

## Paso 3 — Separar datos de entrenamiento y de prueba (¡sin hacer trampa!)

Antes de entrenar, dividimos los datos en dos montones que **nunca se mezclan**:

- **Entrenamiento:** los ejemplos con los que el modelo aprende (220 reales + 900 sintéticos).
- **Prueba:** ejemplos que el modelo **nunca ve durante el aprendizaje** (los 180 gold), y que
  usamos solo para calificarlo. Esta separación es el concepto de **datos de entrenamiento vs.
  prueba** <sup>[[6]](#c6)</sup>.

**¿Por qué separarlos?** Imagina un examen donde el profesor te da exactamente las mismas preguntas
que estudiaste: sacarías 10, pero no probaría que aprendiste. Evaluar con datos nuevos es la única
forma honesta de medir si el modelo **generaliza** a casos que no había visto.

Un detalle: algunas categorías (como `dano_estructural`) casi no aparecen. Ese **desbalance de
clases** <sup>[[14]](#c14)</sup> dificulta el aprendizaje, y lo compensamos más adelante con un
truco llamado **pesos por clase** <sup>[[21]](#c21)</sup>.

---

## Paso 4 — Entrenar el modelo simple primero (el baseline)

**Regla de oro de la ciencia de datos:** empieza por lo más simple. Ese modelo simple se llama
**baseline** o "línea base" <sup>[[17]](#c17)</sup>. **¿Por qué?** Porque es tu punto de comparación:
si después un modelo complicado no le gana al baseline, la complejidad no valió la pena.

Como las computadoras no entienden palabras, primero convertimos cada texto en una lista de números
llamada **vector** <sup>[[15]](#c15)</sup>. La técnica que usamos para eso es **TF-IDF**
<sup>[[16]](#c16)</sup>, que básicamente cuenta qué palabras aparecen y qué tan distintivas son (no
entiende el significado, solo cuenta).

Con esos vectores, entrenamos un **clasificador lineal** <sup>[[18]](#c18)</sup>: un algoritmo que
separa las categorías trazando líneas. Probamos dos clásicos:
- **SVM — Máquina de Vectores de Soporte** <sup>[[19]](#c19)</sup>: traza la frontera que mejor separa
  los grupos dejando el mayor margen posible.
- **Regresión logística** <sup>[[20]](#c20)</sup>: estima la probabilidad de que un texto sea de cada
  categoría.

```bash
py entrenar_baseline.py --gold-test --con-sintetico
```

Esto entrena con los 220 reales + 900 sintéticos y **califica contra los 180 gold**. Resultado:
categoría macro-F1 **0.65**, urgencia macro-F1 **0.45** (ya veremos qué significan esos números en el
Paso 6).

---

## Paso 5 — Entrenar el modelo avanzado (BETO)

El baseline solo cuenta palabras; no entiende que *"no responde"* o *"sigue subiendo"* implican
gravedad. Para eso usamos una **red neuronal** <sup>[[22]](#c22)</sup>, un modelo inspirado en el
cerebro capaz de captar patrones complejos.

En concreto usamos un tipo moderno de red neuronal llamado **transformer** <sup>[[23]](#c23)</sup>
(la misma familia que ChatGPT). Un transformer entrenado para entender texto se llama **BERT**
<sup>[[24]](#c24)</sup>, y la versión de BERT **entrenada en español** se llama **BETO**
<sup>[[25]](#c25)</sup>. Ese es nuestro modelo principal.

BETO ya "sabe español" en general. Nosotros lo **especializamos** en clasificar emergencias
mostrándole nuestros ejemplos; a ese paso se le llama **fine-tuning** o ajuste fino
<sup>[[26]](#c26)</sup>. **¿Por qué no entrenar desde cero?** Porque sería carísimo y lento;
aprovechar lo que BETO ya sabe es mucho más eficiente.

Entrenar una red neuronal necesita una **GPU** <sup>[[27]](#c27)</sup> (un procesador muy rápido).
Como no teníamos, usamos **Google Colab**, que presta GPUs gratis. Todo está en el cuaderno
`entrenar_beto_colab.ipynb`:

1. Súbelo a [Google Colab](https://colab.research.google.com).
2. Activa la GPU: *Entorno de ejecución → Cambiar tipo de entorno → GPU*.
3. Ejecuta las celdas y sube los 3 archivos de datos cuando te lo pida.

Durante el entrenamiento ajustamos algunos **hiperparámetros** <sup>[[29]](#c29)</sup> (opciones que
controlan cómo aprende): entrenamos por 4 **épocas** <sup>[[28]](#c28)</sup> (4 pasadas completas por
los datos) y usamos **pesos por clase** <sup>[[21]](#c21)</sup> para las categorías raras.

Resultado: categoría macro-F1 **0.74**, urgencia macro-F1 **0.55**.

---

## Paso 6 — Comparar los dos modelos (¿cuál es mejor y por qué?)

Ahora la pregunta clave: **¿BETO le gana al baseline?** Para responderlo con seriedad, medimos a
ambos con las mismas reglas sobre el mismo conjunto gold. Estas son las medidas:

- **Precisión** <sup>[[30]](#c30)</sup>: de lo que el modelo dijo "es X", ¿cuánto era realmente X?
- **Recall** <sup>[[31]](#c31)</sup>: de todo lo que de verdad era X, ¿cuánto detectó el modelo?
- **Falso negativo** <sup>[[32]](#c32)</sup>: un caso real que el modelo **NO detectó**. En
  emergencias es el peor error (no detectar una "persona en riesgo").
- **F1 / Macro-F1** <sup>[[33]](#c33)</sup>: un número que resume precisión y recall; el macro-F1 lo
  promedia entre todas las categorías.

**¿Por qué nos importa más el recall?** Porque en una emergencia es mucho peor **no detectar** un
caso grave (que alguien no reciba ayuda) que dar una falsa alarma.

| Medida | Baseline | BETO | ¿Quién gana? |
|---|---:|---:|:---:|
| Categoría — Macro-F1 | 0.65 | **0.74** | BETO |
| Categoría — Recall "persona en riesgo" | 0.58 | **0.87** | BETO |
| Urgencia — Macro-F1 | 0.45 | **0.55** | BETO |
| Urgencia — Recall "alta" | 0.58 | **0.77** | BETO |

**Conclusión:** BETO gana en todo, sobre todo en el recall de las clases críticas. Se confirma la
hipótesis: el transformer entiende la gravedad que el modelo simple no ve. La comparación completa
está en `datos-modelo/comparacion_modelos.md`.

---

## Paso 7 — Poner el modelo a funcionar

Un modelo entrenado no sirve de nada si nadie lo puede usar. El paso de **usar el modelo ya entrenado
para responder casos nuevos** se llama **inferencia**, y ponerlo disponible se llama **despliegue**
<sup>[[34]](#c34)</sup>.

Lo metimos dentro de un **microservicio** (un programa pequeño con una "ventanilla" de red):

```bash
cd ../microservicio-ml
py -m pip install torch transformers fastapi "uvicorn[standard]"
# (copia los modelos entrenados en la carpeta modelos/ — ver DESPLIEGUE_MODELO.md)
$env:SIREC_MODO = "modelo"     # en Windows PowerShell
py -m uvicorn main:app --port 8000
```

Y ya puedes mandarle un reporte y ver la respuesta de BETO en tiempo real.

---

## Resumen: el orden completo, de principio a fin

1. **Conseguir ejemplos** (corpus real + sintético) y etiquetarlos. → Paso 1
2. **Verificar** que las etiquetas son confiables (kappa + adjudicación → gold). → Paso 2
3. **Separar** entrenamiento y prueba, sin mezclar. → Paso 3
4. **Entrenar el baseline** (modelo simple, punto de comparación). → Paso 4
5. **Entrenar BETO** (modelo avanzado) en Colab. → Paso 5
6. **Comparar** ambos con métricas justas. → Paso 6
7. **Desplegar** el ganador para usarlo. → Paso 7

---

## Diccionario de conceptos de IA usados

Cada concepto que apareció numerado arriba, explicado en una frase. **Todos se usaron en el proyecto.**

<a id="c1"></a>**1. Inteligencia Artificial (IA):** programas que aprenden a hacer una tarea a partir de ejemplos, en lugar de seguir reglas escritas a mano.

<a id="c2"></a>**2. Aprendizaje automático (machine learning):** la técnica de "enseñar" a un programa mostrándole ejemplos ya resueltos para que descubra los patrones solo.

<a id="c3"></a>**3. Procesamiento de Lenguaje Natural (PLN):** la rama de la IA que hace que una computadora entienda y procese texto escrito por humanos.

<a id="c4"></a>**4. Clasificación:** la tarea de poner una etiqueta a algo (aquí: la categoría y la urgencia de un reporte).

<a id="c5"></a>**5. Corpus:** el conjunto completo de textos de ejemplo con los que se entrena y evalúa el modelo.

<a id="c6"></a>**6. Datos de entrenamiento vs. prueba:** dos montones separados de ejemplos; con uno el modelo aprende, con el otro (que no vio) se le califica de forma honesta.

<a id="c7"></a>**7. Etiquetar:** asignar a mano la respuesta correcta (categoría y urgencia) a cada ejemplo.

<a id="c8"></a>**8. Anonimización:** quitar los datos personales (nombres, teléfonos, direcciones) de los textos antes de usarlos.

<a id="c9"></a>**9. Datos sintéticos:** ejemplos generados artificialmente para tener más material de práctica. Solo se usan para entrenar, nunca para evaluar.

<a id="c10"></a>**10. Anotador:** la persona que etiqueta los ejemplos.

<a id="c11"></a>**11. Kappa de Cohen:** un número de 0 a 1 que mide cuánto coinciden dos anotadores etiquetando lo mismo por separado; demuestra que las etiquetas son objetivas.

<a id="c12"></a>**12. Adjudicación:** cuando dos anotadores discrepan, una tercera persona decide la etiqueta final de consenso.

<a id="c13"></a>**13. Conjunto gold ("de oro"):** los ejemplos con etiqueta de máxima confianza (doble etiquetado + adjudicación); se usan como conjunto de prueba.

<a id="c14"></a>**14. Desbalance de clases:** cuando unas categorías tienen muchos más ejemplos que otras, lo que dificulta aprender las raras.

<a id="c15"></a>**15. Vector / vectorización:** convertir un texto en una lista de números, porque las computadoras operan con números, no con palabras.

<a id="c16"></a>**16. TF-IDF:** una técnica clásica para vectorizar texto contando qué palabras aparecen y qué tan distintivas son. No entiende el significado.

<a id="c17"></a>**17. Baseline (línea base):** un modelo sencillo que sirve de punto de comparación; si el modelo avanzado no le gana, no valió la pena la complejidad.

<a id="c18"></a>**18. Clasificador lineal:** un algoritmo que separa las categorías trazando líneas rectas entre los ejemplos representados como vectores.

<a id="c19"></a>**19. SVM (Máquina de Vectores de Soporte):** un clasificador lineal que traza la frontera que mejor separa los grupos, dejando el mayor margen posible.

<a id="c20"></a>**20. Regresión logística:** un clasificador lineal que estima la probabilidad de que un ejemplo pertenezca a cada clase.

<a id="c21"></a>**21. Pesos por clase (class weights):** un ajuste para que el modelo preste más atención a las categorías raras y compense el desbalance.

<a id="c22"></a>**22. Red neuronal:** un modelo inspirado (a grandes rasgos) en el cerebro, capaz de aprender patrones complejos. Es la base de la IA moderna.

<a id="c23"></a>**23. Transformer:** un tipo moderno de red neuronal, base de los modelos de lenguaje actuales; capta el contexto y el significado de las palabras.

<a id="c24"></a>**24. BERT:** un transformer diseñado para comprender texto; entiende frases por su contexto, no solo por las palabras sueltas.

<a id="c25"></a>**25. BETO:** un BERT entrenado específicamente en español (`dccuchile/bert-base-spanish-wwm-cased`). Es nuestro modelo principal.

<a id="c26"></a>**26. Fine-tuning (ajuste fino):** tomar un modelo ya entrenado (BETO) y especializarlo en nuestra tarea con nuestros ejemplos, en vez de entrenar desde cero.

<a id="c27"></a>**27. GPU:** un procesador muy rápido, necesario para entrenar redes neuronales. Usamos Google Colab, que las presta gratis.

<a id="c28"></a>**28. Época (epoch):** una pasada completa del modelo por todos los datos de entrenamiento. Entrenamos por 4 épocas.

<a id="c29"></a>**29. Hiperparámetros:** las opciones que controlan cómo aprende el modelo (número de épocas, velocidad de aprendizaje, etc.).

<a id="c30"></a>**30. Precisión:** de todo lo que el modelo dijo "es X", el porcentaje que realmente era X (mide las falsas alarmas).

<a id="c31"></a>**31. Recall:** de todo lo que de verdad era X, el porcentaje que el modelo detectó (mide lo que se le escapa).

<a id="c32"></a>**32. Falso negativo:** un caso real que el modelo no detectó. En emergencias es el error más grave.

<a id="c33"></a>**33. F1 / Macro-F1:** el F1 combina precisión y recall en un número; el macro-F1 lo promedia entre todas las categorías por igual.

<a id="c34"></a>**34. Inferencia y despliegue:** inferencia es usar el modelo ya entrenado para responder casos nuevos; despliegue es ponerlo disponible para que otros lo usen.

---

> ¿Quieres el panorama completo del sistema (arquitectura, conexiones, despliegue en AWS)? Está en el
> [`README.md`](README.md) principal.
