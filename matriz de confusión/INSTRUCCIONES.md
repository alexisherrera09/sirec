# Matrices de confusión — procedimiento

> **Objetivo:** producir `matrices_confusion.md` con las matrices de confusión y las métricas
> por clase completas de los dos modelos (baseline y BETO) sobre las dos tareas (categoría y
> urgencia), evaluados en el mismo conjunto de prueba.
>
> **Por qué:** el objetivo específico 5 del documento académico dice literalmente *"métricas por
> clase (precisión, exhaustividad y medida F1) **y matriz de confusión**"*, la Tabla 10 del
> capítulo 4 la lista como evidencia comprometida, y era uno de los cinco requisitos del profesor
> desde la Entrega 1. Hoy el capítulo 6 no incluye ninguna matriz, y el §7.2 afirma que ese
> objetivo se cumplió. Esto cierra esa brecha.

---

## Contenido de esta carpeta

| Archivo | Qué es |
|---|---|
| `INSTRUCCIONES.md` | Este documento: qué hay que hacer y en qué orden. |
| `generar_matrices.py` | El script que produce todo. Se ejecuta las veces que haga falta. |
| `matrices_confusion.md` | **El resultado.** Es el entregable de esta carpeta. |

---

## Principio de método: no se reentrena nada

Las cifras del capítulo 6 ya están publicadas en el documento. Regenerarlas con un
reentrenamiento arriesga que salgan distintas y que el anexo contradiga a la tabla. Por eso:

- **Baseline** → sí se reentrena, pero es **determinista**: scikit-learn con semilla 42 y un
  split que no es aleatorio (el test se construye por coincidencia de texto contra
  `gold_kappa.csv`). Ya se verificó que reproduce exactamente las cifras publicadas.
- **BETO** → **no se reentrena**. Solo se hace inferencia sobre los 180 del gold con los pesos
  ya entrenados. En modo evaluación no hay dropout ni aleatoriedad, así que las predicciones son
  siempre las mismas y reproducen las cifras publicadas.

> ⚠️ **No vuelvas a correr `entrenar_beto_colab.ipynb` para esto.** Ese notebook sí tiene fuentes
> de no-determinismo (la cabeza de clasificación se inicializa antes de que se fije la semilla,
> `fp16` activo, sin flags de determinismo de cuDNN, versiones de librerías sin fijar, y
> `load_best_model_at_end` que puede elegir otra época ante diferencias mínimas). Reentrenar
> daría números parecidos pero distintos, y el documento los reporta a tres decimales.

---

## Paso 1 — Baseline ✅ hecho

```powershell
cd "matriz de confusión"
py generar_matrices.py
```

Genera `matrices_confusion.md` con las matrices del modelo de referencia ya completas.

**Verificación de consistencia (ya realizada):** los valores reproducen exactamente los del
documento — categoría (SVM) accuracy 0.672, macro-F1 0.648, recall `persona_en_riesgo` 0.578,
19 falsos negativos de 45; urgencia (LogReg) accuracy 0.661, macro-F1 0.445, recall `alta` 0.583,
20 falsos negativos de 48. Coinciden con las Tablas 23, 24 y 27 del capítulo 6.

---

## Paso 2 — BETO ⏳ pendiente

Falta **una sola cosa**: los pesos de los dos modelos. No están en esta máquina porque pesan
~880 MB y están excluidos de git a propósito.

### 2.1. Conseguir los pesos

Según `DESPLIEGUE_EC2_REALIZADO.md` existen en tres lugares. Cualquiera sirve:

| Origen | Ruta |
|---|---|
| Producción (EC2) | `/usr/local/proyectos/ml_sirec/modelos/` |
| Copia de trabajo (EC2) | `/home/ubuntu/modelos/` |
| Comprimido (EC2) | `beto_modelos.zip` — 176 MB, en la raíz del repo |
| Google Drive | `beto_modelos.zip`, lo dejó ahí la última celda del notebook de Colab |

Desde la EC2, con la llave `.pem`:

```powershell
scp -i RUTA\llave.pem -r ubuntu@13.221.48.89:/usr/local/proyectos/ml_sirec/modelos/* .\microservicio-ml\modelos\
```

O el comprimido, que baja mucho más rápido:

```powershell
scp -i RUTA\llave.pem ubuntu@13.221.48.89:~/proyectos/sirec/beto_modelos.zip .
# y descomprimir dentro de microservicio-ml\modelos\
```

### 2.2. Dejarlos con esta estructura

```
microservicio-ml/modelos/
├── beto_categoria/     ← config.json, model.safetensors (~439 MB), tokenizer...
└── beto_urgencia/      ← config.json, model.safetensors (~439 MB), tokenizer...
```

Si están en otro lado, no hace falta moverlos:

```powershell
py generar_matrices.py --modelos "D:\ruta\donde\esten"
```

### 2.3. Volver a ejecutar

```powershell
py generar_matrices.py
```

El script detecta los pesos, corre la inferencia sobre los 180 del gold (un par de minutos en
CPU) y reescribe `matrices_confusion.md` con las cuatro matrices completas y el resumen
comparativo lleno.

### 2.4. Comprobar que cuadra

Antes de llevar nada al documento, verificar que la salida de BETO coincide con lo publicado:

| Métrica | Valor esperado (capítulo 6) |
|---|---|
| Categoría — accuracy | 0.778 |
| Categoría — macro-F1 | 0.744 |
| Categoría — recall `persona_en_riesgo` | 0.867 · 6 falsos negativos de 45 |
| Urgencia — accuracy | 0.689 |
| Urgencia — macro-F1 | 0.546 |
| Urgencia — recall `alta` | 0.771 · 11 falsos negativos de 48 |

Si coinciden, el anexo es consistente con el cuerpo del documento y se puede usar tal cual.
Si no coinciden, **no cambies el documento todavía**: significa que los pesos de esa carpeta no
son los que produjeron las cifras publicadas, y hay que localizar la versión correcta.

---

## Paso 3 — Llevarlo al documento

1. **Capítulo 6** — insertar las matrices y las tablas por clase. Ubicación natural: dentro de
   §6.4 (modelo de referencia) y §6.5 (BETO), o como un §6.6 bis antes de la comparación.
   Con esto el objetivo específico 5 queda cumplido de verdad y la afirmación del §7.2 deja de
   estar descubierta.

2. **§6.7 "Robustez y análisis de errores"** — aquí está el mayor valor. Las matrices revelan un
   hallazgo que hoy no está escrito:

   > **El error dominante del modelo coincide con el desacuerdo dominante entre los anotadores
   > humanos.** En categoría, la confusión mayor es `otro` ↔ `persona_en_riesgo` (12 casos en
   > cada dirección, 24 en total); la Tabla 21 reporta que el principal desacuerdo humano fue
   > exactamente `persona_en_riesgo ↔ otro`, con 15 casos. En urgencia, la confusión mayor es
   > `alta` ↔ `media` (17 + 21 = 38 casos) y el principal desacuerdo humano fue `media ↔ alta`,
   > con 23 casos. Además `baja` colapsa por completo en el baseline: los 14 casos reales se
   > predicen como `media`, cero aciertos.
   >
   > Es decir: **el modelo no se equivoca al azar, se equivoca justo donde la tarea es
   > intrínsecamente ambigua también para las personas.** Eso conecta el kappa del §6.3 con los
   > errores del §6.7 y convierte esa sección —que hoy solo enumera propiedades del diseño— en un
   > análisis de errores real, que es lo que pidió el profesor.

3. **Anexo** — `matrices_confusion.md` puede ir completo como Anexo D, igual que se hizo con el
   Anexo C del cálculo del kappa. Sirve como evidencia de reproducibilidad.

---

## Si algo falla

| Síntoma | Causa y solución |
|---|---|
| `No module named 'torch'` | `py -m pip install torch transformers` |
| `Pesos no encontrados` | La carpeta no tiene `beto_categoria/` y `beto_urgencia/`. Revisar el paso 2.2 o pasar `--modelos RUTA`. |
| Solo quieres el baseline | `py generar_matrices.py --solo-baseline` |
| Los números de BETO no cuadran | Pesos equivocados. Ver paso 2.4 — no tocar el documento. |
