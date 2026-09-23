# Revisión del documento final — SIREC (Grupo 3032C)

> Análisis del archivo `260826_Grupo_3032C_Entrega_2_SIREC_v2.0.docx` contra la rúbrica oficial
> de la entrega final y la retroalimentación del profesor Efrén Juárez.
>
> **Fecha del análisis:** 23 de septiembre de 2026 · **Entrega:** 30 de septiembre de 2026
> **Alcance:** solo los renglones documentales de la rúbrica (70 %). El video (30 %) no se evalúa aquí.
> **Autor del análisis:** Claude (Claude Code), a petición de Alexis Herrera.

---

## 1. Calificación estimada: **≈ 8.1 / 10** (Notable)

Calculada sobre los seis indicadores documentales de la rúbrica, renormalizados a base 10.

| Indicador | Peso | Nota | Justificación |
|---|---:|---:|---|
| Estilo y formato académico | 10 % | **8** | Caps. 1-4 impecables. Caps. 5-7 caen: encabezados en minúscula y sin acentos, erratas, viñetas donde antes había prosa, cero citas. |
| Estructura / apartados | 10 % | **8** | Ya están todos los apartados + Anexos A, B y C. Extensión cumplida. Pierde por la ruptura de registro entre bloques. |
| Alcance | 10 % | **9** | La contribución ya está demostrada, no solo argumentada: corpus propio, doble clasificación, BETO > baseline, sistema operativo. |
| Implementación | 10 % | **7.5** | Cap. 5 cubre todo lo pedido (incluidos costos y mantenimiento) y Scrum es de 10. Pierde por lo que no muestra: sin captura de código, despliegue real desaprovechado. |
| Verificación | 10 % | **7** | Cap. 6 es sustancial y cierra los huecos que faltaban. Pierde por ausencias concretas (§3). |
| Relación objetivos ↔ desarrollo ↔ conclusiones | 20 % | **8.5** | Cap. 7 recorre objetivo por objetivo, con aportaciones, hallazgos, limitaciones honestas y trabajo futuro. Buena prosa. |

**Contexto del salto.** La versión v1.1 (la que obtuvo 10 en la Entrega 2) valdría ≈ **4.9** bajo esta
rúbrica, porque la rúbrica final mide un trabajo completo y a esa versión le faltaban los capítulos
5, 6 y 7. El v2.0 los incorpora y sube a ≈ 8.1.

**Deudas ya saldadas en el v2.0** (estaban pendientes y ahora están medidas y reportadas):

- Tiempo de triaje manual vs. automático: 15.80 s → 0.82 s (−94.81 %), §6.9.
- Latencia por reporte: 0.822 s extremo a extremo, por debajo del umbral de 2 s comprometido en la Tabla 10. §6.8.2.
- Presupuesto y estimación de costos: USD 66.79/mes, USD 801.48/año. §5.1.3.
- Plan de mantenimiento y ciclo de vida, con versionado semántico. §5.4.

---

## 2. Verificaciones realizadas

| Qué se comprobó | Resultado |
|---|---|
| Correspondencia citas ↔ referencias | **Correcta.** 33 referencias, las 33 citadas en el cuerpo; sin citas huérfanas. |
| URL del repositorio del §5.2.3 | **Correcta.** `alexisherrera09` coincide con el remote real. (El `README.md` del repo tiene una URL desactualizada: `alexisherrera22`.) |
| `urgencia baja` = 66 casos (Tabla 28) | **Correcto** para el corpus completo de 400. En el gold de 180 son 14. |
| Extensión contra los mínimos orientativos | **Cumplida.** Cap. 5 ≈ 12 pp. (esperadas 11) · Cap. 6 ≈ 15 pp. (esperadas 9) · Cap. 7 ≈ 6 pp. (esperadas 3) · Referencias ≈ 4 pp. (esperadas 3). |

---

## 3. Hallazgos que frenan la nota, ordenados por impacto

### 3.1. No hay matriz de confusión ni métricas por clase completas — *(Verificación)*

El punto más grave, porque es **incumplimiento de un compromiso propio**. El objetivo específico 5
dice literalmente *"métricas por clase (precisión, exhaustividad y medida F1) y matriz de confusión"*;
la Tabla 10 del cap. 4 la lista como evidencia; y era uno de los cinco requisitos originales del
profesor desde la Entrega 1.

El cap. 6 reporta macro-F1 y el recall de las dos clases críticas, pero **no hay tabla por clase de
las 7 categorías ni de los 3 niveles de urgencia, ni una sola matriz de confusión**. Agravante: el
§7.2 afirma que ese objetivo se cumplió.

Los datos ya existen en `datos-modelo/comparacion_modelos.md` y `datos-modelo/resultados_baseline.md`.

### 3.2. §6.7 "Robustez y análisis de errores" no hace ni robustez ni análisis de errores — *(Verificación)*

La sección enumera propiedades del diseño experimental (gold independiente, doble anotación, kappa,
adjudicación, exclusión del test). El profesor pidió explícitamente **pruebas de sensibilidad ante
ruido** y **análisis de errores profundo explorando casos límite**. El título promete lo que el
contenido no entrega, que se lee peor que no tener la sección.

### 3.3. El experimento de tiempo de triaje no es reproducible — *(Verificación)*

Regla de oro que dio el profesor: *"cualquier evaluador externo debe poder replicar tus resultados
leyendo únicamente tus instrucciones"*.

El §6.9 no declara cuántos reportes se usaron, cuántos evaluadores participaron, ni cómo se cronometró.
Además compara 15.80 s (lectura y decisión humana) contra 0.82 s (latencia de máquina): no son la
misma magnitud, porque el escenario asistido también tiene tiempo humano de validación. Es el número
más vistoso del documento y el más fácil de desarmar en la defensa.

### 3.4. La evaluación de sesgos son cinco viñetas — *(Verificación)*

El profesor lo repitió tres veces en la sesión: *"incluir una evaluación de equidad, identificar
sesgos — esto es muy, muy, muy importante"*, y su ejemplo fue justamente el caso de este proyecto
(un dataset desbalanceado donde un modelo trivial acierta alto sin detectar nada).

El §6.10 "Consideraciones éticas" son cinco viñetas de IA responsable. El material existe (desbalance
de clases documentado, sesgo de fuentes mediáticas ya reconocido en Limitaciones); falta convertirlo
en un apartado que se llame y haga lo que él pidió.

### 3.5. El despliegue real está desaprovechado — *(Implementación)*

El §5.3 dice que el sistema *"fue diseñado para funcionar tanto en entornos locales como en
infraestructura cloud"* — genérico. Pero existe un despliegue real en producción: EC2, Nginx como
única puerta, HTTPS con certificado de Let's Encrypt y renovación automática, backend y microservicio
bajo systemd solo en localhost, puertos 5000/8000/5432 verificados como cerrados desde internet, y
prueba de resiliencia ejecutada contra producción. Todo documentado en `DESPLIEGUE_EC2_REALIZADO.md`.

**La URL pública no aparece en ninguna parte del documento.** El profesor dijo que no esperaba que
todos lograran desplegar en producción; el equipo lo hizo y no se nota.

### 3.6. No hay captura de código — *(Implementación)*

Lo pidió literal: *"incluye alguna captura de código e incluye alguna captura de ejecución"*. Hay
nueve capturas de interfaz (Figuras 9-17) y ninguna de código.

### 3.7. Formato de los capítulos nuevos — *(Estilo)*

- Encabezados del cap. 6 y **todo** el cap. 7 en minúscula y sin acentos: `Hipotesis y criterio final
  de validacion`, `evaluacion del modelo de referencia`, `evaluacion de beto`, `comparacion entre
  modelos`, `robustez y analisis de errores`, `Validacion operativa`, `Consideranciones eticas`,
  `el problema abordado y la solucion propuesta`, `cumplimiento de los objetivos de investigacion`.
- **Tabla 28 numerada dos veces** ("Clases con menor soporte" y "Resumen de pruebas realizadas").
- Falta el rótulo **"Prueba 3"** en la secuencia de pruebas E2E (salta de Prueba 2 a Prueba 4).
- Tabla 16 con un pie que es una frase: *"Tabla 16. Se propone Semantic Versioning"*.
- Tabla 29 sin línea de Fuente. Tabla 23 dice "Fuente elaboración propia" (falta el dos puntos).
- **Párrafo duplicado** en §5.2.1: dos frases seguidas describen el preprocesamiento con distintas palabras.
- Erratas: *"Consideranciones"* · *"fueron resultados"* → resueltos · *"Reducicon%"* · *"todas métricas"*
  → todas las métricas · *"técnicas avanzadas de aplicabilidad"* → explicabilidad.
- **Ruptura de registro:** los caps. 5-7 usan listas de viñetas donde los caps. 1-4 usaban prosa
  académica. El profesor advirtió: *"hay que mantener la prosa académica"*.

### 3.8. Cero citas en los capítulos 5, 6 y 7 — *(Estilo)*

La Discusión del §6.7.3 afirma *"esto coincide con estudios previos sobre clasificación de texto en
conjuntos desbalanceados"* sin citar, teniendo a He y García (2009) ya en la lista de referencias.
Tres o cuatro citas bien puestas recuperan la continuidad académica que el profesor elogió en los
capítulos 1-4.

### 3.9. Inconsistencia de versiones — *(Estilo / coherencia)*

La Tabla 13 dice `.NET 10`, `Python 3.14`, `Ubuntu 26.04`; la Tabla 14 dice `ASP.NET Core 8`. El
profesor advirtió expresamente sobre *"que coincida en todo el documento"*.

---

## 4. Proyección de la nota

| Escenario | Nota del documento |
|---|---:|
| **Estado actual (v2.0)** | **8.1** |
| + matriz de confusión y métricas por clase (3.1) | 8.6 |
| + robustez real, experimento reproducible, sesgos (3.2, 3.3, 3.4) | 9.2 |
| + despliegue real, URL pública, captura de código (3.5, 3.6) | 9.5 |
| + limpieza de formato y citas (3.7, 3.8, 3.9) | **9.7** |

Los puntos 3.1, 3.5, 3.6, 3.7, 3.8 y 3.9 son **trabajo de edición**: los datos y las evidencias ya
existen en el repositorio, solo hay que trasladarlos al documento.

Los puntos 3.2, 3.3 y 3.4 requieren **ejecutar algo nuevo**, y son justo los que el profesor
enfatizó más en la sesión del 10 de septiembre.

---

## 5. Anexo — Referencia rápida de lo que se evalúa

### 5.1. La rúbrica completa

| Bloque | Indicador | Peso |
|---|---|---:|
| **Estructura 20 %** | Estilo y formato académico | 10 % |
| | Estructura / apartados | 10 % |
| **Contenido 50 %** | Alcance | 10 % |
| | Implementación (incluye aplicación de Scrum) | 10 % |
| | Verificación (cap. 6) | 10 % |
| | Relación objetivos ↔ planteamiento ↔ desarrollo ↔ conclusiones | 20 % |
| **Exposición 30 %** | Video presentación | 10 % |
| | Dominio del contenido expuesto | 20 % |

La rúbrica **solo se aplica en la entrega final**; las entregas anteriores no la usaban. La entrega
final vale el **70 % de la calificación** (la Entrega 2 valía 1.5 puntos y obtuvo 10).

### 5.2. Extensión orientativa (mínimos; no penaliza pasarse; no cuenta portada, índices ni anexos)

| Capítulo | Páginas esperadas |
|---|---|
| 5. Implementación de la propuesta | ~11 |
| 6. Validación y diseño experimental | ~9 |
| 7. Conclusiones y trabajo futuro | ~3 |
| Referencias bibliográficas | ~3 |

### 5.3. El video (30 %) — pendiente, no evaluado en este análisis

- **Máximo 10 minutos**, un único archivo por equipo.
- **Los tres integrantes aparecen con cámara encendida y hablan equitativamente.**
- **Plantilla de PowerPoint obligatoria** — plataforma, Fase 4, "plantilla de exposición".
- Subir a **YouTube**, link en la entrega, cuidando los permisos de acceso.
- **El protagonista es el prototipo**: demostrar en vivo que resuelve el problema planteado.
  La demo puede pregrabarse e insertarse (el profesor lo autorizó expresamente).
- Estructura sugerida: título → índice → introducción → objetivos → desarrollo de la propuesta →
  demo del prototipo → evaluación → conclusiones.
- Sin diapositivas saturadas de texto: imágenes, diagramas, figuras.
- El renglón de mayor peso es **"dominio del contenido expuesto" (20 %)**: que cada integrante
  demuestre que entiende lo que hizo, sin leer.

### 5.4. Punto abierto: publicar el repositorio

El profesor recomienda incluir el link al repositorio público, y el documento ya lo hace en el §5.2.3.
Antes de hacerlo público conviene revisar que no queden credenciales en el historial de git: la
contraseña del panel de producción aparece escrita en `DESPLIEGUE_EC2_REALIZADO.md` y en
`AVANCE_Y_TAREAS_HUMANAS.md`. El historial de git es permanente, así que borrarla ahora no la retira
de los commits anteriores; el orden correcto es cambiarla en el servidor primero.
