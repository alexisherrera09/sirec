# Ricardo — tu tarea (paso a paso)

Hola Ricardo. Me estás ayudando con la parte de datos de mi proyecto de maestría (SIREC,
un clasificador de reportes ciudadanos en emergencias). **No hay que programar nada.**
Tu tarea es **juntar reportes reales, quitarles los datos personales y clasificarlos**.

Tiempo estimado: unas 2–3 horas repartidas.

---

## Paso 0 — Lee la guía (10 min, obligatorio para clasificar bien)

Abre y lee: **`datos-modelo/guia_etiquetado.md`**

Ahí están las **7 categorías** y los **3 niveles de urgencia** con ejemplos y casos de frontera.
No tienes que aprobarla ni firmar nada (eso lo hago yo), pero necesitas conocerla para el Paso 3.

---

## Paso 1 — Junta ~200 reportes REALES

**Archivo que vas a llenar:** `datos-modelo/reportes_ricardo.csv`

Un renglón por reporte. Solo importa la columna **`texto`**; deja la columna **`origen`** como **`real`**.

**De dónde sacarlos (tienen que ser reales, no inventados):**
- Publicaciones públicas de redes sociales durante contingencias pasadas en Veracruz
  (inundaciones, nortes, deslaves): Facebook de grupos de colonias, X/Twitter, etc.
- Notas de prensa que citen reportes de ciudadanos.
- Transcripciones de reportes o llamadas, si tienes acceso.

> Necesitamos que sean reales porque son la "prueba final" del modelo. Inventarlos invalidaría el proyecto.

---

## Paso 2 — Anonimiza (MUY importante)

Antes de pegarlos, **quítales los datos personales**:
- Nombres de personas → bórralos o cámbialos.
- Teléfonos, direcciones con número, placas → quítalos (deja solo la colonia o la calle).

**Ejemplo:**
- Original: *"Habla Juan Pérez del 229-123-4567, mi casa en Av. Hidalgo #45 se inundó"*
- Anonimizado: *"Mi casa en la avenida Hidalgo se inundó"*

---

## Cómo debe quedar tu archivo (imita este estilo)

Mira **`datos-modelo/EJEMPLOS_reportes.csv`** (tiene 21 ejemplos ya anonimizados).
Tu `reportes_ricardo.csv` debe verse así — **borra el renglón de instrucciones que trae** y pega los tuyos:

```csv
texto,origen
"Se metió el agua a mi casa en la colonia Las Brisas, ya nos llega a la rodilla",real
"Se cayó un poste de luz y los cables quedaron sobre la banqueta donde pasa la gente",real
"Hay una señora mayor atrapada dentro de su casa y el agua sigue subiendo",real
"La avenida Díaz Mirón está totalmente inundada, no pasan los carros",real
"Se vino un deslave en el cerro y tapó el camino a la comunidad",real
... (así hasta ~200 renglones)
```

Reglas del CSV:
- Si el texto lleva comas, enciérralo entre **comillas** `"..."` (como en los ejemplos).
- Un reporte por renglón. Sin renglones vacíos.

---

## Paso 3 — Clasifícalos con la herramienta

Abre PowerShell en la carpeta del proyecto y corre:

```powershell
cd datos-modelo
py herramienta_etiquetado.py --entrada reportes_ricardo.csv --origen real
```

1. Abre en el navegador **http://localhost:8080**
2. Escribe tu nombre: **`ricardo`** (todo en minúsculas, importante).
3. Para cada reporte elige **categoría** y **urgencia**:
   - Teclas **1–7** = categoría · teclas **A / M / B** = urgencia · **Enter** = guardar y siguiente.
4. Cuando salga "¡Listo!", terminaste.

Se guarda solo en `corpus_etiquetado.csv`. No toques ese archivo.

---

## Paso 4 — El doble etiquetado (esto lo hacen tú y Nahum juntos)

Después de que tú y Nahum terminen sus archivos, yo (Alexis) armo un archivo chico
**`reportes_kappa.csv`** (~180 reportes) y les aviso. **Los dos** lo van a clasificar
por separado (tú como `ricardo`, Nahum como `nahum`), sin verse. Es rapidísimo con la
herramienta y es lo que el profesor exige para probar que las etiquetas son objetivas.

Cuando te avise, correrás:
```powershell
py herramienta_etiquetado.py --entrada reportes_kappa.csv --origen real
```
y clasificas con el nombre **`ricardo`** otra vez.

---

## Resumen de lo tuyo
- [ ] Leí la guía `guia_etiquetado.md`.
- [ ] Llené `reportes_ricardo.csv` con ~200 reportes reales **anonimizados**.
- [ ] Los clasifiqué con la herramienta (nombre `ricardo`).
- [ ] (Cuando Alexis avise) clasifiqué `reportes_kappa.csv`.

Cualquier duda me dices. ¡Gracias!
