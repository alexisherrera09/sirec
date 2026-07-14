# Resultados del baseline (Fase D4) — SIREC

> Modelo de referencia OBLIGATORIO (TF-IDF + clasificador lineal) exigido por el evaluador,
> para comparar contra BETO (D5). **No se despliega.** Reproducible con `entrenar_baseline.py`.
> Corpus: 400 reportes reales (`origen=real`). Kappa (D3.4) **cerrado** — ver `reporte_kappa.md`.

## 0. Evaluación DEFINITIVA sobre el conjunto gold (test validado) — protocolo principal

Tras cerrar el kappa, la evaluación de referencia usa el **conjunto de prueba gold** de máxima validez:

- **Test = 180 reportes gold** (`gold_kappa.csv`): doblemente etiquetados por Ricardo y Nahum y
  **adjudicados por consenso** (tercer anotador). Es lo más cercano a "verdad" que tenemos.
- **Train = 220 reales restantes + 900 sintéticos** (declarados; los sintéticos solo entrenan).
- **Sin fuga:** los 180 gold se excluyen del entrenamiento. Reproducible: `entrenar_baseline.py --gold-test --con-sintetico`.

### Categoría (7 clases) — test gold

| Modelo | Accuracy | Macro-F1 | Recall `persona_en_riesgo` (crítica) | Falsos negativos crítica |
|---|---:|---:|---:|---:|
| Regresión Logística | 0.656 | 0.635 | 0.511 | 22 / 45 |
| **SVM lineal** | **0.672** | **0.648** | **0.578** | **19 / 45** |

F1 por clase (SVM): `incendio` 0.87, `deslave` 0.82, `inundacion` 0.79, `caida_poste_cable` 0.74,
`persona_en_riesgo` 0.59, `otro` 0.48, **`dano_estructural` 0.25** (solo 6 en el gold → clase frágil).

### Urgencia (3 clases) — test gold

| Modelo | Accuracy | Macro-F1 | Recall `alta` (crítica) | Falsos negativos `alta` |
|---|---:|---:|---:|---:|
| **Regresión Logística** | 0.661 | **0.445** | 0.583 | 20 / 48 |
| SVM lineal | 0.622 | 0.417 | 0.583 | 20 / 48 |

`media` es sólida (F1 0.76) pero **`baja` colapsa (recall 0.00, 14 casos)**: el modelo la absorbe en `media`.
Es honesto reportarlo — con tan pocos ejemplos de `baja` y su cercanía semántica con `media`, el modelo
léxico no la separa. Es justo el tipo de matiz donde BETO debería mejorar.

### Palanca de recall de `alta` sobre el gold (`optimizar_umbral_alta.py --gold-test`)

| Umbral P(alta) | Recall `alta` | Precisión `alta` | Falsos negativos | Macro-F1 |
|---|---:|---:|---:|---:|
| argmax (~0.50) | 0.583 | 0.571 | 20 / 48 | 0.445 |
| ≥ 0.35 | 0.604 | 0.468 | 19 / 48 | 0.414 |
| **≥ 0.30 (recomendado)** | **0.688** | 0.465 | **15 / 48** | 0.419 |
| ≥ 0.20 | 0.875 | 0.408 | 6 / 48 | 0.403 |

**Piso a superar por BETO (sobre el conjunto validado):** categoría macro-F1 ≈ **0.65** (recall
`persona_en_riesgo` **0.58**); urgencia macro-F1 ≈ **0.45**, recall `alta` **0.58** (0.69 con umbral 0.30).

> Nota de comparabilidad: estos números son **más bajos y más estrictos** que los del §1–§4 (5-fold CV
> sobre los 400 con etiqueta de un solo anotador), porque aquí (a) el test son etiquetas de consenso
> más exigentes y (b) los 180 mejores reportes salieron del entrenamiento. No es un retroceso del
> modelo: es una medición más honesta. **Estos son los números de referencia para la memoria.**

---

## Configuración final (tras optimización, ver §5)

- **Vectorización:** unión de TF-IDF de **palabra** (n-gramas 1–2, `min_df=2`, `max_features=20000`) +
  TF-IDF de **carácter** (`char_wb`, 3–5, `max_features=40000`); acentos normalizados, `sublinear_tf`.
  Los n-gramas de carácter fueron la mejora decisiva (ver §5).
- **Clasificadores:** Regresión Logística (`class_weight=balanced`, C=3) y SVM lineal (`class_weight=balanced`).
- **`class_weight=balanced`** por el fuerte desbalance del corpus real (ver `reporte_corpus.md`).
- **Evaluación primaria:** 5-fold CV estratificada sobre los 400 reales. **Secundaria:** holdout 75/25 con
  entrenamiento aumentado por 900 sintéticos (test 100% real). Semilla fija (42).
- Criterio del evaluador: prioridad a **recall** y **falsos negativos** de las clases críticas.

## 1. Categoría (7 clases) — 5-fold CV sobre real

| Modelo | Accuracy | Macro-F1 | Recall `persona_en_riesgo` (crítica) | Falsos negativos crítica |
|---|---:|---:|---:|---:|
| Regresión Logística | 0.730 | 0.713 | 0.607 | 35 / 89 |
| SVM lineal | 0.735 | **0.714** | 0.629 | 33 / 89 |

F1 por clase (SVM): `incendio` 0.88, `caida_poste_cable` 0.86, `deslave` 0.83, `inundacion` 0.78,
`persona_en_riesgo` 0.65, `otro` 0.62, **`dano_estructural` 0.38** (solo 11 muestras reales → clase frágil).

**Confusión dominante:** `persona_en_riesgo` ↔ `otro`. Aun así, con los n-gramas de carácter el recall de
la clase crítica subió de 0.55 a **0.63** (falsos negativos 40 → 33).

## 2. Urgencia (3 clases) — 5-fold CV sobre real

| Modelo | Accuracy | Macro-F1 | Recall `alta` (crítica) | Falsos negativos `alta` |
|---|---:|---:|---:|---:|
| Regresión Logística | 0.640 | **0.506** | 0.528 | 50 / 106 |
| SVM lineal | 0.635 | 0.501 | 0.509 | 52 / 106 |

Sigue siendo la tarea más difícil (la gravedad es semántica, no léxica). El recall de `alta` mejoró de
0.44 a **0.53**, pero aún se pierde ~la mitad de los urgentes en el modo por defecto → se corrige con umbral (§4).

## 3. Efecto del aumento con sintéticos (holdout, test 100% real)

Aumentar el entrenamiento con los 900 sintéticos ayuda a las clases críticas (se declara: los sintéticos
solo entran en entrenamiento; el test se mantiene 100% real):

| Tarea / métrica | Solo real (CV) | Real + sintético (holdout) |
|---|---:|---:|
| Categoría macro-F1 | 0.71 | 0.72 |
| `urgencia=alta` recall (LogReg) | 0.53 | **0.556** |
| Urgencia macro-F1 (LogReg) | 0.51 | 0.563 |

## 4. Optimización del recall de `urgencia=alta` (umbral) — `optimizar_umbral_alta.py`

En triage un FALSO NEGATIVO de `alta` es más grave que un falso positivo. Bajar el umbral de decisión de
`alta` (sobre palabra+carácter, LogReg, 5-fold CV) recorta los falsos negativos de la clase crítica:

| Umbral P(alta) | Recall `alta` | Precisión `alta` | Falsos negativos | Macro-F1 |
|---|---:|---:|---:|---:|
| argmax (~0.50) | 0.528 | 0.566 | 50 / 106 | 0.506 |
| ≥ 0.40 | 0.566 | 0.561 | 46 / 106 | **0.518** |
| **≥ 0.30 (recomendado)** | **0.708** | 0.469 | **31 / 106** | 0.474 |
| ≥ 0.25 | 0.783 | 0.441 | 23 / 106 | 0.469 |

**Punto de operación recomendado:** umbral ≈ **0.30** → recall `alta` **0.71**, falsos negativos **31 vs 59**
(casi la mitad respecto al baseline original), coherente con el principio rector de la guía (ante duda, sobre-alertar).

## 5. Qué se probó para mejorar y qué sobrevivió (honestidad metodológica)

Se hizo un barrido sistemático seleccionando por macro-F1 en 5-fold CV (nunca sobre el conjunto de prueba):

| Palanca probada | Resultado | ¿Se aplica? |
|---|---|---|
| **N-gramas de carácter (`char_wb` 3–5)** | Categoría 0.65→**0.71**, urgencia 0.46→**0.51**, recall crítico ↑ | ✅ **Sí** (mejora decisiva) |
| Umbral de decisión de `alta` | Recall `alta` 0.53→0.71 (compromiso con precisión) | ✅ Sí (perilla operativa, §4) |
| Aumento con sintéticos (solo train) | Ayuda a las clases críticas | ✅ Sí (opción `--con-sintetico`) |
| Normalización de "leetspeak" (`f4ll3c3`→`fallece`) | Urgencia +0.002 (ruido); **categoría −0.05** | ❌ No (los char n-gramas ya lo cubren y normalizar borra señal) |
| Quitar stopwords en español | Sin ganancia consistente | ❌ No |
| n-gramas de palabra (1,3) | Igual o peor, más features | ❌ No |
| Ajuste de C (5, 10), SGD | Dentro del ruido; C alto empeora urgencia | ❌ No (se deja C=3) |
| ComplementNB | Peor en ambas tareas | ❌ No |
| Ensemble soft-voting (LogReg+CNB+SVM) | No supera al modelo lineal simple | ❌ No |

**Lección:** con 400 muestras y un baseline lineal, la única mejora estructural real fue enriquecer las
**features** (carácter); apilar clasificadores o hiperparametrizar no aporta y solo añade riesgo de sobreajuste.

## 6. Conclusiones e implicaciones para BETO (D5)

- **Piso a superar por BETO (referencia definitiva, test gold, §0):** categoría macro-F1 ≈ **0.65**
  (recall `persona_en_riesgo` ≈ 0.58); urgencia macro-F1 ≈ **0.45** (recall `alta` ≈ 0.58 en modo
  normal, 0.69 con umbral 0.30). Los números de §1–§4 (CV, macro-F1 0.71 / 0.51) quedan como
  contexto metodológico, no como piso.
- **Objetivo prioritario:** subir el recall de `urgencia=alta` y `persona_en_riesgo` **sin** sacrificar
  la precisión que hoy exige el umbral, y **recuperar `urgencia=baja`** (hoy recall 0). La gravedad es
  semántica ("no responde", "sigue subiendo"), justo donde un transformer debería ganarle al modelo léxico.
- **`dano_estructural`** seguirá frágil por escasez de datos reales (6 en el gold); se reporta con
  honestidad y se apoya en aumento sintético + class weights.
- El baseline optimizado deja una comparación cuantitativa clara y un objetivo concreto para la memoria.

> Nota metodológica: los números de §0 son los **definitivos**, medidos sobre el conjunto de prueba
> gold validado por doble etiquetado + adjudicación (kappa cerrado, ver `reporte_kappa.md`). Las
> secciones §1–§4 documentan la exploración previa (5-fold CV sobre etiqueta de un solo anotador).
