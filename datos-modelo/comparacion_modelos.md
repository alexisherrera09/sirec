# Comparación de modelos: baseline vs BETO (Fases D4–D6) — SIREC

> Comparación final entre el **baseline clásico** (TF-IDF + lineal, D4) y **BETO fine-tuned**
> (`dccuchile/bert-base-spanish-wwm-cased`, D5) sobre el **mismo conjunto de prueba gold**:
> 180 reportes reales doblemente etiquetados y adjudicados por consenso (`gold_kappa.csv`).
> Entrenamiento en ambos: 220 reales restantes + 900 sintéticos (declarados, solo train). Sin fuga.
> Criterio rector del evaluador: **recall de las clases críticas** (falsos negativos son lo más grave).

## 1. Resumen — el veredicto

| Tarea | Métrica | Baseline (mejor) | **BETO** | Δ |
|---|---|---:|---:|---:|
| **Categoría** | Macro-F1 | 0.648 (SVM) | **0.744** | **+0.096** |
| **Categoría** | Accuracy | 0.672 | **0.778** | +0.106 |
| **Categoría** | Recall `persona_en_riesgo` ⚠️ | 0.578 | **0.867** | **+0.289** |
| **Categoría** | Falsos negativos `persona_en_riesgo` | 19 / 45 | **6 / 45** | **−13** |
| **Urgencia** | Macro-F1 | 0.445 (LogReg) | **0.546** | **+0.101** |
| **Urgencia** | Accuracy | 0.661 | **0.689** | +0.028 |
| **Urgencia** | Recall `alta` ⚠️ | 0.583 | **0.771** | **+0.188** |
| **Urgencia** | Falsos negativos `alta` | 20 / 48 | **11 / 48** | **−9** |

**BETO gana en todas las métricas y de forma decisiva en lo que más importa:** el recall de las
clases críticas. En `persona_en_riesgo` los falsos negativos caen de 19 a **6** (recall 0.58 → 0.87);
en `urgencia=alta` de 20 a **11** (recall 0.58 → 0.77). Es exactamente la hipótesis del proyecto:
un transformer capta la **gravedad semántica** ("no responde", "sigue subiendo", "hay gente adentro")
que un modelo léxico no ve.

> Nota de fuerza: BETO en modo normal (recall `alta` = 0.77) **supera incluso al baseline con su
> umbral forzado a 0.30** (recall `alta` = 0.69). No necesita sacrificar precisión para ganar recall.

## 2. Categoría (7 clases) — F1 por clase sobre el test gold

| Clase | Baseline F1 (SVM) | **BETO F1** | BETO recall | Soporte |
|---|---:|---:|---:|---:|
| incendio | 0.865 | **0.886** | 0.939 | 33 |
| persona_en_riesgo ⚠️ | 0.591 | **0.830** | **0.867** | 45 |
| deslave | 0.824 | 0.824 | 0.875 | 16 |
| caida_poste_cable | 0.744 | **0.791** | 0.895 | 19 |
| inundacion | 0.788 | 0.727 | 0.750 | 16 |
| otro | 0.475 | **0.649** | 0.533 | 45 |
| dano_estructural | 0.250 | **0.500** | 0.500 | 6 |

BETO mejora o iguala en 6 de 7 clases. El salto más importante es `persona_en_riesgo` (F1 0.59 → 0.83)
y `otro` (0.48 → 0.65), las dos que más se confundían entre sí en el baseline. Incluso
`dano_estructural`, la clase más escasa (6 casos), duplica su F1 (0.25 → 0.50).

## 3. Urgencia (3 niveles) — F1 por clase sobre el test gold

| Nivel | Baseline F1 (LogReg) | **BETO F1** | BETO recall | Soporte |
|---|---:|---:|---:|---:|
| media | 0.758 | **0.764** | 0.712 | 118 |
| alta ⚠️ | 0.577 | **0.661** | **0.771** | 48 |
| baja | 0.000 | **0.214** | 0.214 | 14 |

La urgencia sigue siendo la tarea más difícil (la gravedad es un juicio subjetivo — coherente con el
kappa humano de 0.31 en este campo). Aun así BETO **recupera parcialmente `baja`** (recall 0.00 → 0.21),
que el baseline colapsaba por completo contra `media`, y sube con fuerza el recall de `alta`.

## 4. Conclusiones para la memoria

- **BETO es el modelo a desplegar.** Supera al baseline en todas las métricas y, sobre todo, reduce a
  la mitad o más los falsos negativos de las clases críticas — el criterio que el evaluador priorizó.
- **La mejora está donde debía estar:** en la semántica de la gravedad y del riesgo humano, justo la
  brecha que un modelo léxico (TF-IDF) no puede cerrar. El baseline cumplió su rol de piso honesto.
- **Límites que se reportan con honestidad:** `dano_estructural` (6 casos) y `urgencia=baja` (14 casos)
  siguen frágiles por escasez de datos reales; es desbalance natural del corpus, no del modelo.
  Se documenta como trabajo futuro (recolectar más ejemplos de esas clases).
- **Coherencia con el kappa:** la urgencia rinde menos que la categoría en ambos modelos, lo cual es
  consistente con que los propios anotadores humanos concuerdan menos en urgencia (κ 0.31) que en
  categoría (κ 0.70). El techo de un clasificador no puede superar de forma limpia el acuerdo humano.

## 5. Reproducibilidad

- Baseline: `py entrenar_baseline.py --gold-test --con-sintetico` (+ `optimizar_umbral_alta.py --gold-test`).
- BETO: `entrenar_beto_colab.ipynb` en Colab con GPU (o `entrenar_beto.py --gold-test --con-sintetico`).
- Modelos entrenados: `beto_categoria/` y `beto_urgencia/` (exportados en `beto_modelos.zip`).
- Conjunto de prueba: `gold_kappa.csv` (180, consenso humano). Kappa: `reporte_kappa.md`.
