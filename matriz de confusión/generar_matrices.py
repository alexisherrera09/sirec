# -*- coding: utf-8 -*-
"""
Genera `matrices_confusion.md` con las matrices de confusion completas de SIREC.

Cubre las dos tareas (categoria de 7 clases y urgencia de 3 niveles) para los dos
modelos (baseline clasico y BETO), evaluados sobre el MISMO conjunto de prueba:
los 180 reportes reales del gold adjudicado por consenso (`gold_kappa.csv`).

Cubre el requisito del objetivo especifico 5 del documento academico:
"metricas por clase (precision, exhaustividad y medida F1) y matriz de confusion".

BASELINE  -> se reentrena aqui mismo. Es determinista (semilla 42, scikit-learn),
             asi que reproduce exactamente las cifras del capitulo 6.
BETO      -> NO se reentrena. Solo inferencia sobre el gold con los pesos ya
             entrenados. La inferencia es determinista (modo eval, sin dropout),
             asi que tambien reproduce las cifras del capitulo 6.

Uso:
    py generar_matrices.py                      # baseline + BETO si estan los pesos
    py generar_matrices.py --solo-baseline      # omite BETO
    py generar_matrices.py --modelos RUTA       # carpeta con beto_categoria/ y beto_urgencia/

Dependencias: scikit-learn, pandas, numpy  (+ torch y transformers para BETO)
"""

import argparse
import os
import sys

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.metrics import confusion_matrix, precision_recall_fscore_support

# --------------------------------------------------------------------------
# Rutas y constantes  (identicas a datos-modelo/entrenar_baseline.py)
# --------------------------------------------------------------------------
BASE = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(BASE)
DATOS = os.path.join(RAIZ, "datos-modelo")

REAL = os.path.join(DATOS, "corpus_etiquetado.csv")
SINT = os.path.join(DATOS, "corpus_sintetico.csv")
GOLD = os.path.join(DATOS, "gold_kappa.csv")

MODELOS_DEF = os.path.join(RAIZ, "microservicio-ml", "modelos")
SALIDA = os.path.join(BASE, "matrices_confusion.md")

CRITICO = {"categoria": "persona_en_riesgo", "urgencia": "alta"}
SEED = 42

# Modelo que el documento academico reporta como mejor en cada tarea.
MEJOR_BASELINE = {"categoria": "LinearSVM", "urgencia": "LogReg"}


def norm(t):
    return " ".join(str(t or "").lower().split())


# --------------------------------------------------------------------------
# Datos: mismo split sin fuga que usa el capitulo 6
# --------------------------------------------------------------------------
def cargar_split(con_sintetico=True):
    """Test = 180 gold adjudicados. Train = reales restantes (+ sinteticos)."""
    real = pd.read_csv(REAL, encoding="utf-8-sig")
    real = real[real["origen"] == "real"].copy()
    gold = pd.read_csv(GOLD, encoding="utf-8-sig")

    textos_gold = {norm(t) for t in gold["texto"]}
    train = real[~real["texto"].map(norm).isin(textos_gold)].copy()

    if con_sintetico:
        sint = pd.read_csv(SINT, encoding="utf-8-sig")
        train = pd.concat([train, sint], ignore_index=True)

    return train.reset_index(drop=True), gold.reset_index(drop=True)


# --------------------------------------------------------------------------
# Baseline: TF-IDF (palabra + caracter) + clasificador lineal
# --------------------------------------------------------------------------
def construir_pipeline(clf):
    return Pipeline([
        ("tfidf", FeatureUnion([
            ("palabra", TfidfVectorizer(
                lowercase=True, ngram_range=(1, 2), min_df=2, max_features=20000,
                strip_accents="unicode", sublinear_tf=True)),
            ("caracter", TfidfVectorizer(
                lowercase=True, analyzer="char_wb", ngram_range=(3, 5), min_df=2,
                max_features=40000, strip_accents="unicode", sublinear_tf=True)),
        ])),
        ("clf", clf),
    ])


def modelos_baseline():
    return {
        "LogReg": LogisticRegression(max_iter=2000, class_weight="balanced", C=3.0),
        "LinearSVM": LinearSVC(class_weight="balanced", C=1.0),
    }


def predecir_baseline(tarea, nombre_modelo, train, gold):
    clf = modelos_baseline()[nombre_modelo]
    pipe = construir_pipeline(clf)
    pipe.fit(train["texto"].astype(str).values, train[tarea].astype(str).values)
    y_pred = pipe.predict(gold["texto"].astype(str).values)
    return list(gold[tarea].astype(str).values), list(y_pred)


# --------------------------------------------------------------------------
# BETO: solo inferencia sobre el gold
# --------------------------------------------------------------------------
def predecir_beto(tarea, gold, carpeta_modelos, lote=16):
    import torch
    from transformers import AutoTokenizer, AutoModelForSequenceClassification

    ruta = os.path.join(carpeta_modelos, "beto_" + tarea)
    if not os.path.isdir(ruta):
        raise FileNotFoundError(ruta)

    tok = AutoTokenizer.from_pretrained(ruta)
    mdl = AutoModelForSequenceClassification.from_pretrained(ruta)
    mdl.eval()

    id2lab = mdl.config.id2label
    textos = [str(t) for t in gold["texto"].values]
    preds = []

    with torch.no_grad():
        for i in range(0, len(textos), lote):
            enc = tok(textos[i:i + lote], truncation=True, max_length=128,
                      padding=True, return_tensors="pt")
            logits = mdl(**enc).logits
            for j in logits.argmax(dim=1).tolist():
                preds.append(id2lab[j])

    return list(gold[tarea].astype(str).values), preds


# --------------------------------------------------------------------------
# Render en Markdown
# --------------------------------------------------------------------------
def tabla_matriz(y_true, y_pred, etiquetas):
    """Matriz de confusion como tabla Markdown. Diagonal en negrita."""
    m = confusion_matrix(y_true, y_pred, labels=etiquetas)
    out = []
    out.append("| real \\ predicho | " + " | ".join("`%s`" % e for e in etiquetas) + " | **Total** |")
    out.append("|---" * (len(etiquetas) + 2) + "|")
    for i, e in enumerate(etiquetas):
        celdas = []
        for j in range(len(etiquetas)):
            v = int(m[i][j])
            celdas.append("**%d**" % v if i == j else ("%d" % v if v else "·"))
        out.append("| **`%s`** | %s | %d |" % (e, " | ".join(celdas), int(m[i].sum())))
    tot = ["%d" % int(m[:, j].sum()) for j in range(len(etiquetas))]
    out.append("| **Total** | " + " | ".join(tot) + " | **%d** |" % int(m.sum()))
    return "\n".join(out)


def tabla_metricas(y_true, y_pred, etiquetas, critico):
    """Precision / recall / F1 / soporte por clase, + falsos negativos."""
    p, r, f, s = precision_recall_fscore_support(
        y_true, y_pred, labels=etiquetas, zero_division=0)
    yt, yp = np.array(y_true), np.array(y_pred)

    out = []
    out.append("| Clase | Precisión | Exhaustividad (recall) | F1 | Soporte | Falsos negativos |")
    out.append("|---|---:|---:|---:|---:|---:|")
    for i, e in enumerate(etiquetas):
        pos = yt == e
        fn = int(np.sum(pos & (yp != e)))
        marca = " ⚠️" if e == critico else ""
        out.append("| `%s`%s | %.3f | %.3f | %.3f | %d | %d / %d |"
                   % (e, marca, p[i], r[i], f[i], int(s[i]), fn, int(pos.sum())))
    macro_f1 = float(np.mean(f))
    acc = float(np.mean(yt == yp))
    out.append("| **Macro promedio** | **%.3f** | **%.3f** | **%.3f** | %d | — |"
               % (float(np.mean(p)), float(np.mean(r)), macro_f1, int(s.sum())))
    return "\n".join(out), macro_f1, acc


def principales_confusiones(y_true, y_pred, etiquetas, top=5):
    """Pares real->predicho mas frecuentes fuera de la diagonal."""
    m = confusion_matrix(y_true, y_pred, labels=etiquetas)
    pares = []
    for i, a in enumerate(etiquetas):
        for j, b in enumerate(etiquetas):
            if i != j and m[i][j] > 0:
                pares.append((int(m[i][j]), a, b))
    pares.sort(reverse=True)
    out = ["| Real | Predicho como | Casos |", "|---|---|---:|"]
    for n, a, b in pares[:top]:
        out.append("| `%s` | `%s` | %d |" % (a, b, n))
    return "\n".join(out)


def bloque(titulo, y_true, y_pred, etiquetas, critico):
    met, macro_f1, acc = tabla_metricas(y_true, y_pred, etiquetas, critico)
    partes = [
        "### %s" % titulo,
        "",
        "**Accuracy:** %.3f · **Macro-F1:** %.3f · *n* = %d" % (acc, macro_f1, len(y_true)),
        "",
        "#### Matriz de confusión",
        "",
        tabla_matriz(y_true, y_pred, etiquetas),
        "",
        "#### Métricas por clase",
        "",
        met,
        "",
        "#### Principales confusiones",
        "",
        principales_confusiones(y_true, y_pred, etiquetas),
        "",
    ]
    return "\n".join(partes)


# --------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--solo-baseline", action="store_true",
                    help="No intenta cargar BETO.")
    ap.add_argument("--modelos", default=MODELOS_DEF,
                    help="Carpeta que contiene beto_categoria/ y beto_urgencia/.")
    args = ap.parse_args()

    print("Cargando split (test = 180 gold, sin fuga)...")
    train, gold = cargar_split(con_sintetico=True)
    print("  train = %d  |  test gold = %d" % (len(train), len(gold)))

    doc = []
    doc.append("# Matrices de confusión — SIREC")
    doc.append("")
    doc.append("> Generado automáticamente por `generar_matrices.py`.")
    doc.append("> Conjunto de prueba: **%d reportes reales** del gold adjudicado por consenso" % len(gold))
    doc.append("> (`datos-modelo/gold_kappa.csv`). Entrenamiento: %d ejemplos" % len(train))
    doc.append("> (reales restantes + sintéticos declarados). Sin fuga: el gold nunca se usó para entrenar.")
    doc.append("")
    doc.append("Cubre el objetivo específico 5 del documento académico: *\"métricas por clase")
    doc.append("(precisión, exhaustividad y medida F1) y matriz de confusión\"*.")
    doc.append("")
    doc.append("**Cómo leer las matrices:** las **filas** son la clase real (etiqueta de consenso")
    doc.append("humano) y las **columnas** la clase que predijo el modelo. La diagonal en negrita son")
    doc.append("los aciertos; todo lo que está fuera de la diagonal es un error. El punto `·` es cero.")
    doc.append("")
    doc.append("---")
    doc.append("")

    pos_resumen = len(doc)   # el resumen comparativo se inserta aqui al final
    resumen = []

    for tarea in ("categoria", "urgencia"):
        etiquetas = sorted(pd.unique(gold[tarea].astype(str)))
        critico = CRITICO[tarea]
        nombre_tarea = "Categoría temática (7 clases)" if tarea == "categoria" \
            else "Nivel de urgencia (3 niveles)"

        doc.append("## %s" % nombre_tarea)
        doc.append("")
        doc.append("Clase crítica: `%s` (los falsos negativos aquí son el error más grave)." % critico)
        doc.append("")

        # --- baseline ---
        nombre_bl = MEJOR_BASELINE[tarea]
        print("Baseline %s / %s ..." % (nombre_bl, tarea))
        yt, yp = predecir_baseline(tarea, nombre_bl, train, gold)
        doc.append(bloque("Modelo de referencia — TF-IDF + %s" % nombre_bl,
                          yt, yp, etiquetas, critico))
        _, f_bl, a_bl = tabla_metricas(yt, yp, etiquetas, critico)

        # --- BETO ---
        f_bt = a_bt = None
        if not args.solo_baseline:
            try:
                print("BETO / %s ..." % tarea)
                yt2, yp2 = predecir_beto(tarea, gold, args.modelos)
                doc.append(bloque("BETO ajustado (modelo desplegado)",
                                  yt2, yp2, etiquetas, critico))
                _, f_bt, a_bt = tabla_metricas(yt2, yp2, etiquetas, critico)
            except FileNotFoundError as e:
                print("  [!] Pesos no encontrados: %s" % e)
                doc.append("### BETO ajustado (modelo desplegado)")
                doc.append("")
                doc.append("> ⏳ **Pendiente.** No se encontraron los pesos en `%s`." % args.modelos)
                doc.append("> Ver `INSTRUCCIONES.md`, paso 2, para colocarlos y volver a ejecutar.")
                doc.append("")
            except ImportError as e:
                print("  [!] Falta libreria: %s" % e)
                doc.append("### BETO ajustado (modelo desplegado)")
                doc.append("")
                doc.append("> ⏳ **Pendiente.** Falta `torch` o `transformers`: `py -m pip install torch transformers`.")
                doc.append("")

        resumen.append((nombre_tarea, a_bl, f_bl, a_bt, f_bt))
        doc.append("---")
        doc.append("")

    # --- resumen comparativo, insertado justo despues del encabezado ---
    cab = ["## Resumen comparativo", "",
           "| Tarea | Accuracy baseline | Macro-F1 baseline | Accuracy BETO | Macro-F1 BETO |",
           "|---|---:|---:|---:|---:|"]
    for n, a1, f1v, a2, f2v in resumen:
        c3 = "%.3f" % a2 if a2 is not None else "⏳ pendiente"
        c4 = "%.3f" % f2v if f2v is not None else "⏳ pendiente"
        cab.append("| %s | %.3f | %.3f | %s | %s |" % (n, a1, f1v, c3, c4))
    cab += ["", "---", ""]
    doc[pos_resumen:pos_resumen] = cab

    with open(SALIDA, "w", encoding="utf-8") as fh:
        fh.write("\n".join(doc).rstrip() + "\n")

    print("\nEscrito: %s" % SALIDA)


if __name__ == "__main__":
    sys.exit(main())
