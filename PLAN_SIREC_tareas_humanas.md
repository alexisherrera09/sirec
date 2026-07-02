# SIREC — Tareas humanas del equipo (qué hacer y cuándo)

> Documento para el equipo (3 personas). Complementa a:
> - `PLAN_SIREC_ClaudeCode_total.md` (Claude construye todo el código)
> - `PLAN_SIREC_AWS_Despliegue.md` (despliegue posterior)
>
> Claude Code hace toda la programación. Este archivo lista lo que SOLO ustedes pueden hacer, en el momento exacto en que deben hacerlo. Las tareas están numeradas en orden cronológico.

---

## MOMENTO 0 — Antes de abrir Claude Code (preparación, ~1 hora)

**H0.1 — Preparar la máquina de desarrollo.**
Instalar en la computadora donde correrá el proyecto: .NET 8 SDK, Node.js 20+, Python 3.11+, Docker Desktop y Git. Claude Code puede guiar la instalación, pero descargar e instalar requiere sus permisos de administrador.

**H0.2 — Crear la carpeta del proyecto y el repositorio Git.**
Carpeta raíz `sirec/`, iniciar repositorio (idealmente en GitHub privado del equipo). Copiar dentro los tres documentos del plan.

**H0.3 — Abrir Claude Code en VS Code y seleccionar el modelo** (Sonnet). Entregarle `PLAN_SIREC_ClaudeCode_total.md` y pedirle la Fase A1.

---

## MOMENTO 1 — Durante las Fases A1, B1–B5, C1–C2 (Claude programa; ustedes verifican)

**H1.1 — Verificar cada checkpoint en su propia máquina.**
Claude ejecuta y reporta los checkpoints, pero ustedes deben reproducir al menos los principales (A1, B2, C2) con sus propios ojos: abrir el navegador, mandar un reporte, verlo en el panel. No den por buena una fase solo porque Claude dice que pasó.

**H1.2 — Leer el código generado de cada componente (mínimo 1 hora por componente, repartido entre los tres).**
No para corregirlo, sino para ENTENDERLO: en la defensa les preguntarán cómo funciona y "lo hizo la IA" no es una respuesta defendible. Sugerencia de reparto: una persona se especializa en el backend .NET, otra en el microservicio Python + modelo, otra en el frontend React. Cada quien debe poder explicar su parte sin ayuda.

**H1.3 — Hacer commits al repositorio al cierre de cada fase.**
Con mensajes claros ("Fase B2 completada: endpoint público con fallback"). Esto documenta el proceso para la memoria.

---

## MOMENTO 2 — En cuanto Claude termine las Fases D1 y D2 (la parte humana crítica, ~10–14 horas repartidas entre los 3)

Esta es la ventana de trabajo humano más importante del proyecto. El profesor exige estos entregables y NO pueden delegarse a la IA.

**H2.1 — Aprobar la guía de etiquetado (D1). [30–60 min, los tres juntos]**
Leer `guia_etiquetado.md` que Claude redactó. Verificar que los criterios de urgencia y los casos de frontera les parecen defendibles. Pedir ajustes a Claude si algo no convence. Nada se etiqueta hasta aprobar la guía.

**H2.2 — Recolectar ~300–400 reportes REALES. [4–6 horas repartidas]**
Fuentes: publicaciones en X/Facebook durante contingencias pasadas en su municipio, notas de prensa local, reportes citados en medios. Copiar solo el texto, ANONIMIZAR (quitar nombres, teléfonos, direcciones exactas) y registrar la fuente genérica. Guardarlos en el CSV que la herramienta de Claude espera. Regla: el conjunto de prueba del modelo saldrá SOLO de estos reportes reales; sin ellos, las métricas no valen.

**H2.3 — Etiquetar los reportes reales con la herramienta de Claude. [2–3 horas repartidas]**
Cada quien etiqueta su lote siguiendo la guía aprobada. Ante la duda, consultar los casos de frontera de la guía; si surge un caso nuevo, anotarlo para añadirlo a la guía.

**H2.4 — Doble etiquetado para el kappa. [1.5–2 horas, exactamente DOS personas]**
Dos integrantes etiquetan de forma INDEPENDIENTE (sin verse, sin comentar) la misma muestra de ~150–200 reportes reales en el modo doble de la herramienta. No comparen respuestas hasta terminar. Después, Claude calcula el kappa de Cohen. Este dato es requisito explícito del profesor.

**H2.5 — Revisar una muestra del corpus sintético de Claude. [~30 min]**
Leer al azar 30–50 de los reportes sintéticos generados y confirmar que suenan a español de México verosímil. Marcar a Claude los que suenen artificiales para regenerarlos.

---

## MOMENTO 3 — Durante las Fases D4–D6 (entrenamiento; ustedes deciden y validan)

**H3.1 — Si no hay GPU local: correr el notebook en Google Colab. [1 hora de atención]**
Claude genera `entrenar_beto_colab.ipynb`; alguien del equipo lo sube a Colab con su cuenta de Google, lo ejecuta, y descarga el modelo resultante a `/datos-modelo/modelo_exportado/`. Claude no tiene cuenta de Google: esto es de ustedes.

**H3.2 — Leer y validar `comparacion_modelos.md`. [30–45 min, los tres]**
Verificar que las tablas de métricas por clase están completas, que BETO supera al baseline, y ENTENDER el análisis de falsos negativos de `persona_en_riesgo` y `urgencia=alta`. El profesor preguntará por esto; deben poder explicarlo sin leer.

**H3.3 — Probar el sistema de extremo a extremo con el modelo real.**
Repetir la prueba del CHECKPOINT C2 con el modo modelo activo. Escribir reportes inventados variados y evaluar a ojo si las clasificaciones son razonables. Anotar los errores curiosos: sirven para la sección de limitaciones de la memoria.

---

## MOMENTO 4 — Antes y durante el despliegue en AWS (solo cuando TODO funcione en local)

**H4.1 — Preguntar en UNIR por créditos de AWS Academy/Educate. [cuanto antes, no esperar a este momento]**
Si hay créditos, la instancia sale gratis. Hacerlo desde ya aunque el despliegue sea después.

**H4.2 — Crear/configurar la cuenta AWS. [1 hora]**
Cuenta, método de pago, y OBLIGATORIO: alarma de presupuesto (AWS Budgets) a $5 USD antes de crear nada. Crear el par de llaves SSH y guardarlo seguro. Claude no puede crear cuentas ni aceptar cobros: esto es de ustedes.

**H4.3 — Decidir y configurar el dominio.**
Dominio propio o DuckDNS gratuito para la API. Apuntarlo a la IP elástica de la instancia. (Claude los guía, pero el registro es de ustedes.)

**H4.4 — Ejecutar el despliegue con Claude siguiendo `PLAN_SIREC_AWS_Despliegue.md`.**
Ustedes crean la instancia EC2 y el bucket S3 desde la consola AWS (o dan a Claude acceso vía AWS CLI configurado con sus credenciales — decisión de ustedes; si configuran AWS CLI, Claude puede automatizar casi todo). Verificar el checklist de seguridad final del documento ANTES de dar por terminado.

**H4.5 — Definir credenciales de producción.**
Contraseña real de PostgreSQL, usuario/contraseña del operador del panel, secreto JWT: valores nuevos, no los de desarrollo. Guardarlos en un gestor de contraseñas del equipo.

**H4.6 — Apagar la instancia cuando no se use.**
EC2 cobra por hora encendida. Encenderla para trabajar y para la defensa; apagarla el resto del tiempo. Revisar el panel de facturación una vez por semana.

---

## MOMENTO 5 — Cierre académico (en paralelo desde el MOMENTO 2, no al final)

**H5.1 — Redactar la memoria conforme avanza el proyecto.**
Cada fase terminada se documenta esa misma semana (metodología, decisiones, resultados). La memoria es donde se gana la calificación; no se deja para el final. Los archivos que Claude genera (`reporte_corpus.md`, `resultados_baseline.md`, `comparacion_modelos.md`, `guia_etiquetado.md`) son insumos directos de capítulos.

**H5.2 — Cubrir explícitamente los 5 requisitos del profesor en la memoria.**
Checklist: (1) categorías precisas, (2) origen de reportes en tabla cuantificada, (3) procedimiento de etiquetado + kappa reportado, (4) criterio de urgencia con ejemplos de frontera, (5) baseline + métricas por clase + análisis de falsos negativos. Ninguno puede faltar.

**H5.3 — Declarar el uso de IA según la normativa de UNIR.**
Verificar qué exige la universidad sobre declarar herramientas de IA en el desarrollo, y cumplirlo. El corpus sintético ya queda declarado en `reporte_corpus.md`; el uso de Claude Code en el desarrollo debe declararse conforme a la política vigente.

**H5.4 — Preparar la defensa. [última semana]**
Ensayar la demo en vivo (formulario → panel) con la instancia encendida y una petición de calentamiento previa. Cada integrante domina su componente (ver H1.2). Preparar respuestas para las preguntas previsibles: por qué BETO y no un LLM, por qué microservicios, por qué esos falsos negativos, cómo se etiquetó.

---

## RESUMEN DE CARGA HUMANA TOTAL ESTIMADA

| Momento | Horas aprox. (equipo completo) |
|---|---|
| 0 — Preparación | 1–2 h |
| 1 — Verificación y lectura de código | 6–9 h (repartidas) |
| 2 — Corpus real, etiquetado y kappa | 10–14 h (repartidas) |
| 3 — Entrenamiento y validación | 2–3 h |
| 4 — AWS | 3–5 h |
| 5 — Memoria y defensa | el resto del esfuerzo académico |

La programación completa la hace Claude Code. La calificación la ganan ustedes en los momentos 2 y 5.
