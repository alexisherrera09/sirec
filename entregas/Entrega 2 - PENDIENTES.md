# Entrega 2 — Pendientes del equipo

> Estado tras aplicar la retroalimentación del profesor (`Entrega 2 comentarios.txt`)
> sobre la plantilla oficial de UNIR. El documento a entregar es
> **`Entrega 2 Final.docx`**; el anterior (`Entrega 2 - SIREC (Desarrollo conceptual
> Design Thinking).docx`) queda como histórico.
> Última actualización: 2026-08-06.
>
> Los 15 señalamientos del profesor quedaron atendidos. Lo que sigue son los seis
> puntos que **no se pudieron cerrar** desde la generación del documento: tres
> requieren Word o al equipo, dos son decisiones de criterio y uno es una
> verificación bibliográfica. La trazabilidad completa está en
> `Entrega 2 - PLAN DE CORRECCIONES.md`.

---

## Pendientes activos, por orden de importancia

### 1. Métricas de los dos antecedentes latinoamericanos (3.3.2)
- **Qué falta:** el estado del arte no reporta el **tamaño del dataset ni los
  resultados numéricos** de Paltin et al. (2025) y de Franco Cantos (2024). En la
  tabla 4 y en el texto aparece «tamaño no reportado en la fuente consultada».
- **Por qué está así:** no se pudieron verificar esas cifras en la fuente, y la
  regla del proyecto es no inventar datos. Los otros cuatro trabajos sí llevan
  cifras (7 200 términos de CrisisLex; 166 100 y 141 500 mensajes de CrisisBench).
- **Qué hacer:** que alguien lea las dos fuentes y complete, por cada una, tamaño
  de muestra, procedimiento de etiquetado y métricas obtenidas. Es lo único que un
  lector exigente puede señalar como incompleto en ese apartado.
- **Responsable:** _______________  ·  **Estado:** ⏳ pendiente

### 2. Actualizar el índice en Word
- **Qué falta:** abrir `Entrega 2 Final.docx` y actualizar el índice de contenidos
  (clic derecho › Actualizar campos, o F9). El documento trae la marca
  `updateFields`, así que Word suele ofrecerlo al abrir.
- **Por qué importa:** el profesor pidió que la numeración jerárquica apareciera
  **también en el índice**. Hasta que no se actualice el campo, el índice no la
  muestra. `python-docx` no puede calcular números de página.
- **Responsable:** _______________  ·  **Estado:** ⏳ pendiente

### 3. Confirmar el conteo de páginas en Word
- **Qué falta:** verificar que el desarrollo (capítulos 1 a 3, sin portada, índice
  ni anexos) queda entre 20 y 30 páginas.
- **Medición actual:** **30 páginas** con LibreOffice (páginas 4 a 33 del PDF de
  vista previa). Word puede variar en ±1.
- **Si se pasa de 30:** hay margen de recorte en 3.3 y 3.7 sin tocar los mínimos
  que exige el profesor (3-5 páginas de fundamento teórico, 3-4 de estado del arte).
- **Responsable:** _______________  ·  **Estado:** ⏳ pendiente

### 4. Validar los umbrales del apartado 3.7
- **Qué falta:** que los tres integrantes revisen la tabla 8 y confirmen que los
  ocho umbrales son alcanzables: F1 macro ≥ 0.75 (temática) y ≥ 0.70 (urgencia),
  exhaustividad ≥ 0.90 en persona en riesgo y en urgencia alta, 0 falsos negativos
  graves, kappa ≥ 0.60, latencia p95 ≤ 3 s y ≤ 15 % de reportes en la clase «otro».
- **Por qué importa:** son compromisos evaluables. Si alguno se considera
  inalcanzable, hay que ajustarlo **antes** de entregar, no después de medir.
- **Responsable:** _______________  ·  **Estado:** ⏳ pendiente

### 5. Dos decisiones de criterio
- **a) Sombreado del encabezado de las tablas.** Las tablas usan la rejilla y la
  tipografía de la plantilla (Calibri 9–9,5 pt, permitido por el apartado 1.3 de
  `instrucciones.pdf`), pero el **fondo azul claro del encabezado es una decisión
  propia**, no viene de la plantilla. Si el equipo o el profesor lo consideran una
  desviación, se quita cambiando una línea en `build/doc_builder.py`.
- **b) Enunciado del propósito general en la introducción.** El profesor pidió
  «presentar de manera general lo que se pretende lograr». Hoy eso está repartido
  entre 1.3 (justificación), 1.4 (alcance) y el capítulo 2, pero no hay una frase
  que lo enuncie como tal en la introducción. Decidir si se añade.
- **Responsable:** _______________  ·  **Estado:** ⏳ pendiente

### 6. Capturas reales del sistema (opcional)
- **Qué falta:** las figuras 2 y 3 son wireframes propios. Como SIREC ya está
  desplegado, podrían sustituirse por capturas reales del formulario y del panel.
- **Nota:** no es requisito; los wireframes cumplen lo que pidió el profesor.
- **Estado:** ⏳ opcional

---

## Atendido de forma parcial (declarado en el documento)

- **Funcionamiento institucional sin fuente documental.** Las afirmaciones sobre
  cómo se determina hoy la urgencia se sustentan en las dos visitas de campo del
  equipo, no en un informe oficial (no existe público). Queda declarado como
  limitación metodológica en 3.1.2.
- **Longitud de los párrafos.** El profesor pidió 5–8 renglones y dividir los que
  pasen de 10–12. Hoy hay 84 párrafos en 5–8 renglones, 26 más cortos y **6 de
  unos 9 renglones**; ninguno supera los 10.

---

## Resuelto (2026-08-06)

Los 15 señalamientos del profesor:

- ✅ **Plantilla oficial de UNIR.** El documento se genera sobre `plantilla.docx`:
  portada, A4, márgenes 3/2/2,5/2,5 cm, Calibri 12, interlineado 1,5, encabezado
  con los tres integrantes y el título, pie con número de página.
- ✅ **Título con la sigla definida.** «Sistema Inteligente de Reportes de
  Emergencia Ciudadana (SIREC): clasificación y priorización automática…», y la
  sigla se define además en su primera aparición del cuerpo, en el apartado 1.4.
- ✅ **Extensión.** De ~9 páginas a **30 de desarrollo**, dentro del rango 20–30.
- ✅ **Numeración jerárquica** (1., 1.1, 3.1.1) en el cuerpo. La plantilla traía
  viñeta en el segundo nivel; se corrigió la numeración multinivel conservando su
  tipografía.
- ✅ **Cada capítulo y anexo en página nueva**, y ningún título pegado a otro (0 casos).
- ✅ **Párrafos divididos**: ninguno supera las 120 palabras (~10 renglones).
- ✅ **Introducción de 3 páginas** con estadísticas oficiales citadas: Cenapred
  (2024) y datos abiertos del 9-1-1 (Centro Nacional de Información, 2025 y 2026).
- ✅ **Objetivo general medible** (qué, con qué IA, qué resultado y cómo se mide) y
  seis objetivos específicos encadenados a él.
- ✅ **Fundamento teórico (3.3.1)** en ~4 páginas de prosa con citas, cubriendo los
  14 conceptos que pidió el profesor.
- ✅ **Estado del arte (3.3.2)** con 6 trabajos y ficha por trabajo; tabla
  comparativa al final como síntesis y cierre con la brecha (véase el pendiente 1).
- ✅ **Viñetas convertidas a prosa** en hallazgos, enunciados HMW, fundamento
  teórico y módulos del prototipo: de 52 a 29 párrafos en lista.
- ✅ **12 tablas** con «Tabla N. Título», fuente, numeración consecutiva, llamada
  desde el texto e interpretación posterior.
- ✅ **Matriz de selección explicada**: criterios, pesos, escala, quién valoró
  (consenso de los tres integrantes) y con qué evidencia.
- ✅ **Prototipo visual**: figura 1 (arquitectura con entradas, salidas y
  conexiones), figuras 2 y 3 (formulario y panel), y el apartado 3.5.3 explica cómo
  se presentan prioridad, confianza, errores y revisión humana.
- ✅ **Apartado 3.7 nuevo**: protocolo comparativo TF-IDF frente a BETO con las
  mismas particiones y semilla fija, métricas por clase y macro, matriz de
  confusión, falsos negativos críticos, kappa, latencia y criterios mínimos de
  éxito con umbrales.
- ✅ **Referencias: de 7 a 29**, todas verificadas, todas citadas y sin citas
  huérfanas (comprobado con `build/auditar.py`).
- ✅ **Anexos A y B** con el instrumento de la encuesta, los resultados agregados,
  el mapa de empatía y el criterio operativo de urgencia.

## Recordatorio (no es de esta entrega)

- **Declaración de uso de IA:** corresponde a la memoria final.
- **Capítulos 4 a 7** (Metodología, Implementación, Validación, Conclusiones): en
  entregas posteriores. El apartado 3.7 define el diseño de la evaluación; los
  resultados van en el capítulo de validación.
