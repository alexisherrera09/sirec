# Reporte del kappa de Cohen y conciliación — SIREC (Fase D3.4)

> Requisito del evaluador (Efrén Juárez): *"muestra doblemente etiquetada por DOS humanos +
> kappa de Cohen reportado"*. Este documento reporta el acuerdo inter-anotador inicial, el
> procedimiento de conciliación (adjudicación por un tercer anotador) aplicado cuando un campo
> quedó por debajo del umbral, y el conjunto **gold** resultante.
>
> Reproducible con: `calcular_kappa.py`, `generar_adjudicacion.py`, `consolidar_adjudicacion.py`.

## 1. Diseño del ejercicio

- **Muestra:** 180 reportes reales (`reportes_kappa.csv`), subconjunto estratificado del corpus
  real de 400 (los 180 están 100% contenidos en `corpus_etiquetado.csv`).
- **Anotadores:** Ricardo y Nahum, de forma **independiente y sin consultarse** (`INSTRUCCIONES_KAPPA.md`),
  usando la guía de etiquetado ya aprobada (`guia_etiquetado.md`).
- **Campos evaluados:** `categoria` (7 clases) y `urgencia` (3 niveles).
- **Escala de interpretación:** Landis & Koch (1977).

## 2. Kappa de Cohen inicial (antes de conciliar)

| Campo | Reportes emparejados | Acuerdo bruto (pₒ) | **Kappa (κ)** | Interpretación |
|---|---:|---:|---:|---|
| **Categoría** | 180 | 0.756 (136/180) | **0.701** | Considerable (substantial) |
| **Urgencia** | 180 | 0.611 (110/180) | **0.310** | Aceptable (fair) |

**Lectura honesta:**
- La **categoría** alcanza acuerdo *considerable* (κ = 0.70), por encima del umbral de referencia
  (≥ 0.60). Las etiquetas temáticas son objetivas y reproducibles entre anotadores.
- La **urgencia** queda en acuerdo *aceptable* (κ = 0.31), por debajo del umbral. Es un hallazgo
  legítimo y esperable: la urgencia es un juicio intrínsecamente más subjetivo que la categoría
  temática, y depende de cuánta gravedad infiere cada persona de un texto breve. No se oculta:
  se reporta y se resuelve con adjudicación (sección 4).

## 3. Principales desacuerdos

**Categoría** (44 desacuerdos): el más frecuente es `persona_en_riesgo` ↔ `otro` (15 casos),
que corresponde al caso frontera central de la guía (¿el texto implica o no una persona expuesta?).
Le siguen confusiones menores `persona_en_riesgo` ↔ `inundacion` y `otro` ↔ `caida_poste_cable`.

**Urgencia** (70 desacuerdos): el patrón es un corrimiento sistemático de un nivel —
`media`↔`alta` (30 casos) y `media`↔`baja` (21) — más 19 casos extremos `alta`↔`baja`.
El acuerdo en la clase crítica `urgencia=alta` fue de solo 31% (22/71), lo que confirma que el
criterio de urgencia necesitaba una decisión de consenso.

## 4. Conciliación por adjudicación (tercer anotador)

Procedimiento académico estándar cuando el acuerdo de un campo queda bajo umbral: un **tercer
anotador** (Alexis) resolvió cada desacuerdo consultando la guía, produciendo una etiqueta de
consenso. Las coincidencias entre Ricardo y Nahum se preservaron sin cambio.

- Decisiones de adjudicación: **114** (44 de categoría + 70 de urgencia).
- Resultado: `gold_kappa.csv` — 180 reportes con etiqueta final consensuada, `origen=real`.

### Distribución final del conjunto gold (180)

| Categoría | n | | Urgencia | n |
|---|---:|---|---|---:|
| `persona_en_riesgo` | 45 | | `media` | 118 |
| `otro` | 45 | | `alta` | 48 |
| `incendio` | 33 | | `baja` | 14 |
| `caida_poste_cable` | 19 | | | |
| `deslave` | 16 | | | |
| `inundacion` | 16 | | | |
| `dano_estructural` | 6 | | | |

## 5. Conclusión para la memoria

- El acuerdo inter-anotador en **categoría es considerable (κ = 0.70)**, lo que valida la
  objetividad del esquema temático de 7 clases.
- El acuerdo en **urgencia fue aceptable (κ = 0.31)**; se reconoce y documenta la mayor
  subjetividad de este juicio, y se resolvió mediante **adjudicación por un tercer anotador**
  para obtener un conjunto de prueba de consenso de alta calidad.
- Ninguna etiqueta fue generada por IA: el kappa mide acuerdo entre **dos personas reales** y la
  conciliación la realizó una **tercera persona real**, conforme al requisito del evaluador.
