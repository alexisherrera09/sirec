# SIREC — Avance del plan y tareas que te tocan a ti

> Documento de corte. Explica **hasta dónde llegó Claude (la IA)**, **por qué se detuvo justo ahí**,
> y **qué necesitas hacer tú (el equipo humano)** para poder continuar — con ejemplos y nombres de archivo concretos.
>
> Fecha de corte: **2026-07-02**. · Repartición de tareas por persona añadida: **2026-07-07**.

---

## 🔔 Actualización 2026-07-14 (tarde) — BETO entrenado: gana al baseline (D5/D6)

BETO fine-tuned corrió en Colab sobre el split gold. **Resultado contundente: supera al baseline en todo.**

| Tarea | Métrica | Baseline | **BETO** |
|---|---|---:|---:|
| Categoría | Macro-F1 | 0.65 | **0.74** |
| Categoría | Recall `persona_en_riesgo` | 0.58 (FN 19) | **0.87 (FN 6)** |
| Urgencia | Macro-F1 | 0.45 | **0.55** |
| Urgencia | Recall `alta` | 0.58 (FN 20) | **0.77 (FN 11)** |

- La mejora clave está en el **recall de las clases críticas** (el criterio del profesor): FN de
  `persona_en_riesgo` 19→6 y de `alta` 20→11. Confirma la hipótesis: el transformer capta la gravedad
  semántica que el modelo léxico no ve. Comparación completa en `comparacion_modelos.md`.
- Modelos exportados en `beto_modelos.zip` (`beto_categoria/`, `beto_urgencia/`).
- Límites honestos: `dano_estructural` (6) y `urgencia=baja` (14) siguen frágiles por escasez de datos.

**Pendiente:** (1) integrar BETO real al microservicio Python (reemplaza el modo simulado, sin cambiar
el contrato); (2) escribir la memoria; (3) despliegue AWS. Ya no hay tareas humanas de datos bloqueantes.

---

## 🔔 Actualización 2026-07-14 — kappa cerrado y baseline re-reportado sobre test validado

Ricardo y Nahum entregaron su doble etiquetado (`kappa_ricardo.csv`, `kappa_nahum.csv`, 180 c/u).
Con eso se cerró el núcleo humano que faltaba (**D3.4**):

- ✅ **Kappa de Cohen calculado** (`calcular_kappa.py`):
  - **Categoría: κ = 0.70** (considerable) — por encima del umbral.
  - **Urgencia: κ = 0.31** (aceptable) — por debajo del umbral. Hallazgo honesto: la urgencia es más subjetiva.
- ✅ **Conciliación por adjudicación** (decisión de Alexis, tercer anotador). Alexis resolvió los
  **114 desacuerdos** (44 categoría + 70 urgencia) en `adjudicacion_kappa.csv`. Scripts nuevos:
  `generar_adjudicacion.py` (arma el archivo con celdas en blanco solo en desacuerdos) y
  `consolidar_adjudicacion.py` (produce el gold, valida que no queden vacías).
- ✅ **Conjunto GOLD:** `gold_kappa.csv` — 180 reportes con etiqueta de **consenso** (100% real,
  doblemente validados). Son subconjunto exacto de los 400. Reporte completo en `reporte_kappa.md`.
- ✅ **Baseline re-reportado sobre el test validado** (decisión: 180 gold = test, 220 reales + sintéticos = train):
  - Categoría: macro-F1 **0.65** (SVM), recall `persona_en_riesgo` **0.58** (FN 19/45).
  - Urgencia: macro-F1 **0.45** (LogReg), recall `alta` **0.58** (0.69 con umbral 0.30). `baja` colapsa (recall 0).
  - Estos son los **números definitivos** (más estrictos que el CV previo). Ver `resultados_baseline.md` §0.
  - Modo nuevo en los scripts: `--gold-test` (baseline y umbral).

**Gating humano:** ✅ **cerrado por completo.** Guía aprobada, corpus real, kappa reportado + adjudicado.
Ya no hay tareas humanas bloqueantes. **Siguiente paso: BETO (D5) en Colab** con el split gold, y
evaluación comparada (D6) contra el piso del baseline.

---

## 🔔 Actualización 2026-07-13 — llegaron los datos reales

Ricardo y Nahum **entregaron sus corpus etiquetados** (200 reportes reales cada uno). Con eso:

- ✅ **D3.2/D3.3 completadas:** 400 reportes reales consolidados en `datos-modelo/corpus_etiquetado.csv`
  (validados: 7 categorías y 3 urgencias correctas, 0 duplicados entre ambos, 100% `origen=real`).
  Se corrigió 1 fila de Nahum que traía una nota personal en la columna `origen` → normalizada a `real`.
- ✅ **Trazabilidad (requisito del evaluador):** `datos-modelo/reporte_corpus.md` (% real 30.8 / % sintético 69.2 +
  distribución por clase y por anotador). Regenerable con `generar_reporte_corpus.py`.
- ✅ **Muestra de kappa lista:** `datos-modelo/reportes_kappa.csv` (180 reportes SIN etiqueta, estratificados)
  para que Ricardo y Nahum la etiqueten por separado (D3.4).
- ✅ **Scripts listos para ejecutar:** `calcular_kappa.py` (solo stdlib, ya probado), `entrenar_baseline.py`
  (TF-IDF + LogReg/SVM, métricas por clase + falsos negativos), `entrenar_beto_colab.ipynb` (fine-tuning para Colab),
  `requirements-modelo.txt`.

**Ojo — desbalance de clases real:** `dano_estructural` solo 11 de 400 (2.8%); `inundacion` 32; `deslave` 34.
Es la frecuencia natural de los reportes, no un sesgo de etiquetado. Se maneja con class weights y se reporta el recall por clase.

**Gating humano que aún bloquea D5–D6:**
1. ✅ **Guía aprobada** por Alexis (2026-07-13) — sección 6 de `guia_etiquetado.md`. **Tarea 1 cerrada.**
2. ⏳ **PENDIENTE — doble etiquetado del kappa (D3.4).** Instrucciones ya preparadas y despachadas:
   `datos-modelo/INSTRUCCIONES_KAPPA.md` (reenviable a ambos). Cada uno clasifica `reportes_kappa.csv`
   por separado, sin verse:
   - **Ricardo** corre `--salida kappa_ricardo.csv` (nombre `ricardo`) → debe regresar `kappa_ricardo.csv`.
   - **Nahum** corre `--salida kappa_nahum.csv` (nombre `nahum`) → debe regresar `kappa_nahum.csv`.
   - Cuando lleguen ambos: `py calcular_kappa.py --entrada kappa_ricardo.csv kappa_nahum.csv`.
   - **Esperando:** los dos archivos `kappa_*.csv` de vuelta. Es el único núcleo humano restante.

**D4 (baseline) NO depende del kappa** y ya se ejecutó en paralelo (guía aprobada):
- ✅ `entrenar_baseline.py` corrido y **optimizado** sobre los 400 reales (5-fold CV + holdout con sintéticos).
  Resultados en `datos-modelo/resultados_baseline.md`. Se hizo un barrido sistemático de mejoras (features,
  clasificadores, hiperparámetros) seleccionando por CV. **Única mejora estructural real: n-gramas de carácter**
  (leetspeak, stopwords, ensembles, ComplementNB, ajuste de C → descartados por ruido o empeorar).
- ✅ **Números finales del baseline (piso para BETO):**
  - Categoría: macro-F1 **0.71** (era 0.65); recall `persona_en_riesgo` **0.63** (FN 40→33).
  - Urgencia: macro-F1 **0.51** (era 0.46); recall `alta` **0.53** (FN 59→50), y con umbral 0.30 → **0.71** (FN 31).
  - Palanca del umbral documentada en `optimizar_umbral_alta.py` (compromiso recall↔precisión, criterio del profesor).
- Dependencias instaladas en el Python global de la máquina: scikit-learn, pandas, numpy.

BETO (D5–D6) se cierra tras el kappa.

### ⏸️ Punto de espera acordado (2026-07-13) — ✅ RESUELTO el 2026-07-14 (ver corte superior)

Se decidió **pausar aquí** hasta que Ricardo y Nahum entreguen su doble etiquetado. La IA ya hizo todo
lo delegable (corpus consolidado, trazabilidad, guía aprobada, muestra de kappa, baseline optimizado).
**No se avanza a BETO (D5) ni al cuaderno de Colab hasta tener el kappa** — así se evita trabajo sobre
etiquetas aún sin validar.

**En espera de:** `kappa_ricardo.csv` y `kappa_nahum.csv` (ver `INSTRUCCIONES_KAPPA.md`).
**Al recibirlos, retomar así:**
1. `py calcular_kappa.py --entrada kappa_ricardo.csv kappa_nahum.csv` → reportar kappa (categoría y urgencia).
2. Si el kappa es aceptable (≥0.60 considerable), continuar con BETO (D5) en Colab y evaluación (D6).
3. Re-reportar las métricas del baseline y BETO sobre el conjunto de prueba ya validado.

---

## 1. Hasta aquí llegó la IA (todo esto ya está hecho y verificado)

| Fase del plan | Qué se construyó | Estado | Dónde está |
|---|---|---|---|
| **A1** | Microservicio de clasificación (Python/FastAPI), modo simulado por palabras clave | ✅ pytest 6/6 | `microservicio-ml/` |
| **B1–B5** | Backend .NET 8: base de datos, endpoint público con respaldo si falla el clasificador, panel, login JWT, CORS | ✅ checkpoints OK | `backend-api/` |
| **C1–C2** | Frontend React: formulario público + panel del operador (priorizado por urgencia) | ✅ flujo e2e OK | `frontend/` |
| **D1** | Guía de etiquetado (7 categorías, criterio de urgencia, casos frontera) | ✅ redactada | `datos-modelo/guia_etiquetado.md` |
| **D2** | Herramienta de etiquetado local (individual + doble) | ✅ probada | `datos-modelo/herramienta_etiquetado.py` |
| **D3.1** | Corpus **sintético** (900 reportes generados, declarados como sintéticos) | ✅ generado | `datos-modelo/corpus_sintetico.csv` |

**En pocas palabras:** el sistema de software completo funciona de punta a punta en local (formulario → clasificación → panel), y la parte "sintética" de los datos está lista.

---

## 2. Dónde y por qué me detuve (esto NO lo puede hacer la IA)

Me detuve justo antes de las fases **D3.2, D3.3 y D3.4** (datos reales + kappa) y, por lo tanto, antes de **D4–D6** (baseline, BETO, evaluación).

**El motivo no es técnico, es de honestidad académica.** Tu profesor (Efrén Juárez) puso tres exigencias que, si las hace una IA, **invalidan la titulación**:

1. **La guía la debe aprobar un humano.** Si yo apruebo lo que yo mismo escribí, no hubo revisión independiente.
2. **El conjunto de prueba debe ser 100% real.** Si yo "invento" reportes reales, eso es *fabricar datos* — las métricas saldrían falsas y es causal de reprobación por deshonestidad.
3. **El kappa de Cohen debe medir el acuerdo entre DOS personas reales.** Si una IA etiqueta dos veces, el número es una mentira. El plan lo dice literal: *"una IA etiquetando no cuenta como acuerdo entre anotadores"*.

Por eso el software (que sí es mi trabajo) está terminado, pero la **evidencia de validez** (datos reales + acuerdo humano) tiene que producirla el equipo. Es el único núcleo humano de todo el proyecto.

---

## 3. Lo que necesito que hagas tú — explicado paso a paso

Son **tres tareas**. Ninguna requiere programar. Abajo te digo exactamente en qué archivo y con qué formato.

### Repartición del trabajo (2026-07-07)

El trabajo manual lo hace el equipo (**Ricardo** y **Nahum**), con instructivos individuales ya preparados:

| Persona | Qué hace | Archivo que llena | Nombre en la herramienta | Instructivo |
|---|---|---|---|---|
| **Ricardo** | Junta y clasifica ~200 reportes reales | `datos-modelo/reportes_ricardo.csv` | `ricardo` | `datos-modelo/INSTRUCCIONES_RICARDO.md` |
| **Nahum** | Junta y clasifica ~200 reportes reales (fuentes/eventos distintos a los de Ricardo) | `datos-modelo/reportes_nahum.csv` | `nahum` | `datos-modelo/INSTRUCCIONES_NAHUM.md` |
| **Ambos** | Doble etiquetado de `reportes_kappa.csv` (~180) para el kappa | `datos-modelo/reportes_kappa.csv` | cada uno el suyo | (Alexis lo prepara y avisa) |

- Los dos archivos juntos (~400 reportes) forman el **conjunto de prueba** real.
- Molde de estilo para copiar/anonimizar y practicar la clasificación: `datos-modelo/EJEMPLOS_reportes.csv` (21 ejemplos ya anonimizados con su categoría/urgencia correcta).
- La **aprobación académica de la guía (Tarea 1) la firma Alexis**; Ricardo y Nahum solo la leen para clasificar bien.
- El **archivo del kappa** (`reportes_kappa.csv`, ~180 tomados de los dos archivos) lo arma Alexis cuando ambos terminen, y entonces los dos lo etiquetan por separado.

---

### TAREA 1 — Leer y aprobar la guía de etiquetado

**Archivo a leer:** `datos-modelo/guia_etiquetado.md`

**Qué hacer:** léela (son ~10 min) y decide si el criterio te convence. Fíjate sobre todo en:
- Las **7 definiciones de categoría** (sección 2). ¿Están bien para reportes de tu municipio?
- La **regla de desempate**: si hay una persona en peligro *además* de otra cosa (ej. "se incendia la casa y hay alguien adentro"), lo clasifico como `persona_en_riesgo`, no `incendio`. ¿De acuerdo?
- El **criterio de urgencia** (sección 3) y su principio: ante duda entre `alta` y `media`, si hay personas expuestas → `alta`.
- Los **7 casos de frontera** (sección 4). Aquí es donde más fácil pueden discrepar.

**Cómo entregarlo:** al final de `guia_etiquetado.md` agrega unas líneas como estas (ejemplo):

```markdown
## 6. Aprobación del equipo
- Revisada y aprobada por: Alexis Herrera, María López — 2026-07-05.
- Ajustes pedidos: ninguno.  (o: "cambiamos el caso frontera 3 a urgencia alta")
```

> Si quieres cambios en vez de aprobar, dímelo y yo edito la guía; tú solo firmas la versión final.

---

### TAREA 2 — Conseguir ~300–400 reportes REALES y etiquetarlos

Esta es la tarea grande, pero es de "copiar, limpiar y clasificar", no de programar.

#### 2a. Recolectar el texto real

**Archivo a llenar:** `datos-modelo/reportes_sin_etiquetar.csv`

De dónde sacar reportes reales (fuentes que el plan permite):
- Publicaciones públicas de redes sociales durante contingencias pasadas (inundaciones, nortes, deslaves en Veracruz).
- Notas de prensa que citen reportes ciudadanos.
- Transcripciones de reportes o llamadas (si tienen acceso).

**Formato del archivo** (una fila por reporte; solo importa la columna `texto`):

```csv
texto,origen
"Se metió el agua a mi casa en la colonia Las Brisas, ya nos llega a la rodilla",real
"Hay un poste caído con cables sobre la avenida, cuidado",real
"¿Dónde puedo llevar a mi familia? Perdimos todo con la inundación",real
```

#### 2b. Anonimizar (MUY importante)

Antes de guardar, **quita datos personales** del texto real:
- Nombres propios de personas → cámbialos o bórralos.
- Teléfonos, direcciones exactas con número, placas, etc. → quítalos o generalízalos (deja solo la colonia).

Ejemplo:
- ❌ Original: *"Habla Juan Pérez del 229-123-4567, mi casa en Av. Hidalgo #45 se inundó"*
- ✅ Anonimizado: *"Mi casa en la avenida Hidalgo se inundó"*

#### 2c. Etiquetar con la herramienta

En una terminal:

```powershell
cd datos-modelo
py herramienta_etiquetado.py --entrada reportes_sin_etiquetar.csv --origen real
```

Abre **http://localhost:8080**, escribe tu nombre y clasifica cada reporte:
- Teclas **1–7** = categoría · teclas **A / M / B** = urgencia · **Enter** = guardar y siguiente.

El resultado se guarda solo en `datos-modelo/corpus_etiquetado.csv`. **Este será el conjunto de prueba del modelo.**

---

### TAREA 3 — Doble etiquetado (para el kappa de Cohen)

**Objetivo:** demostrar que las etiquetas son objetivas, midiendo cuánto coinciden **dos personas distintas** etiquetando lo mismo por separado.

**Qué hacer:**
1. Tomen un subconjunto de ~150–200 de los reportes reales (puede ser un CSV aparte, ej. `reportes_muestra_kappa.csv`, o los mismos 150 primeros).
2. **Dos personas del equipo** los etiquetan **por separado, sin verse**, cada una con un nombre distinto:

```powershell
# Persona 1
py herramienta_etiquetado.py --entrada reportes_muestra_kappa.csv --origen real
# (en el navegador escribe: ana)

# Persona 2 (después, en otra sesión o computadora)
py herramienta_etiquetado.py --entrada reportes_muestra_kappa.csv --origen real
# (en el navegador escribe: luis)
```

La herramienta guarda las dos respuestas por separado (columna `etiquetador`), y con eso yo calculo el kappa automáticamente después.

> ⚠️ Esto **tiene** que hacerlo dos personas reales. Es el único punto donde no hay atajo: es exactamente lo que el profesor quiere ver.

---

## 4. Qué haré yo mientras tanto (en paralelo, no te detiene)

Mientras el equipo hace lo anterior, yo puedo ir dejando listo (avísame para arrancar):

- **Red-team de la guía**: buscarle huecos y dejarte una lista de puntos a decidir, para que revisar sea más rápido.
- **Ayuda para conseguir fuentes reales**: buscar enlaces/candidatos reales de contingencias en Veracruz para que solo copien y anonimicen.
- **Escribir y probar los scripts** que faltan, listos para ejecutar en cuanto tengan los datos:
  - `calcular_kappa.py` (kappa de Cohen + interpretación)
  - `reporte_corpus.md` (trazabilidad: % real / % sintético + distribución por clase)
  - `entrenar_baseline.py` (TF-IDF + regresión logística/SVM, métricas por clase)
  - `entrenar_beto.py` + `entrenar_beto_colab.ipynb` (fine-tuning de BETO)
  - `comparacion_modelos.md` (baseline vs BETO)

---

## 5. Resumen en una frase

**El software está terminado; falta la evidencia humana.** Necesito de ti: (1) aprobar la guía, (2) juntar y etiquetar ~300–400 reportes reales, (3) que dos personas etiqueten ~150–200 para el kappa. En cuanto tenga `corpus_etiquetado.csv` con datos reales, ejecuto el entrenamiento y la evaluación, y cerramos el modelo.

**Checklist rápido (por persona):**

_Alexis:_
- [ ] Leí y aprobé (o pedí cambios en) `datos-modelo/guia_etiquetado.md`
- [ ] Armé `reportes_kappa.csv` (~180) cuando Ricardo y Nahum terminaron
- [ ] Le aviso a Claude para continuar con D4–D6

_Ricardo:_
- [ ] Leí la guía `datos-modelo/guia_etiquetado.md`
- [ ] Llené `datos-modelo/reportes_ricardo.csv` con ~200 reportes reales anonimizados
- [ ] Los clasifiqué con la herramienta (nombre `ricardo`)
- [ ] Clasifiqué `reportes_kappa.csv` (cuando Alexis avisó)

_Nahum:_
- [ ] Leí la guía `datos-modelo/guia_etiquetado.md`
- [ ] Llené `datos-modelo/reportes_nahum.csv` con ~200 reportes reales anonimizados
- [ ] Los clasifiqué con la herramienta (nombre `nahum`)
- [ ] Clasifiqué `reportes_kappa.csv` (cuando Alexis avisó)
