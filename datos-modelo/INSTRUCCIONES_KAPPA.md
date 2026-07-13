# Doble etiquetado (kappa) — instrucciones para Ricardo y Nahum

Hola. Esta es la **última tarea** de datos del proyecto SIREC y es rapidísima (~40–50 min).
No hay que juntar ni anonimizar nada nuevo: **solo clasificar** una lista de 180 reportes que ya
está lista. Lo hacen **los dos por separado, sin verse**, y con eso se calcula el "kappa de Cohen"
(la medida que exige el profesor para probar que las etiquetas son objetivas).

> ⚠️ Lo más importante: **NO se consultan entre ustedes mientras etiquetan, ni comparan respuestas.**
> El sentido de esta prueba es justamente ver qué tanto coinciden trabajando por separado.
> Si se ponen de acuerdo, el número deja de servir.

---

## Qué te va a pasar Alexis

Dos archivos, ponlos **juntos en una misma carpeta**:
1. `reportes_kappa.csv` — los 180 reportes a clasificar (ya vienen sin etiqueta).
2. `herramienta_etiquetado.py` — la misma herramienta que ya usaste.

(Si ya tienes la herramienta de la vez pasada, solo necesitas el `reportes_kappa.csv` nuevo.)

---

## Paso 1 — Ten a la mano la guía

Clasifica con el mismo criterio de siempre: **`guia_etiquetado.md`** (7 categorías + 3 urgencias,
con ejemplos y casos de frontera). Es la versión ya aprobada; no cambió nada.

## Paso 2 — Abre la herramienta con TU archivo de salida

En PowerShell, dentro de la carpeta donde pusiste los dos archivos, corre el comando que te toca:

**Si eres RICARDO:**
```powershell
py herramienta_etiquetado.py --entrada reportes_kappa.csv --salida kappa_ricardo.csv
```

**Si eres NAHUM:**
```powershell
py herramienta_etiquetado.py --entrada reportes_kappa.csv --salida kappa_nahum.csv
```

## Paso 3 — Clasifica los 180

1. Abre en el navegador **http://localhost:8080**
2. Escribe tu nombre — **exactamente** `ricardo` o `nahum` (minúsculas).
3. Para cada reporte elige **categoría** y **urgencia** y guarda:
   - Teclas **1–7** = categoría · **A / M / B** = urgencia · **Enter** = guardar y siguiente.
4. Clasifica **los 180**, hasta que salga el mensaje **"¡Listo! No hay más reportes pendientes"**.
   - No dejes ninguno en blanco. Si dudas, elige lo que más se acerque según la guía (así se hace en la vida real).
   - Si te interrumpen, puedes cerrar y volver a correr el mismo comando: retoma donde te quedaste.

## Paso 4 — Regrésale a Alexis UN archivo

Cuando termines, en la carpeta te quedó **un solo archivo**:
- Ricardo → **`kappa_ricardo.csv`**
- Nahum → **`kappa_nahum.csv`**

Mándaselo a Alexis (ese archivo tiene 180 renglones con columnas
`texto, categoria, urgencia, etiquetador, origen`). **Eso es todo.**

---

## Checklist
- [ ] Puse `reportes_kappa.csv` y la herramienta en una carpeta.
- [ ] Clasifiqué **sin consultar** al otro compañero.
- [ ] Etiqueté **los 180** (salió "¡Listo!").
- [ ] Le regresé a Alexis mi archivo `kappa_ricardo.csv` / `kappa_nahum.csv`.

¡Gracias! Con esto se cierra la parte humana del proyecto.
