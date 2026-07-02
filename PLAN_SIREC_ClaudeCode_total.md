# SIREC — Plan de implementación total para Claude Code

> **Instrucciones para ti, Claude (modelo Claude Fable 5), operando en Claude Code / VS Code.**
> Tú construirás TODO el código de este proyecto. El equipo humano solo interviene en los puntos marcados como [HUMANO], que son mínimos y no delegables.
> SIREC = Sistema Inteligente de Reportes de Emergencia Ciudadana: plataforma web que clasifica y prioriza automáticamente reportes ciudadanos de emergencia (español de México) para una coordinación municipal de protección civil.

---

## 0. CÓMO DEBES TRABAJAR (léelo antes de escribir código)

- Trabaja **una fase a la vez**, en el orden de la sección 8. Al final de cada fase hay un **CHECKPOINT**: ejecútalo tú mismo, verifica el resultado esperado y repórtalo antes de continuar. No avances con checkpoints fallando.
- Todo debe funcionar **en local primero**. El despliegue en AWS tiene su propio documento (`PLAN_SIREC_AWS_Despliegue.md`); no lo ejecutes hasta que el checkpoint final local pase.
- En local NO uses Nginx ni HTTPS. Comunicación directa por `localhost`.
- Crea cada componente en su propia carpeta: `/microservicio-ml`, `/backend-api`, `/frontend`, `/datos-modelo`.
- Cada componente con su README de arranque y sus dependencias declaradas (`requirements.txt`, `.csproj`, `package.json`).
- Configuración sensible (cadenas de conexión, URLs entre servicios, secreto JWT) SIEMPRE en variables de entorno o archivos de configuración de desarrollo, nunca en el código.
- Comentarios y mensajes en español; nombres de variables según la convención del lenguaje.
- Genera pruebas automatizadas básicas donde el plan lo indique.

### Requisitos del evaluador académico (OBLIGATORIOS, afectan la calificación)

El proyecto fue aprobado por el profesor con cinco exigencias que este plan integra. Cuando construyas el componente de datos y evaluación (sección 7), estos puntos son innegociables:

1. Categorías precisas y fijas (resuelto: sección 1.1).
2. Origen de los reportes del corpus documentado y cuantificado (tabla de proporciones: real / redactado / sintético).
3. Procedimiento de etiquetado documentado, con acuerdo entre anotadores (kappa de Cohen) medido sobre una muestra doblemente etiquetada por humanos.
4. Criterio de urgencia explícito, con ejemplos de frontera, en una guía de etiquetado formal.
5. Baseline obligatorio (TF-IDF + regresión logística/SVM) + métricas POR CLASE + énfasis en recall/falsos negativos de las clases críticas (`persona_en_riesgo`, `urgencia=alta`).

### Puertos fijos en local

| Servicio | Puerto | URL base |
|---|---|---|
| Microservicio Python (FastAPI) | 8000 | http://localhost:8000 |
| Backend .NET (API) | 5000 | http://localhost:5000 |
| Frontend React (Vite) | 5173 | http://localhost:5173 |
| PostgreSQL | 5432 | localhost:5432 |

### Requisitos de la máquina (verifícalos tú al inicio; si falta algo, indícalo)

.NET 8 SDK · Node.js 20+ · Python 3.11+ · Docker (solo para PostgreSQL local) · Git

---

## 1. CONTRATO DE DATOS COMPARTIDO (FUENTE ÚNICA DE VERDAD)

Estos valores son compartidos por todos los componentes. Defínelos una sola vez por componente (constantes/enums) y no permitas que diverjan.

### 1.1 Categorías temáticas (7, fijas)

| Valor interno | Etiqueta visible |
|---|---|
| `inundacion` | Inundación |
| `persona_en_riesgo` | Persona en riesgo |
| `caida_poste_cable` | Caída de poste o cable |
| `deslave` | Deslave |
| `incendio` | Incendio |
| `dano_estructural` | Daño estructural |
| `otro` | Otro |

### 1.2 Niveles de urgencia (3, fijos)

| Valor interno | Etiqueta visible | Orden de prioridad |
|---|---|---|
| `alta` | Alta | 1 (primero) |
| `media` | Media | 2 |
| `baja` | Baja | 3 (último) |

### 1.3 Contrato de la API de clasificación (.NET → Python)

```
POST http://localhost:8000/clasificar
{ "texto": "Se está metiendo el agua a mi casa en Las Brisas" }

Respuesta:
{
  "categoria": "inundacion",
  "urgencia": "alta",
  "confianza_categoria": 0.94,
  "confianza_urgencia": 0.88
}
```

Reglas: `categoria` ∈ los 7 valores; `urgencia` ∈ los 3 valores; confianzas en [0.0, 1.0]; texto vacío/ inválido → HTTP 422.

### 1.4 Modelo de datos del reporte (PostgreSQL)

| Campo | Tipo | Notas |
|---|---|---|
| `id` | UUID | PK |
| `texto` | text | Reporte original |
| `colonia` | text NULL | Opcional |
| `telefono` | text NULL | Opcional |
| `categoria` | varchar | 7 valores |
| `urgencia` | varchar | 3 valores |
| `confianza_categoria` | float | [0,1] |
| `confianza_urgencia` | float | [0,1] |
| `estado` | varchar | `pendiente` / `en_atencion` / `atendido` |
| `creado_en` | timestamptz | Auto |

---

## 2. COMPONENTE A — Microservicio de clasificación (Python + FastAPI)

Carpeta: `/microservicio-ml`. **Constrúyelo primero.**

### Fase A1 — Modo simulado
Construye:
- FastAPI con `POST /clasificar` (contrato 1.3) y `GET /salud` → `{"estado":"ok","modo":"simulado"}`.
- Clasificación simulada por palabras clave (ej.: "inund"/"agua" → `inundacion`; "atrapad"/"herid" → `persona_en_riesgo`+`alta`; "poste"/"cable" → `caida_poste_cable`; sin coincidencia → `otro`+`media`). Confianzas fijas plausibles (0.9).
- Validación: texto vacío → 422. Pruebas con pytest para el endpoint (mínimo: caso válido, caso vacío, verificación de que categoría/urgencia pertenecen a los valores permitidos).
- `requirements.txt` y README.

**CHECKPOINT A1 (ejecútalo tú):**
```
uvicorn main:app --port 8000 &
curl http://localhost:8000/salud                     → {"estado":"ok","modo":"simulado"}
curl -X POST .../clasificar con "se inundó la calle" → categoria=inundacion
pytest                                               → todas las pruebas pasan
```

### Fase A2 — Modelo real (se ejecuta al final, cuando exista el modelo de la sección 7)
- Carga el modelo BETO ajustado desde `/datos-modelo/modelo_exportado/`.
- Sustituye las reglas por inferencia real. El contrato 1.3 NO cambia.
- `GET /salud` → `{"modo":"modelo"}`. Implementa una variable de entorno `MODO` (`simulado`/`modelo`) para poder alternar.

**CHECKPOINT A2:** mismas llamadas que A1 con `modo=modelo`; clasificaciones provienen del modelo.

---

## 3. COMPONENTE B — Backend .NET 8 (ASP.NET Core, C#)

Carpeta: `/backend-api`. Constrúyelo con A corriendo en modo simulado.

### Fase B1 — Base de datos y esqueleto
- Web API .NET 8 en puerto 5000. Levanta PostgreSQL local con: `docker run --name sirec-db -e POSTGRES_PASSWORD=sirec -e POSTGRES_DB=sirec -p 5432:5432 -d postgres:16`
- EF Core + Npgsql. Entidad `Reporte` (1.4). Migración inicial aplicada.

**CHECKPOINT B1:** `dotnet run` levanta sin errores; la tabla existe (verifícalo con una consulta).

### Fase B2 — Endpoint público
- `POST /api/reportes` `{texto, colonia?, telefono?}` → llama al microservicio (URL en configuración) → guarda con estado `pendiente` → devuelve el reporte.
- Resiliencia: si el microservicio no responde, guarda con `otro`/`media`, marca `requiere_revision=true` (agrega el campo) y registra el fallo en logs. Nunca pierdas un reporte.

**CHECKPOINT B2:** `curl` con "hay una persona atrapada en el segundo piso" → reporte creado con `persona_en_riesgo`/`alta`. Prueba también apagando el microservicio: el reporte se guarda igual con el fallback.

### Fase B3 — Endpoints del panel
- `GET /api/reportes` ordenado por urgencia (alta→media→baja) y fecha descendente; filtros `?categoria=` y `?estado=`.
- `PATCH /api/reportes/{id}/estado` (`pendiente`→`en_atencion`→`atendido`; rechaza transiciones inválidas).
- `GET /api/reportes/resumen` → contadores {alta, media, baja, total_hoy}.

**CHECKPOINT B3:** las tres rutas responden con datos coherentes con lo insertado en B2.

### Fase B4 — Autenticación JWT
- `POST /api/auth/login` (usuario/contraseña de operador desde configuración) → token JWT.
- Endpoints del panel (B3) protegidos; `POST /api/reportes` queda público.

**CHECKPOINT B4:** sin token → 401; con token → 200.

### Fase B5 — CORS
- Permite origen `http://localhost:5173`.

**CHECKPOINT B5:** una petición desde el frontend no produce error de CORS.

---

## 4. COMPONENTE C — Frontend React

Carpeta: `/frontend`. Vite + React. La URL de la API va en `VITE_API_URL` (no fija en el código).

### Fase C1 — Formulario público
- Página pública responsiva (móvil primero): textarea grande "Describe tu emergencia", campos opcionales colonia y teléfono, botón enviar → `POST /api/reportes` → confirmación visible. Sin registro ni pasos extra.

**CHECKPOINT C1:** `npm run dev`, envía un reporte desde el navegador y verifica que aparece vía `GET /api/reportes`.

### Fase C2 — Panel del operador
- Login contra `/api/auth/login`; guarda el token en memoria.
- Tarjetas de reportes ordenadas por urgencia con color (rojo=alta, ámbar=media, verde=baja): texto, categoría, urgencia, confianza, tiempo transcurrido, estado.
- Contadores superiores desde `/resumen`. Filtro por categoría. Botones de cambio de estado. Polling cada 10–15 s.

**CHECKPOINT C2 — extremo a extremo local (el más importante):**
```
Con A(:8000), B(:5000) y C(:5173) corriendo:
1. Enviar desde el formulario: "se cayó un poste con cables en la avenida"
2. Login en el panel → el reporte aparece como caida_poste_cable, priorizado
3. Cambiar estado a en_atencion → se actualiza
```

---

## 5. COMPONENTE D — Datos, entrenamiento y evaluación

Carpeta: `/datos-modelo`. **Tú (Claude Code) construyes toda la tubería; el equipo humano solo hace lo marcado [HUMANO].** Este componente materializa los requisitos del evaluador (sección 0).

### Fase D1 — Guía de etiquetado (tú la redactas; el equipo la valida)
Genera `guia_etiquetado.md` con:
- Definición operativa de cada una de las 7 categorías con 3 ejemplos cada una.
- **Criterio de urgencia explícito**: señales textuales que determinan `alta` (vidas en riesgo: personas atrapadas, heridas, arrastradas; fuego activo con personas cerca; cables energizados en vía transitada), `media` (daño material en curso sin personas afectadas; riesgo potencial), `baja` (situación controlada, informativa o de daño menor).
- Mínimo 5 casos de frontera resueltos y justificados (ej.: inundación sin personas pero junto a escuela en horario de clases → `alta` por exposición previsible).
- [HUMANO] El equipo lee y aprueba la guía (o pide ajustes) antes de la Fase D3.

### Fase D2 — Herramienta de etiquetado (tú la construyes)
Construye una mini‑aplicación local de etiquetado (puede ser una página HTML+JS servida localmente o una TUI en Python) que:
- Lea un CSV de reportes sin etiquetar y muestre uno por uno con botones para categoría y urgencia.
- Guarde el resultado en `corpus_etiquetado.csv` (columnas: texto, categoria, urgencia, etiquetador, origen).
- Soporte "modo doble etiquetado": el mismo subconjunto presentado a dos etiquetadores distintos, guardando ambas respuestas por separado.
Objetivo: que el trabajo humano de etiquetar tome horas, no días.

### Fase D3 — Construcción del corpus (mixta)
1. **Tú generas** `corpus_sintetico.csv`: ~800–1,000 reportes sintéticos variados en español de México (regístralos con `origen=sintetico`). Varía registro (formal/coloquial), errores de tecleo, longitud, colonias ficticias. Distribúyelos entre las 7 categorías y 3 urgencias siguiendo la guía D1, con especial cobertura de `persona_en_riesgo`.
2. [HUMANO] El equipo recolecta ~300–400 reportes REALES (redes sociales de contingencias pasadas, notas de prensa, transcripciones), los anonimiza y los etiqueta con tu herramienta (D2), con `origen=real`. **El conjunto de prueba se formará exclusivamente de estos** (regla innegociable: nunca evaluar sobre datos sintéticos).
3. [HUMANO] Dos personas etiquetan de forma independiente una muestra de ~150–200 reportes reales usando el modo doble de la herramienta (necesario para el kappa; no puede hacerlo la IA).
4. **Tú generas** `reporte_corpus.md`: tabla de origen cuantificado (% real / % sintético), distribución por clase, y el **kappa de Cohen** calculado sobre la muestra doble, con interpretación. Script: `calcular_kappa.py`.

### Fase D4 — Baseline (obligatorio, tú lo haces completo)
- `entrenar_baseline.py`: TF-IDF + regresión logística y SVM (scikit-learn), mismas particiones que usará BETO (train/val con estratificación; **test solo con datos reales**).
- Reporta métricas POR CLASE (precisión, recall, F1 para cada categoría y cada urgencia) y matrices de confusión. Exporta `resultados_baseline.md` con tablas.

### Fase D5 — Fine-tuning de BETO (tú lo haces completo)
- `entrenar_beto.py`: fine-tuning de `dccuchile/bert-base-spanish-wwm-cased` (BETO) para las dos tareas (categoría y urgencia; dos cabezas o dos modelos, justifica la elección en comentarios).
- Si la máquina local no tiene GPU, genera también un notebook `entrenar_beto_colab.ipynb` listo para Google Colab, y documenta cómo bajar el modelo resultante a `/datos-modelo/modelo_exportado/`.
- Evaluación con métricas POR CLASE + matriz de confusión + **análisis explícito de falsos negativos de `persona_en_riesgo` y `urgencia=alta`** (requisito del evaluador). Si el recall de las clases críticas es bajo, aplica mitigación (ponderación de clases o ajuste de umbral) y documenta el antes/después.
- Genera `comparacion_modelos.md`: tabla lado a lado baseline vs. BETO (accuracy, F1 macro, recall de clases críticas) con conclusión.

### Fase D6 — Exportación e integración
- Exporta el modelo a `/datos-modelo/modelo_exportado/` en formato cargable por el microservicio (Transformers `save_pretrained`).
- Ejecuta la Fase A2 (integración) y su checkpoint.

**CHECKPOINT D:** `comparacion_modelos.md` existe con métricas por clase; kappa reportado; BETO supera al baseline en F1 macro y en recall de clases críticas; CHECKPOINT A2 pasa.

---

## 6. LO MÍNIMO NO DELEGABLE DEL EQUIPO HUMANO (resumen)

Por exigencia del evaluador y por honestidad metodológica, SOLO estas tareas no puede hacerlas la IA:
1. Recolectar y etiquetar los ~300–400 reportes reales (con la herramienta que tú construyes en D2; son pocas horas).
2. El doble etiquetado de la muestra de ~150–200 para el kappa (dos personas, de forma independiente).
3. Aprobar la guía de etiquetado (D1) y revisar/entender el código y resultados para poder defenderlos ante el tribunal.

Todo lo demás —código, scripts, corpus sintético, entrenamiento, evaluación, documentación técnica— lo haces tú.

---

## 7. ORDEN DE EJECUCIÓN GLOBAL

1. Componente A, Fase A1 (simulado) → CHECKPOINT A1.
2. Componente B, Fases B1→B5 → checkpoints.
3. Componente C, Fases C1→C2 → CHECKPOINT C2 (extremo a extremo con simulado).
4. Componente D, Fases D1→D2 (guía + herramienta) → [HUMANO] etiquetado real en paralelo.
5. Componente D, Fases D3→D6 → CHECKPOINT D (incluye A2: modelo real integrado).
6. Repetir la prueba de extremo a extremo con el modelo real.
7. Solo entonces: despliegue con `PLAN_SIREC_AWS_Despliegue.md` (frontend en S3; backend, microservicio y PostgreSQL en EC2).

---

## 8. NOTA DE MODELO Y USO EN CLAUDE CODE

- Este plan está pensado para ejecutarse con **Claude Sonnet** (`claude-sonnet-4-6`) en Claude Code dentro de VS Code; selecciona ese modelo en la configuración si no está activo. El plan funciona igual con cualquier modelo Claude reciente: lo importante es seguir las fases y checkpoints en orden.
- Forma de trabajo recomendada para el humano: abrir Claude Code en la carpeta raíz del proyecto, entregar este documento y pedir literalmente: *"Lee PLAN_SIREC_ClaudeCode_total.md y ejecuta la Fase A1. Reporta el resultado del CHECKPOINT A1 antes de continuar."* Y así, fase por fase.
- Tú (Claude Code) debes anunciar al final de cada fase: qué construiste, el resultado del checkpoint, y qué fase sigue.
- Las tareas humanas y sus momentos están en el documento `PLAN_SIREC_tareas_humanas.md`; cuando llegues a un punto marcado [HUMANO], detente e indica al equipo qué les toca hacer antes de continuar.
