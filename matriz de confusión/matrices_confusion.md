# Matrices de confusión — SIREC

> Generado automáticamente por `generar_matrices.py`.
> Conjunto de prueba: **180 reportes reales** del gold adjudicado por consenso
> (`datos-modelo/gold_kappa.csv`). Entrenamiento: 1120 ejemplos
> (reales restantes + sintéticos declarados). Sin fuga: el gold nunca se usó para entrenar.

Cubre el objetivo específico 5 del documento académico: *"métricas por clase
(precisión, exhaustividad y medida F1) y matriz de confusión"*.

**Cómo leer las matrices:** las **filas** son la clase real (etiqueta de consenso
humano) y las **columnas** la clase que predijo el modelo. La diagonal en negrita son
los aciertos; todo lo que está fuera de la diagonal es un error. El punto `·` es cero.

---

## Resumen comparativo

| Tarea | Accuracy baseline | Macro-F1 baseline | Accuracy BETO | Macro-F1 BETO |
|---|---:|---:|---:|---:|
| Categoría temática (7 clases) | 0.672 | 0.648 | ⏳ pendiente | ⏳ pendiente |
| Nivel de urgencia (3 niveles) | 0.661 | 0.445 | ⏳ pendiente | ⏳ pendiente |

---

## Categoría temática (7 clases)

Clase crítica: `persona_en_riesgo` (los falsos negativos aquí son el error más grave).

### Modelo de referencia — TF-IDF + LinearSVM

**Accuracy:** 0.672 · **Macro-F1:** 0.648 · *n* = 180

#### Matriz de confusión

| real \ predicho | `caida_poste_cable` | `dano_estructural` | `deslave` | `incendio` | `inundacion` | `otro` | `persona_en_riesgo` | **Total** |
|---|---|---|---|---|---|---|---|---|
| **`caida_poste_cable`** | **16** | · | · | 1 | · | 1 | 1 | 19 |
| **`dano_estructural`** | 1 | **1** | · | · | · | 2 | 2 | 6 |
| **`deslave`** | · | 1 | **14** | · | 1 | · | · | 16 |
| **`incendio`** | 1 | · | · | **32** | · | · | · | 33 |
| **`inundacion`** | · | · | · | · | **13** | 1 | 2 | 16 |
| **`otro`** | 4 | · | 3 | 6 | 1 | **19** | 12 | 45 |
| **`persona_en_riesgo`** | 2 | · | 1 | 2 | 2 | 12 | **26** | 45 |
| **Total** | 24 | 2 | 18 | 41 | 17 | 35 | 43 | **180** |

#### Métricas por clase

| Clase | Precisión | Exhaustividad (recall) | F1 | Soporte | Falsos negativos |
|---|---:|---:|---:|---:|---:|
| `caida_poste_cable` | 0.667 | 0.842 | 0.744 | 19 | 3 / 19 |
| `dano_estructural` | 0.500 | 0.167 | 0.250 | 6 | 5 / 6 |
| `deslave` | 0.778 | 0.875 | 0.824 | 16 | 2 / 16 |
| `incendio` | 0.780 | 0.970 | 0.865 | 33 | 1 / 33 |
| `inundacion` | 0.765 | 0.812 | 0.788 | 16 | 3 / 16 |
| `otro` | 0.543 | 0.422 | 0.475 | 45 | 26 / 45 |
| `persona_en_riesgo` ⚠️ | 0.605 | 0.578 | 0.591 | 45 | 19 / 45 |
| **Macro promedio** | **0.662** | **0.667** | **0.648** | 180 | — |

#### Principales confusiones

| Real | Predicho como | Casos |
|---|---|---:|
| `persona_en_riesgo` | `otro` | 12 |
| `otro` | `persona_en_riesgo` | 12 |
| `otro` | `incendio` | 6 |
| `otro` | `caida_poste_cable` | 4 |
| `otro` | `deslave` | 3 |

### BETO ajustado (modelo desplegado)

> ⏳ **Pendiente.** No se encontraron los pesos en `C:\Proyectos\sirec\microservicio-ml\modelos`.
> Ver `INSTRUCCIONES.md`, paso 2, para colocarlos y volver a ejecutar.

---

## Nivel de urgencia (3 niveles)

Clase crítica: `alta` (los falsos negativos aquí son el error más grave).

### Modelo de referencia — TF-IDF + LogReg

**Accuracy:** 0.661 · **Macro-F1:** 0.445 · *n* = 180

#### Matriz de confusión

| real \ predicho | `alta` | `baja` | `media` | **Total** |
|---|---|---|---|---|
| **`alta`** | **28** | 3 | 17 | 48 |
| **`baja`** | · | **0** | 14 | 14 |
| **`media`** | 21 | 6 | **91** | 118 |
| **Total** | 49 | 9 | 122 | **180** |

#### Métricas por clase

| Clase | Precisión | Exhaustividad (recall) | F1 | Soporte | Falsos negativos |
|---|---:|---:|---:|---:|---:|
| `alta` ⚠️ | 0.571 | 0.583 | 0.577 | 48 | 20 / 48 |
| `baja` | 0.000 | 0.000 | 0.000 | 14 | 14 / 14 |
| `media` | 0.746 | 0.771 | 0.758 | 118 | 27 / 118 |
| **Macro promedio** | **0.439** | **0.452** | **0.445** | 180 | — |

#### Principales confusiones

| Real | Predicho como | Casos |
|---|---|---:|
| `media` | `alta` | 21 |
| `alta` | `media` | 17 |
| `baja` | `media` | 14 |
| `media` | `baja` | 6 |
| `alta` | `baja` | 3 |

### BETO ajustado (modelo desplegado)

> ⏳ **Pendiente.** No se encontraron los pesos en `C:\Proyectos\sirec\microservicio-ml\modelos`.
> Ver `INSTRUCCIONES.md`, paso 2, para colocarlos y volver a ejecutar.

---
