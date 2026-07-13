# Reporte de trazabilidad del corpus — SIREC

> Requisito del evaluador: origen cuantificado de los reportes (% real / % sintético) y
> distribución por clase. El **conjunto de prueba del modelo es 100%% real** (regla innegociable).
> Generado automáticamente a partir de `corpus_etiquetado.csv` (real) y `corpus_sintetico.csv`.

## 1. Origen de los datos (trazabilidad)

| Origen | Reportes | % del total | Uso |
|---|---:|---:|---|
| `real` (recolectado y anonimizado) | 400 | 30.8% | Entrenamiento + **conjunto de prueba** |
| `sintetico` (generado con IA, declarado) | 900 | 69.2% | Solo aumento de entrenamiento; **nunca** en prueba |
| `redactado` (reescrito por el equipo) | 0 | 0.0% | — |
| **Total** | **1300** | **100%** | |

Los 400 reportes reales fueron recolectados y etiquetados por dos integrantes del equipo
(Ricardo: 200, Nahum: 200) a partir de publicaciones públicas de contingencias en Veracruz,
anonimizados según la guía de etiquetado. Fuentes/eventos distintos entre ambos (0 duplicados).

## 2. Distribución por categoría

| Categoría | Real | Sintético | Total |
|---|---:|---:|---:|
| `persona_en_riesgo` | 89 | 180 | 269 |
| `inundacion` | 32 | 140 | 172 |
| `caida_poste_cable` | 55 | 120 | 175 |
| `deslave` | 34 | 120 | 154 |
| `incendio` | 70 | 120 | 190 |
| `dano_estructural` | 11 | 120 | 131 |
| `otro` | 109 | 100 | 209 |
| **Total** | **400** | **900** | **1300** |

## 3. Distribución por urgencia

| Urgencia | Real | Sintético | Total |
|---|---:|---:|---:|
| `alta` | 106 | 395 | 501 |
| `media` | 228 | 314 | 542 |
| `baja` | 66 | 191 | 257 |
| **Total** | **400** | **900** | **1300** |

## 4. Corpus real por anotador (categoría)

| Anotador | `persona_en_riesgo` | `inundacion` | `caida_poste_cable` | `deslave` | `incendio` | `dano_estructural` | `otro` | Total |
|---|---|---|---|---|---|---|---|---|
| nahum | 62 | 11 | 9 | 4 | 44 | 5 | 65 | 200 |
| ricardo | 27 | 21 | 46 | 30 | 26 | 6 | 44 | 200 |

## 5. Observaciones para la memoria (honestidad de datos)

- **Desbalance de clases real (natural, no corregido en los datos):** la clase
  `dano_estructural` está fuertemente subrepresentada en el corpus real (11 de 400, 2.8%).
  También `inundacion` (32) y `deslave` (34) son minoritarias. Esto se debe a que refleja la
  frecuencia real de los reportes recolectados, no a un sesgo de etiquetado. Se abordará en el
  modelado con **class weights / métricas por clase** y se reportará el impacto en recall.
- **Corrección de datos aplicada:** 1 fila de Nahum traía una nota personal del anotador en la
  columna `origen`; se normalizó a `origen=real` (la nota no altera texto/categoría/urgencia).
- **Sesgo entre anotadores visible:** Ricardo etiquetó más `caida_poste_cable` y urgencia `media`;
  Nahum más `persona_en_riesgo` y `otro`. Esto es esperado por trabajar eventos distintos, pero
  **motiva el cálculo de kappa** sobre una muestra doblemente etiquetada (ver `reportes_kappa.csv`).
- **Conjunto de prueba:** se formará exclusivamente con `origen=real` (400 disponibles).
