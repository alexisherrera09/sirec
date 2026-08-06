# Entrega 2 — Pendientes del equipo

> Estado tras aplicar la retroalimentación del profesor (`Entrega 2 comentarios.txt`)
> sobre la plantilla oficial de UNIR. El documento a entregar es
> **`Entrega 2 Final.docx`**; el anterior (`Entrega 2 - SIREC (Desarrollo conceptual
> Design Thinking).docx`) queda como histórico.
> Última actualización: 2026-08-06.

---

## Pendientes activos (le toca al equipo)

### 1. Actualizar el índice en Word
- **Qué falta:** abrir `Entrega 2 Final.docx` en Word y actualizar el índice de
  contenidos (clic derecho › Actualizar campos, o F9). El documento ya trae la
  marca `updateFields`, así que Word suele ofrecerlo al abrir.
- **Por qué:** el índice es un campo automático; `python-docx` no puede calcular
  los números de página.
- **Estado:** ⏳ pendiente

### 2. Verificar el conteo de páginas en Word
- **Qué falta:** confirmar que el desarrollo (capítulos 1 a 3, sin portada, índice
  ni anexos) queda entre 20 y 30 páginas.
- **Medición actual:** **30 páginas** con LibreOffice (páginas 4 a 33 del PDF de
  vista previa). Word puede variar en ±1 página.
- **Si se pasa de 30:** hay margen de recorte en 3.3 y 3.7 sin tocar los mínimos
  que exige el profesor; ver `build/README.md`.
- **Estado:** ⏳ pendiente

### 3. Lectura de revisión del equipo
- **Qué falta:** que los tres integrantes lean el documento completo, sobre todo
  el apartado **3.7**, donde se comprometen umbrales numéricos (F1 macro ≥ 0.75,
  exhaustividad ≥ 0.90 en clases críticas, kappa ≥ 0.60, latencia p95 ≤ 3 s).
- **Por qué importa:** son compromisos evaluables; si el equipo considera alguno
  inalcanzable, hay que ajustarlo **antes** de entregar, no después de medir.
- **Estado:** ⏳ pendiente

### 4. Capturas reales del sistema (opcional)
- **Qué falta:** las figuras 2 y 3 son wireframes propios. Como SIREC ya está
  desplegado, podrían sustituirse por capturas reales del formulario y del panel.
- **Nota:** no es requisito; los wireframes ya cumplen lo que pidió el profesor.
- **Estado:** ⏳ opcional

---

## Resuelto en esta revisión (2026-08-06)

Los 15 señalamientos del profesor, con su trazabilidad completa en
`Entrega 2 - PLAN DE CORRECCIONES.md`:

- ✅ **Plantilla oficial de UNIR.** El documento se genera sobre `plantilla.docx`:
  portada, A4, márgenes 3/2/2,5/2,5 cm, Calibri 12, interlineado 1,5, encabezado
  con los tres integrantes y el título, pie con número de página.
- ✅ **Título con la sigla definida.** «Sistema Inteligente de Reportes de
  Emergencia Ciudadana (SIREC): clasificación y priorización automática…».
- ✅ **Extensión.** De ~9 páginas a **30 de desarrollo**, dentro del rango 20–30.
- ✅ **Numeración jerárquica** (1., 1.1, 3.1.1) en el cuerpo y en el índice. La
  plantilla traía viñeta en el segundo nivel; se corrigió la numeración multinivel
  conservando la tipografía.
- ✅ **Cada capítulo y anexo en página nueva**, y ningún título pegado a otro.
- ✅ **Párrafos de 5–8 renglones**: ninguno supera las 120 palabras.
- ✅ **Introducción de 3 páginas** con estadísticas oficiales citadas: Cenapred
  (2024) y datos abiertos del 9-1-1 (Centro Nacional de Información, 2025 y 2026).
- ✅ **Objetivo general medible** (qué, con qué IA, qué resultado y cómo se mide).
- ✅ **Fundamento teórico (3.3.1)** en prosa con citas, cubriendo los 13 conceptos
  que pidió el profesor.
- ✅ **Estado del arte (3.3.2)** con 6 trabajos y ficha completa por trabajo; la
  tabla comparativa va al final como síntesis, y cierra con la brecha.
- ✅ **Viñetas convertidas a prosa** en hallazgos, HMW, fundamento teórico y módulos.
- ✅ **12 tablas** con «Tabla N. Título», fuente, numeración consecutiva, llamada
  desde el texto e interpretación.
- ✅ **Matriz de selección explicada**: criterios, pesos, escala, quién valoró
  (consenso de los tres integrantes) y con qué evidencia.
- ✅ **Prototipo visual**: figura 1 (arquitectura con entradas, salidas y
  conexiones), figuras 2 y 3 (formulario y panel), y el apartado 3.5.3 explica
  cómo se presentan prioridad, confianza, errores y revisión humana.
- ✅ **Apartado 3.7 nuevo**: protocolo comparativo TF-IDF frente a BETO con las
  mismas particiones y semilla fija, métricas por clase y macro, matriz de
  confusión, falsos negativos críticos, kappa, latencia y criterios mínimos de
  éxito con umbrales.
- ✅ **Referencias: de 7 a 29**, todas verificadas, todas citadas y sin citas
  huérfanas (comprobado con `build/auditar.py`).
- ✅ **Anexos A y B** con el instrumento de la encuesta, los resultados agregados,
  el mapa de empatía y el criterio operativo de urgencia.

## Recordatorio (no es de esta entrega)

- **Declaración de uso de IA:** corresponde a la memoria final, no a esta entrega.
- **Capítulos 4 a 7** (Metodología, Implementación, Validación, Conclusiones):
  entregas posteriores. El apartado 3.7 define el diseño de la evaluación; los
  resultados van en el capítulo de validación.
