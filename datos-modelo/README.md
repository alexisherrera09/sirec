# Datos, entrenamiento y evaluación — SIREC (Componente D)

Materializa los requisitos del evaluador: categorías fijas, trazabilidad del corpus,
procedimiento de etiquetado con kappa de Cohen, criterio de urgencia explícito y baseline
con métricas por clase.

## Estado de las fases

| Fase | Qué es | Estado |
|---|---|---|
| D1 | `guia_etiquetado.md` — guía de etiquetado (7 categorías, criterio de urgencia, 7 casos frontera) | ✅ Hecha (falta **[HUMANO]** aprobarla) |
| D2 | `herramienta_etiquetado.py` — app local de etiquetado (individual + doble) | ✅ Hecha y probada |
| D3.1 | `generar_corpus_sintetico.py` → `corpus_sintetico.csv` (900 reportes sintéticos) | ✅ Hecha |
| D3.2 | ~300–400 reportes **reales** recolectados, anonimizados y etiquetados | ⏳ **[HUMANO]** |
| D3.3 | Doble etiquetado de ~150–200 reales (dos personas) para el kappa | ⏳ **[HUMANO]** |
| D3.4 | `calcular_kappa.py` + `reporte_corpus.md` (trazabilidad + kappa) | ⏳ Pendiente (tras D3.2/D3.3) |
| D4 | `entrenar_baseline.py` (TF-IDF + LogReg/SVM) + `resultados_baseline.md` | ⏳ Pendiente |
| D5 | `entrenar_beto_colab.ipynb` (Colab) + `comparacion_modelos.md` | ⏳ Pendiente |
| D6 | Exportar modelo e integrar en el microservicio (Fase A2) | ⏳ Pendiente |

## Qué le toca al equipo humano (no delegable)

1. **Leer y aprobar** `guia_etiquetado.md` (o pedir ajustes).
2. **Recolectar ~300–400 reportes reales** (redes de contingencias pasadas, notas de prensa,
   transcripciones), **anonimizarlos** y ponerlos en `reportes_sin_etiquetar.csv` (columna `texto`).
   El conjunto de prueba se forma **exclusivamente** con estos.
3. **Etiquetarlos** con la herramienta (D2).
4. **Doble etiquetado**: dos personas etiquetan de forma independiente ~150–200 reportes reales
   (cada una con un nombre de etiquetador distinto) para el kappa de Cohen. **No lo hace la IA.**

## Cómo etiquetar (herramienta D2)

```powershell
cd datos-modelo
py herramienta_etiquetado.py --entrada reportes_sin_etiquetar.csv --origen real
```
Abre http://localhost:8080, escribe tu nombre de etiquetador y clasifica (atajos: teclas
1–7 para categoría, A/M/B para urgencia, Enter para guardar). Resultado en `corpus_etiquetado.csv`.

Para el **doble etiquetado**: dos personas usan la misma entrada con nombres distintos
(ej. `ana`, `luis`); cada una etiqueta el subconjunto de forma independiente.

## Generar el corpus sintético (reproducible)

```powershell
py generar_corpus_sintetico.py
```
Genera `corpus_sintetico.csv` (semilla fija). Todos los registros llevan `origen=sintetico`.
**Nunca se usa para el conjunto de prueba.**

## Archivos

| Archivo | Función |
|---|---|
| `guia_etiquetado.md` | Guía de etiquetado (D1) |
| `herramienta_etiquetado.py` | Herramienta de etiquetado local (D2) |
| `generar_corpus_sintetico.py` | Generador del corpus sintético (D3.1) |
| `corpus_sintetico.csv` | 900 reportes sintéticos etiquetados (train/val) |
| `reportes_sin_etiquetar.csv` | **[HUMANO]** reportes reales a etiquetar (plantilla incluida) |
| `corpus_etiquetado.csv` | Salida de la herramienta (se crea al etiquetar) |
