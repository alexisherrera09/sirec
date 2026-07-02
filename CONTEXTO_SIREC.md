# SIREC — Contexto maestro del proyecto

> Documento de contexto para cualquier colaborador (humano o IA) que trabaje en este proyecto.
> Resume qué es SIREC, por qué importa, todas las decisiones acordadas, lo que DEBE hacerse,
> lo que NO debe hacerse, y la retroalimentación oficial del evaluador.
> Acompaña a: `PLAN_SIREC_ClaudeCode_total.md`, `PLAN_SIREC_AWS_Despliegue.md`, `PLAN_SIREC_tareas_humanas.md`.

---

## 1. Qué es SIREC

**SIREC — Sistema Inteligente de Reportes de Emergencia Ciudadana.**

Título formal: *"SIREC: clasificación y priorización inteligente de reportes ciudadanos de emergencia"*.

Es una plataforma web que aplica procesamiento del lenguaje natural (PLN) y aprendizaje automático para **clasificar y priorizar automáticamente** los reportes ciudadanos de emergencia que recibe una coordinación municipal de protección civil. Cada reporte escrito en lenguaje natural recibe, en el instante en que ingresa, dos etiquetas: una **categoría temática** (7 posibles) y un **nivel de urgencia** (alta, media, baja). Los reportes se presentan al operador en un panel ordenado por prioridad: lo más peligroso siempre aparece primero, sin importar el orden de llegada.

## 2. Contexto académico

- **Programa:** Maestría en Inteligencia Artificial, UNIR.
- **Asignatura:** Seminario de IA (trabajo de innovación / titulación aplicada).
- **Líneas de trabajo cubiertas:** Línea 3 (Aprendizaje automático) y Línea 5 (Procesamiento del lenguaje natural).
- **Equipo:** 3 integrantes, todos programadores.
- **Plazo:** aproximadamente 2 meses (8 semanas) para el desarrollo.
- **Estado:** la propuesta (formulario) fue entregada, revisada y **aprobada** por el profesor con retroalimentación específica (ver sección 6).
- El desarrollo del código lo realizará Claude Code (modelo Sonnet) en VS Code, siguiendo los planes; el equipo humano realiza las tareas no delegables (corpus real, doble etiquetado, validación, memoria, defensa).

## 3. Importancia para la sociedad

Durante contingencias (inundaciones, nortes, deslaves — frecuentes en Veracruz, México, uno de los estados con más declaratorias de emergencia por fenómenos hidrometeorológicos), las coordinaciones de protección civil reciben decenas o cientos de reportes ciudadanos en texto libre por múltiples vías. Hoy, un operador humano debe **leerlos uno por uno** para decidir qué es urgente y a qué área corresponde. Ese triaje manual es lento y propenso a errores justo cuando cada minuto cuesta: un reporte crítico ("hay una persona atrapada, el agua subió un metro") puede quedar esperando detrás de reportes menores.

SIREC convierte esa bandeja caótica en una **lista de prioridades en segundos**, para que la ayuda llegue primero a donde más urge. El sistema no sustituye el criterio humano: le quita al operador la carga de leer y ordenar, y le deja lo que solo un humano debe hacer — decidir y despachar. El valor es medible (tiempo de triaje manual vs. automático; métricas del modelo) y la arquitectura es replicable en cualquier municipio hispanohablante sin reentrenar el modelo.

## 4. Decisiones de arquitectura y alcance (ACORDADAS, no reabrir sin razón)

| Decisión | Valor acordado |
|---|---|
| Alcance del caso de uso | Prueba de concepto para **una coordinación municipal** (un municipio como caso de estudio); adopción gubernamental real fuera de alcance |
| Categorías temáticas | **7 fijas:** `inundacion`, `persona_en_riesgo`, `caida_poste_cable`, `deslave`, `incendio`, `dano_estructural`, `otro` |
| Niveles de urgencia | **3 fijos:** `alta`, `media`, `baja` |
| Modelo de IA principal | **BETO** (`dccuchile/bert-base-spanish-wwm-cased`), fine-tuning con corpus propio |
| Baseline (obligatorio) | TF-IDF + regresión logística y/o SVM (scikit-learn); solo para comparación, NO se despliega |
| Backend principal | **.NET 8 (ASP.NET Core, C#)** — API REST, PostgreSQL vía Entity Framework Core, autenticación JWT, panel |
| Modelo servido como | **Microservicio Python (FastAPI)** independiente; el backend .NET lo consume por HTTP local. Arranca en **modo simulado** (reglas por palabras clave) y luego se conecta BETO real, sin cambiar el contrato |
| Frontend | **React** separado (Vite), consume la API .NET. Dos vistas: formulario público (sin registro) y panel del operador (con login) |
| Base de datos | **PostgreSQL** (en local vía Docker; en producción instalada en la instancia) |
| Despliegue local | Todo por `localhost` y puertos directos (8000 Python, 5000 .NET, 5173 React, 5432 BD). Sin Nginx ni HTTPS en local |
| Despliegue producción | **Frontend en S3** (sitio estático, CloudFront recomendado para HTTPS). **Backend + microservicio + PostgreSQL en UNA instancia EC2** (t3.small/medium), servicios bajo **systemd**, **Nginx** como proxy inverso solo para la API, HTTPS con Certbot. **Sin Docker en producción** |
| Entrenamiento | Entornos gratuitos (Google Colab si no hay GPU local) |
| Canales de entrada | Solo el formulario web en este proyecto; la arquitectura desacoplada deja WhatsApp/Telegram/redes como trabajo futuro |
| Orden de trabajo | Local primero (checkpoints por fase) → modelo real integrado → solo entonces AWS |

## 5. Estado del arte y novedad (con referencias verificadas)

Existen antecedentes latinoamericanos, y el proyecto se posiciona frente a ellos (no se presenta como si no existiera nada):

- **Paltin, D., Mejía, J., Orellana, M., & Zambrano-Martínez, J. (2025).** Modelado semántico de emergencias del ECU 911 con NLP y ontologías. *Revista Tecnológica ESPOL, 37*(E1), 112-125. https://doi.org/10.37815/rte.v37nE1.1351 — Enfoque ontológico (OWL/SWRL/Prolog) sobre llamadas al 911 ecuatoriano; paradigma distinto al de SIREC.
- **Franco Cantos, J. H. (2024).** *Identificación automática de tweets de emergencia en la red social "X": caso de estudio en Ecuador* [Tesis de maestría, Pontificia Universidad Católica del Ecuador]. — Clasificación BINARIA con modelos clásicos; recomienda transformers como trabajo futuro (SIREC hace exactamente eso).

**La novedad de SIREC es la combinación** que ningún antecedente reúne: (1) doble clasificación simultánea tema + urgencia, (2) español de México, (3) modelo transformer (BETO) con corpus propio, (4) sistema desplegado en producción con panel operativo. No se afirma que "no existe nada parecido": se afirma que no se ha identificado una herramienta equivalente de acceso público con esta combinación.

## 6. Retroalimentación oficial del profesor (Efrén Juárez) — REQUISITOS DE CALIFICACIÓN

La propuesta fue evaluada positivamente ("muy sólida", "viable y bien encaminada", "puede ser un trabajo de titulación aplicado con bastante fuerza"). El profesor exigió cuidar estos puntos, que son **obligatorios para la calificación final**:

1. **Precisar el conjunto de categorías** → resuelto: 7 categorías fijas, documentarlas tal cual en la memoria.
2. **Precisar el origen de los reportes** → el corpus debe tener trazabilidad cuantificada (tabla: % real / % redactado / % sintético declarado).
3. **Precisar el procedimiento de etiquetado** → guía de etiquetado formal + muestra doblemente etiquetada por DOS humanos + **kappa de Cohen reportado**.
4. **Definir el criterio de urgencia** → explícito, con ejemplos de frontera, en la guía de etiquetado.
5. **Baseline claro + métricas por clase + falsos negativos** → el modelo clásico es requisito (no opcional); reportar precisión/recall/F1 POR CLASE; **priorizar recall porque en emergencias los falsos negativos son más graves que otros errores** (especialmente en `persona_en_riesgo` y `urgencia=alta`).

## 7. Lo que SÍ debe hacerse (compromisos)

- Seguir los planes fase por fase, verificando cada CHECKPOINT antes de avanzar.
- Todo el stack con herramientas **gratuitas y de código abierto**. Costo por predicción: cero.
- Conjunto de prueba del modelo **100% real/humano** (nunca sintético).
- Declarar explícitamente cualquier dato sintético generado con IA y su proporción.
- Documentar cada fase en la memoria **conforme avanza** (no al final).
- El equipo debe **leer y entender** el código generado: cada integrante domina un componente y puede defenderlo.
- Cumplir la normativa de UNIR sobre declaración de uso de IA en el trabajo.
- Configurar alarma de presupuesto AWS ($5 USD) antes de crear recursos; apagar la instancia cuando no se use.
- Checklist de seguridad antes de la entrega: PostgreSQL, puerto 8000 y puerto 5000 jamás expuestos a internet; HTTPS válido; CORS restringido; credenciales de producción distintas a las de desarrollo y fuera del repositorio.

## 8. Lo que NO debe hacerse (prohibiciones acordadas)

- **NO usar servicios de IA de pago** (ChatGPT, Claude API, Gemini) en el sistema en producción. El mérito académico está en el clasificador propio.
- **NO usar Amazon Comprehend** ni servicios administrados de clasificación: convertirían el trabajo en "consumir una API".
- **NO evaluar el modelo sobre datos sintéticos** ni ocultar el origen de los datos.
- **NO simular el kappa de Cohen**: el doble etiquetado lo hacen dos personas reales, de forma independiente. Una IA etiquetando no cuenta como "acuerdo entre anotadores".
- **NO inventar citas, autores, páginas ni URLs.** Solo se citan fuentes verificadas (las de la sección 5 lo están).
- **NO afirmar que "no existe nada parecido"**: la novedad se defiende como combinación específica frente a antecedentes reconocidos.
- **NO desplegar en AWS antes de que todo funcione en local** con el modelo real integrado.
- **NO exponer a internet** PostgreSQL (5432), el microservicio Python (8000) ni el backend directo (5000); solo Nginx con HTTPS al frente.
- **NO cambiar el contrato de datos** (categorías, urgencias, formato de la API de clasificación) sin actualizarlo en TODOS los componentes a la vez.
- **NO saltarse checkpoints** ni avanzar de fase con un checkpoint fallando.
- **NO dejar la memoria escrita para el final**: es donde se gana la calificación.

## 9. Documentos del proyecto y su función

| Documento | Función |
|---|---|
| `PLAN_SIREC_ClaudeCode_total.md` | Plan de implementación completo para Claude Code (Sonnet) en VS Code: contrato de datos, componentes A-D, fases y checkpoints, requisitos del evaluador integrados |
| `PLAN_SIREC_AWS_Despliegue.md` | Despliegue en producción: frontend en S3 (+CloudFront), backend/microservicio/BD en EC2, seguridad y verificación final. Solo tras validar local |
| `PLAN_SIREC_tareas_humanas.md` | Tareas no delegables del equipo y su momento exacto (6 momentos cronológicos) |
| `formulario_SIREC.docx` | Propuesta oficial entregada y aprobada (referencia) |
| Este documento | Contexto maestro: qué, por qué, decisiones, requisitos y límites |
