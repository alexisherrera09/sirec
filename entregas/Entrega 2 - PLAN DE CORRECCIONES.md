# Plan de trabajo — Entrega 2 de SIREC: corrección total según la retroalimentación del profesor

**Fecha:** 2026-08-06
**Documento a corregir:** `/home/ubuntu/proyectos/sirec/entregas/Entrega 2 - SIREC (Desarrollo conceptual Design Thinking).docx`
**Retroalimentación que se atiende:** `/home/ubuntu/proyectos/sirec/entregas/Entrega 2 comentarios.txt` (Efrén Juárez)
**Alcance de este archivo:** solo el plan. No se ejecuta nada hasta que Alexis lo autorice.

---

## 0. Nota previa sobre la numeración de las entregas

El correo del profesor abre con «he revisado su **Entrega 1**», pero el contenido que
comenta es inequívocamente el de **nuestra Entrega 2**: habla del capítulo 2 de objetivos
y de «3.1 Empatizar, 3.2 Definir, 3.3 Investigación de antecedentes, 3.4 Idear, 3.5
Prototipar», que es exactamente el índice del `.docx` que entregamos. Él numera distinto
porque para su registro la propuesta inicial (`Entrega 1.pdf`) no cuenta como entregable
documental. **Todo lo que sigue aplica al documento de Design Thinking.**

Consecuencia práctica: cuando menciona «el rango de 20 a 30 páginas establecido para la
Entrega 1», ese rango es el que debe cumplir **este** documento.

---

## 1. Punto de partida, medido

No es una impresión, son los números reales del `.docx` de hoy:

| Métrica | Hoy | Lo que exige el profesor |
|---|---|---|
| Palabras de cuerpo | **4 544** | 20–30 págs de desarrollo sustantivo (≈ 7 000–11 000 palabras) |
| Páginas de desarrollo | **≈ 9** (él dijo «aproximadamente diez») | 20–30 |
| Tablas | 9 | 9, pero **todas rotuladas y explicadas** |
| Rótulos «Tabla N. Título» | **0 en todo el documento** | uno por tabla, consecutivos |
| Figuras propias | **0** | al menos 1 de arquitectura + wireframes |
| Viñetas / listas numeradas | **37 + 15 = 52 párrafos** | prosa académica; viñetas solo donde sea justificable |
| Saltos de página | **2** (para 5 capítulos + anexo) | cada capítulo y los anexos en página nueva |
| Índice | **no existe** | índice con numeración jerárquica igual a la del cuerpo |
| Párrafos de ≥ 120 palabras (~9+ renglones) | **3** | 5–8 renglones; dividir arriba de 10–12 |
| Encabezados de 3.er nivel numerados | **0 de 9** (p. ej. «Perfiles de usuario» sin número) | numeración jerárquica completa |
| Referencias | **7** | «aumenten la cantidad» → meta 20–25 |
| Plantilla | Calibri, hoja Letter, márgenes 1.25″/1″, sin interlineado definido, **sin portada de plantilla** | todo el formato de `plantilla.docx` |
| Sigla en el título | «SIREC: clasificación y priorización…» | nombre completo primero, sigla definida en su 1.ª aparición |

El diagnóstico coincide punto por punto con lo que él escribió, así que no hay nada que
discutirle: los 13 señalamientos son verificables en el archivo.

---

## 2. Trazabilidad: cada señalamiento → dónde se resuelve

| # | Señalamiento del profesor | Dónde se atiende | Fase |
|---|---|---|---|
| C1 | Usar `plantilla.docx`: portada, estilos, tipografía, márgenes, interlineado, encabezados, pies, diseño de tablas | Todo el documento | F1 |
| C2 | El título con «SIREC» no se entiende; definir la sigla | Portada + 1.ª aparición en 1.1 | F1 |
| C3 | Solo ~10 págs; ampliar con **análisis**, no relleno (intro, fundamento teórico, estado del arte, prototipo) | 1, 3.3.1, 3.3.2, 3.5 | F3, F4 |
| C4 | Párrafos de 5–8 renglones; dividir los de 10–12+ | 3 párrafos detectados + los nuevos | F2 |
| C5 | Nunca un título pegado a otro sin texto; cada capítulo en página nueva; anexos igual y con el mismo estilo | Caps. 1, 2 y Anexo A | F1, F2 |
| C6 | Numeración jerárquica de temas y subtemas, igual en índice y cuerpo (2.1/2.2, 3.1–3.6) | Todos los encabezados + índice | F1 |
| C7 | Introducción de mínimo 2 págs en prosa, con contexto, problema, justificación, propósito, alcance y estructura, **con citas de estadísticas oficiales** sobre Veracruz | Cap. 1 | F3 |
| C8 | Objetivo general: qué se desarrolla, con qué IA, qué resultado y **cómo se mide**; específicos que conduzcan a él | Cap. 2 | F2 |
| C9 | Fundamento teórico: 3–5 págs de prosa con citas (representación de texto, TF-IDF, regresión logística, SVM, multiclase, Transformers, BERT, BETO, tokenización, ajuste fino, desbalance, calibración, métricas, acuerdo entre evaluadores) | 3.3.1 | F3 |
| C10 | Estado del arte: 3–4 págs; por trabajo: problema, contexto, idioma, dataset, tamaño, etiquetado, herramientas, modelos, métricas, resultados, limitaciones y relación con SIREC; tabla al final como síntesis; cerrar con brecha | 3.3.2 | F3 |
| C11 | Abuso de tablas y viñetas; toda tabla con «Tabla N. Título», fuente/nota, numeración consecutiva, llamada desde el texto e interpretación; corregir la secuencia | Las 9 tablas | F2, F6 |
| C12 | Tablas con el diseño de la plantilla; la matriz de selección debe explicar criterios, pesos, puntuaciones, **quién valoró y con qué evidencia** | 3.6 + estilo global | F1, F6 |
| C13 | Prototipo demasiado abstracto: figura propia con formulario, API, clasificador, BD y panel, con entradas/salidas/conexiones; wireframes; cómo se presentan prioridad, confianza, errores y revisión humana | 3.5 | F4 |
| C14 | Evaluación: baseline TF-IDF vs BETO, mismos datos y particiones reproducibles, precision/recall/F1 por clase y macro, matriz de confusión, falsos negativos críticos, kappa, tiempo de respuesta y **criterios mínimos de éxito** | **3.7 nueva** | F5 |
| C15 | Referencias insuficientes; toda cita con entrada y toda entrada citada | Referencias + cuerpo | F7 |

### 2.1 Verificación de cobertura: los 13 párrafos del correo, en su orden

El correo del profesor tiene 29 líneas: **13 párrafos con acción** más el elogio inicial y la
despedida. Ningún señalamiento quedó fuera (dos párrafos traen dos cada uno, de ahí que 13
párrafos den 15 puntos). No hay otra fuente de retroalimentación: el `.docx` no tiene
comentarios de Word (`comments.xml` no existe) y el PDF de la Entrega 2 tiene 0 anotaciones.

| Párrafo (línea del `.txt`) | Frase que lo define | Punto | Fase |
|---|---|---|---|
| 1 (L1) | «El problema del triaje manual […] es pertinente» | elogio, sin acción | — |
| 2 (L3) | «El primer aspecto que deben corregir es el uso de plantilla.docx» + «la sigla SIREC no se entiende por sí sola» | C1, C2 | F1 |
| 3 (L5) | «ocupa aproximadamente diez páginas y queda muy por debajo del rango de 20 a 30» + «cada párrafo tenga entre cinco y ocho renglones» | C3, C4 | F3, F2 |
| 4 (L7) | «No debe colocarse un título inmediatamente después de otro» + «cada capítulo debe comenzar en una página nueva» | C5 | F1, F2 |
| 5 (L9) | «numerar jerárquicamente los temas y subtemas […] La misma numeración debe aparecer en el índice» | C6 | F1 |
| 6 (L11) | «La introducción debe tener un mínimo de dos páginas» + «deben sustentarse con estadísticas oficiales» | C7 | F3 |
| 7 (L13) | «El objetivo general debe indicar […] qué resultado se espera y cómo se medirá» | C8 | F2 |
| 8 (L15) | «El fundamento teórico es demasiado breve […] de aproximadamente tres a cinco páginas, sustentada con citas» | C9 | F3 |
| 9 (L17) | «El estado del arte también es muy básico […] tres o cuatro páginas de prosa académica» | C10 | F3 |
| 10 (L19) | «abusa de tablas y viñetas» + «La tabla de la página 9 no está numerada ni titulada» | C11 | F2, F6 |
| 11 (L21) | «Las tablas tampoco utilizan el diseño establecido en plantilla.docx» + «La matriz de selección […] debe rotularse y explicarse» | C12 | F1, F6 |
| 12 (L23) | «El prototipo todavía es demasiado abstracto […] Incluyan una figura propia» | C13 | F4 |
| 13 (L25) | «La evaluación debe comparar el baseline de TF-IDF y modelos clásicos con BETO utilizando el mismo conjunto de datos y particiones reproducibles. Definan métricas como precision, recall y F1 por clase y macro, matriz de confusión, falsos negativos en categorías críticas, acuerdo de etiquetado, tiempo de respuesta y criterios mínimos de éxito.» | **C14** | **F5** |
| 14 (L27) | «Las referencias incluidas son pertinentes, pero resultan insuficientes» | C15 | F7 |

---

## 3. Decisiones que necesito del equipo antes de arrancar

Tres son bloqueantes de verdad; las demás las puedo resolver yo con criterio si nadie opina.

1. **`plantilla.docx` (bloqueante de F1).** No está en la máquina; la busqué en todo
   `/home/ubuntu`. Hay que bajarla del aula virtual de UNIR y dejarla en
   `entregas/plantilla.docx`. Sin ella, F1 no se puede hacer y F2–F7 se harían sobre un
   formato que luego habría que rehacer.
   *Plan B si tarda:* escribir el contenido en el `.docx` actual usando **solo estilos
   nombrados** (Título 1/2/3, Normal, Tabla), de modo que el volcado posterior sea un
   mapeo de estilos y no una reescritura. Cuesta una sesión extra y es el riesgo que
   quiero evitar.

2. **Dónde va la evaluación (C14).** El profesor la exige en este documento, pero
   nuestro alcance acordado eran los capítulos 1–3. **Recomiendo** una sección nueva
   **3.7 «Diseño de la evaluación del prototipo»** dentro del capítulo 3: cumple lo que
   pide sin invadir el capítulo 6 de la memoria final (allí irán los resultados, aquí el
   diseño y los criterios de éxito).

3. **Anexo A.** El README decía que los anexos no iban en esta entrega, pero el profesor
   ya los dio por presentes («los anexos también deben comenzar en una página nueva y
   conservar el mismo estilo»). **Recomiendo conservarlo** y darle el formato que pide.

4. **Estadísticas oficiales de Veracruz (C7).** Las afirmaciones de 1.1 —«uno de los
   territorios con mayor número de declaratorias»— hoy no tienen fuente. Hay que
   sustentarlas con CENAPRED, CONAGUA/SMN, INEGI o el SESNSP (llamadas al 911), o
   suavizarlas. **No se inventa ni un dato ni una cita** (regla del proyecto).

5. **Capturas reales del sistema (C13).** SIREC ya está desplegado en la EC2, así que
   además del diagrama podemos poner capturas reales del formulario y del panel. Es la
   forma más barata de matar el «prototipo demasiado abstracto». Confirmar que el equipo
   quiere mostrarlo ahora y no reservarlo para la defensa.

---

## 4. Presupuesto de páginas (para que la ampliación no sea relleno)

Supuesto: plantilla UNIR con fuente 11–12 pt e interlineado 1.5 → **≈ 350–400 palabras
por página**. La cuenta final se verifica sobre la plantilla real, no sobre este supuesto.

| Sección | Palabras hoy (aprox.) | Meta | Páginas meta | Trabajo principal |
|---|---|---|---|---|
| 1. Introducción | 700 | 1 050 | 3 | Prosa + citas + justificación explícita |
| 2. Objetivos | 450 | 500 | 1.5 | Párrafo de entrada + medibilidad del general |
| 3. Entrada del cap. 3 | 120 | 200 | 0.5 | — |
| 3.1 Empatizar | 1 200 | 1 400 | 4 | 7 viñetas de hallazgos → prosa; interpretar tablas |
| 3.2 Definir | 700 | 900 | 2.5 | HMW en prosa; partir 2 párrafos largos |
| 3.3.1 Fundamento teórico | 350 (viñetas) | **1 600** | 4.5 | **El bloque más grande: +1 250 palabras** |
| 3.3.2 Estado del arte | 300 | **1 350** | 4 | De 3 a 6–8 trabajos con ficha completa |
| 3.4 Idear | 350 | 600 | 1.5 | Prosa por alternativa |
| 3.5 Prototipar | 300 | 900 | 2.5 | + 3 figuras y su explicación |
| 3.6 Selección | 250 | 500 | 1.5 | Pesos, valoradores, evidencia |
| **3.7 Evaluación (nueva)** | 0 | **1 000** | 3 | Diseño experimental y criterios de éxito |
| **Total desarrollo** | **≈ 4 700** | **≈ 10 000** | **≈ 28** | dentro del rango 20–30 |
| Referencias | 7 entradas | 20–25 | 2 | no cuentan como desarrollo |
| Portada + índice + Anexo A | — | — | 4 | no cuentan como desarrollo |

El delta es **+5 300 palabras**, y más de la mitad se concentra en dos secciones
(fundamento teórico y estado del arte), que son justo las dos que él marcó como
«demasiado breves». Eso es análisis, no relleno.

---

## 5. Fases de trabajo

### F0 — Insumos y verificación previa (bloqueante)
- Conseguir `plantilla.docx` y colocarla en `entregas/`.
- Recolectar y **verificar** las fuentes estadísticas del punto 3.4 (guardar liga y dato exacto).
- Decidir los 5 puntos de la sección 3.
- Tomar las capturas del sistema desplegado (formulario + panel) si se aprueban.
- Comprobar con qué se generan las figuras: en el venv solo hay `python-docx`; no hay
  matplotlib, graphviz, pandoc ni LibreOffice. Opciones: instalar `graphviz`/`matplotlib`
  en `.venv-docs`, o que el equipo dibuje el diagrama en draw.io y lo exporte a PNG.
- **Entregable:** carpeta de insumos completa y decisiones tomadas.

### F1 — Andamiaje editorial sobre la plantilla (C1, C2, C5, C6, C12)
- Portada, encabezados y pies exactamente de la plantilla.
- Título nuevo: **«Sistema Inteligente de Reportes de Emergencia Ciudadana (SIREC): clasificación y priorización automática de reportes ciudadanos de emergencia»**, con la sigla definida en su primera aparición del cuerpo.
- Índice con numeración jerárquica; numerar los **9 encabezados de tercer nivel** (3.1.1 Perfiles de usuario, 3.1.2 Resultados de la encuesta, 3.1.3 Mapa de empatía, 3.1.4 Hallazgos clave, etc.).
- Salto de página antes de cada capítulo y del anexo (hoy solo hay 2 saltos para 6 arranques).
- Estilo de tabla de la plantilla aplicado a las 9 tablas.
- **Entregable:** documento vacío de contenido nuevo pero con el formato aprobado.
- **Criterio de terminado:** el documento, impreso, es indistinguible en formato del ejemplo de la plantilla.

### F2 — Cirugía de redacción sobre lo que ya existe (C4, C5, C8, C11)
- Párrafo de presentación después de «1. Introducción» y de «2. Objetivos» (hoy los dos títulos van pegados a su subtítulo).
- Dividir los 3 párrafos largos identificados: «Criterio de urgencia» (141 palabras), «Origen y composición del corpus» (127) y el de trabajos previos (142).
- Convertir a prosa los bloques de viñetas que son argumentación: hallazgos clave de 3.1 (7 viñetas), HMW de 3.2 (5), fundamento teórico de 3.3.1 (6), módulos de 3.5 (5). Se conservan como lista solo los objetivos específicos y el alcance del MVP.
- Reforzar el objetivo general con el **cómo se mide** y verificar que los 6 específicos conduzcan a él.
- **Criterio de terminado:** ningún párrafo pasa de 10 renglones; ningún encabezado queda sin texto debajo.

### F3 — Contenido sustantivo nuevo (C3, C7, C9, C10) — la fase más pesada
- **Introducción (3 págs):** contexto y motivación con datos citados, planteamiento del problema, justificación de la relevancia, propósito general, delimitación del MVP y cierre con la estructura del documento.
- **3.3.1 Fundamento teórico (4.5 págs):** prosa encadenada que recorra representación de texto y TF-IDF, regresión logística y SVM, clasificación multiclase, la arquitectura Transformer, BERT y BETO, tokenización por subpalabras, ajuste fino y transferencia, desbalance de clases, calibración de la confianza, métricas por clase y macro, y acuerdo entre evaluadores. Cada concepto se explica **y se conecta con la decisión de diseño de SIREC** que lo usa.
- **3.3.2 Estado del arte (4 págs):** pasar de 3 a 6–8 trabajos. Cada uno con la ficha de 12 campos que pide C10, en prosa. La tabla comparativa se mueve al **final** como síntesis. Cierre con conclusiones y la brecha.
- **Criterio de terminado:** cada afirmación teórica o de antecedentes tiene su cita, y cada cita existe en Referencias.

### F4 — Prototipo visual (C13)
- **Figura 1 — Arquitectura de SIREC:** formulario → API .NET 8 → microservicio FastAPI/BETO → PostgreSQL → panel del operador, con las entradas y salidas de cada módulo rotuladas sobre las flechas.
- **Figura 2 y 3 — Pantallas principales:** formulario de captura y panel priorizado (wireframe o captura real del despliegue).
- Texto que explique **cómo se le presentan al operador la prioridad, la confianza del modelo, los errores y los casos que requieren revisión humana** — hoy el documento no dice nada de esto y es una pregunta directa del profesor.
- Las figuras llevan «Figura N. Título» y nota de fuente («Elaboración propia»), llamada desde el texto e interpretación.

### F5 — Diseño de la evaluación, sección 3.7 nueva (C14)
- Protocolo comparativo baseline TF-IDF (regresión logística y SVM) frente a BETO ajustado, **mismo corpus y mismas particiones**, con semilla fija y estratificación declaradas para que sean reproducibles.
- Métricas: precision, recall y F1 por clase y macro, matriz de confusión, y conteo explícito de **falsos negativos en «persona en riesgo» y «urgencia alta»**.
- Calidad del etiquetado con kappa de Cohen y su umbral de aceptación.
- Latencia de respuesta de extremo a extremo.
- **Criterios mínimos de éxito**, numéricos y comprometidos por escrito (qué valor de F1 macro, qué recall mínimo en clases críticas, qué kappa, qué latencia). Esto es lo que él reclama con «no basta con indicar que el sistema será evaluado».

### F6 — Tablas (C11, C12)
- Renumerar las 9 tablas de forma consecutiva con «Tabla N. Título» y nota de fuente. **Hoy no hay ni un rótulo en el documento**, así que se crean los 9.
- Llamada desde el texto («como se observa en la Tabla 4…») y un párrafo de interpretación por tabla: qué muestra y qué se concluye.
- Matriz de selección de 3.6: criterios y **pesos** justificados, escala explicada, **quién asignó las puntuaciones** (los tres integrantes, y cómo se resolvieron los desacuerdos) y con qué evidencia.

### F7 — Referencias y citas (C15)
- Llevar de 7 a **20–25** entradas, todas verificadas y todas citadas en el texto; y a la inversa, ninguna cita huérfana.
- Candidatas por bloque, **cada una a verificar antes de entrar** (si no se verifica, se descarta):
  - *Contexto y estadísticas:* CENAPRED (impacto socioeconómico de los desastres), CONAGUA / Servicio Meteorológico Nacional, declaratorias de emergencia publicadas en el DOF, INEGI, SESNSP (llamadas de emergencia al 911).
  - *Representación de texto y modelos clásicos:* Salton y Buckley (1988), Joachims (1998), Cortes y Vapnik (1995), Manning, Raghavan y Schütze (2008), Jurafsky y Martin.
  - *Transformers y ajuste fino:* Vaswani et al. (2017), Devlin et al. (2019), Cañete et al. (2020), Howard y Ruder (2018), Wolf et al. (2020), Sennrich et al. (2016) o Kudo y Richardson (2018) para tokenización.
  - *Desbalance, calibración y métricas:* Chawla et al. (2002), Japkowicz y Stephen (2002), Guo et al. (2017), Sokolova y Lapalme (2009).
  - *Acuerdo entre evaluadores:* Cohen (1960) —ya está—, Landis y Koch (1977), Artstein y Poesio (2008).
  - *Dominio de emergencias y desastres:* Imran et al. (2015) —ya está—, Olteanu et al. (CrisisLex), Alam et al. (CrisisBench), Nguyen et al. (2017), más los dos latinoamericanos que ya citamos.
- APA 7 uniforme, con DOI donde exista.

### F8 — Cierre y control de calidad
- Lectura completa de corrido buscando saltos de estilo entre lo viejo y lo nuevo.
- Verificación mecánica con `python-docx`: conteo de palabras, tablas rotuladas, figuras rotuladas, párrafos largos, encabezados sin texto, citas sin referencia.
- Conteo real de páginas ya en la plantilla; ajuste si queda fuera de 20–30.
- Exportar el PDF (desde Word del equipo: en la EC2 no hay LibreOffice ni pandoc).
- Actualizar `Entrega 2 - README (decisiones y estado).md` y `Entrega 2 - PENDIENTES.md`, y commit en `main` con el `.docx`, el PDF y las figuras.

---

## 6. Orden recomendado y esfuerzo

```
F0 (insumos) ──► F1 (plantilla) ──► F3 (contenido nuevo) ─┐
                      │                                   ├──► F6 (tablas) ──► F7 (refs) ──► F8 (QA)
                      └──► F2 (cirugía) ──► F4 (figuras) ─┘
                                            F5 (evaluación)
```

| Fase | Esfuerzo | Depende de |
|---|---|---|
| F0 | trabajo del equipo, no mío | — |
| F1 | 1 sesión | plantilla |
| F2 | 1 sesión | F1 |
| F3 | **3 sesiones** (la intro, el teórico y el estado del arte, una cada uno) | F1 + fuentes de F0 |
| F4 | 1 sesión | decisión de figuras (F0) |
| F5 | 1 sesión | — |
| F6 | 1 sesión | F1, F3 |
| F7 | 1 sesión | F3 |
| F8 | media sesión | todas |

Total: **9–10 sesiones de trabajo**. Se puede entregar por fases para que el equipo
revise sobre la marcha en lugar de leer 28 páginas de golpe al final.

---

## 7. Riesgos y cómo se manejan

| Riesgo | Manejo |
|---|---|
| **Citas inventadas.** Es el riesgo más grave: una referencia falsa hunde el trabajo más que una sección corta | Ninguna cita entra sin verificar la fuente. Si no se puede verificar, se elimina la afirmación o se reformula sin ella |
| **La plantilla llega al final** y hay que rehacer el formato de 28 páginas | Plan B de la sección 3.1: trabajar solo con estilos nombrados desde el inicio |
| **Ampliar con relleno**, que es exactamente lo que él prohibió | El presupuesto de la sección 4 asigna el crecimiento a análisis; en la revisión final se marca cualquier párrafo que no aporte argumento |
| **Sobrevender la encuesta** de 42 respuestas como si fuera representativa | Ya está declarada como muestra no probabilística; mantener esa nota al ampliar 3.1 |
| **Comprometer criterios de éxito** en 3.7 que el modelo real no alcance | Fijar los umbrales con lo que ya se observó en el sistema desplegado, no con cifras aspiracionales |
| Las visitas a Protección Civil no dieron datos duros | Ya está redactado como limitación metodológica; se conserva así |

---

## 8. Checklist de aceptación (se revisa antes de entregar)

- [ ] Formato 100 % de `plantilla.docx`: portada, tipografía, márgenes, interlineado, encabezados, pies y diseño de tablas
- [ ] Título con el nombre completo del sistema y la sigla definida en su primera aparición
- [ ] Índice con numeración jerárquica idéntica a la del cuerpo
- [ ] Cada capítulo y el anexo empiezan en página nueva
- [ ] Ningún encabezado seguido de otro sin texto entre ambos
- [ ] Desarrollo sustantivo entre 20 y 30 páginas, verificado en la plantilla
- [ ] Ningún párrafo de más de 10–12 renglones
- [ ] Introducción de 2 páginas mínimo, en prosa y con estadísticas citadas
- [ ] Objetivo general con herramienta, resultado esperado y forma de medirlo
- [ ] Fundamento teórico de 3–5 páginas en prosa, con citas y los 13 conceptos que pidió
- [ ] Estado del arte de 3–4 páginas con la ficha completa por trabajo, tabla al final y brecha
- [ ] Las 9 tablas: «Tabla N. Título», fuente, consecutivas, llamadas desde el texto e interpretadas
- [ ] Matriz de selección con criterios, pesos, escala, valoradores y evidencia
- [ ] Figura de arquitectura con módulos, entradas, salidas y conexiones
- [ ] Wireframes o capturas de las pantallas principales
- [ ] Explicación de cómo se presentan prioridad, confianza, errores y revisión humana
- [ ] Sección 3.7 con protocolo comparativo, particiones reproducibles, métricas por clase y macro, matriz de confusión, falsos negativos críticos, kappa, latencia y criterios mínimos de éxito numéricos
- [ ] 20–25 referencias APA 7, todas verificadas, todas citadas y sin citas huérfanas
- [ ] PDF exportado y todo versionado en git

---

## 9. Herramientas

- Edición del `.docx`: `python-docx` ya instalado en `/home/ubuntu/proyectos/sirec/.venv-docs`.
- Auditoría mecánica: scripts propios sobre ese venv (los usados para el diagnóstico de la sección 1).
- Figuras: pendiente de decidir en F0 (no hay matplotlib, graphviz, pandoc ni LibreOffice en la máquina).
- PDF: exportación desde Word en la máquina del equipo.
- Respaldo del archivo original antes de la primera modificación: copia `pre-correcciones-2026-08-06` en `entregas/`.
