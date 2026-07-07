# Nahum — tu tarea (paso a paso)

Hola Nahum. Me estás ayudando con la parte de datos de mi proyecto de maestría (SIREC,
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

**Archivo que vas a llenar:** `datos-modelo/reportes_nahum.csv`

Un renglón por reporte. Solo importa la columna **`texto`**; deja la columna **`origen`** como **`real`**.

**De dónde sacarlos (tienen que ser reales, no inventados):**
- Publicaciones públicas de redes sociales durante contingencias pasadas en Veracruz
  (inundaciones, nortes, deslaves): Facebook de grupos de colonias, X/Twitter, etc.
- Notas de prensa que citen reportes de ciudadanos.
- Transcripciones de reportes o llamadas, si tienes acceso.

> **Para no repetir con Ricardo:** ponte de acuerdo con él para cubrir fuentes o eventos
> distintos (ej. tú los nortes/deslaves, él las inundaciones urbanas), o distintas fechas/colonias.

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
Tu `reportes_nahum.csv` debe verse así — **borra el renglón de instrucciones que trae** y pega los tuyos:

```csv
texto,origen
"Se está deslavando el cerro arriba de las casas y la gente sigue adentro",real
"Hay un cable chispeando en plena avenida y hay niños jugando cerca",real
"El techo de la bodega se colapsó con la lluvia y había trabajadores adentro",real
"Un niño fue arrastrado por la corriente en el arroyo, ayuda urgente",real
"¿A qué hora reabren el albergue de la colonia Formando Hogar?",real
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
py herramienta_etiquetado.py --entrada reportes_nahum.csv --origen real
```

1. Abre en el navegador **http://localhost:8080**
2. Escribe tu nombre: **`nahum`** (todo en minúsculas, importante).
3. Para cada reporte elige **categoría** y **urgencia**:
   - Teclas **1–7** = categoría · teclas **A / M / B** = urgencia · **Enter** = guardar y siguiente.
4. Cuando salga "¡Listo!", terminaste.

Se guarda solo en `corpus_etiquetado.csv`. No toques ese archivo.

---

## Paso 4 — El doble etiquetado (esto lo hacen tú y Ricardo juntos)

Después de que tú y Ricardo terminen sus archivos, yo (Alexis) armo un archivo chico
**`reportes_kappa.csv`** (~180 reportes) y les aviso. **Los dos** lo van a clasificar
por separado (tú como `nahum`, Ricardo como `ricardo`), sin verse. Es rapidísimo con la
herramienta y es lo que el profesor exige para probar que las etiquetas son objetivas.

Cuando te avise, correrás:
```powershell
py herramienta_etiquetado.py --entrada reportes_kappa.csv --origen real
```
y clasificas con el nombre **`nahum`** otra vez.

---

## Resumen de lo tuyo
- [ ] Leí la guía `guia_etiquetado.md`.
- [ ] Llené `reportes_nahum.csv` con ~200 reportes reales **anonimizados**.
- [ ] Los clasifiqué con la herramienta (nombre `nahum`).
- [ ] (Cuando Alexis avise) clasifiqué `reportes_kappa.csv`.

Cualquier duda me dices. ¡Gracias!
