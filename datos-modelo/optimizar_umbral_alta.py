# -*- coding: utf-8 -*-
"""
Optimización del recall de urgencia=alta (Fase D4, mejora) — SIREC.

En triage de emergencias un FALSO NEGATIVO de urgencia `alta` (clasificar como `media`
algo que era urgente) es más grave que un falso positivo. Este script mide el compromiso
recall↔precisión de `alta` al bajar el UMBRAL de decisión, con TF-IDF palabra+carácter,
en 5-fold CV sobre el corpus real. Sirve para elegir y justificar el punto de operación.

Uso:
    py optimizar_umbral_alta.py

Solo compara; no guarda modelo. Reproducible (semilla 42).
"""
import os
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import f1_score, recall_score, precision_score

BASE = os.path.dirname(os.path.abspath(__file__))
CLASSES = np.array(["alta", "baja", "media"])  # orden fijo
ALTA = 0


def vectorizador():
    return FeatureUnion([
        ("palabra", TfidfVectorizer(lowercase=True, ngram_range=(1, 2), min_df=2,
                                    max_features=20000, strip_accents="unicode", sublinear_tf=True)),
        ("caracter", TfidfVectorizer(lowercase=True, analyzer="char_wb", ngram_range=(3, 5),
                                     min_df=2, max_features=40000, strip_accents="unicode", sublinear_tf=True)),
    ])


def oof_proba(X, y):
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    proba = np.zeros((len(y), 3))
    for tr, te in skf.split(X, y):
        pipe = Pipeline([("v", vectorizador()),
                         ("c", LogisticRegression(max_iter=3000, C=3.0, class_weight="balanced"))])
        pipe.fit(X[tr], y[tr])
        cols = list(pipe.named_steps["c"].classes_)
        idx = [cols.index(c) for c in CLASSES]
        proba[te] = pipe.predict_proba(X[te])[:, idx]
    return proba


def pred_umbral(proba, tau):
    """Si P(alta) >= tau -> 'alta'; si no, argmax entre baja/media."""
    return np.where(proba[:, ALTA] >= tau, "alta",
                    CLASSES[1:][np.argmax(proba[:, 1:], axis=1)])


def fila(y, y_pred, etiqueta):
    rec = recall_score(y, y_pred, labels=["alta"], average="macro", zero_division=0)
    pre = precision_score(y, y_pred, labels=["alta"], average="macro", zero_division=0)
    f1a = f1_score(y, y_pred, labels=["alta"], average="macro", zero_division=0)
    mf1 = f1_score(y, y_pred, average="macro", zero_division=0)
    fn = int(np.sum((y == "alta") & (y_pred != "alta")))
    print("%-34s  recall=%.3f  prec=%.3f  F1=%.3f  FN=%3d/%d  macroF1=%.3f"
          % (etiqueta, rec, pre, f1a, fn, int(np.sum(y == "alta")), mf1))


def main():
    df = pd.read_csv(os.path.join(BASE, "corpus_etiquetado.csv"), encoding="utf-8-sig")
    df = df[df["origen"] == "real"]
    X = df["texto"].astype(str).values
    y = df["urgencia"].astype(str).values
    print("Corpus real: %d reportes | 'alta' reales: %d" % (len(y), int(np.sum(y == "alta"))))
    print("Modelo: TF-IDF palabra+carácter + LogReg(balanced), 5-fold CV\n")
    proba = oof_proba(X, y)
    fila(y, CLASSES[np.argmax(proba, axis=1)], "argmax (referencia)")
    for tau in [0.45, 0.40, 0.35, 0.30, 0.25, 0.20]:
        fila(y, pred_umbral(proba, tau), "umbral alta >= %.2f" % tau)
    print("\nGuía de elección: umbral ~0.30 maximiza recall de 'alta' sin degradar el macro-F1 global; "
          "bajar más sube el recall pero castiga la precisión. Elegir según cuánta sobre-alerta tolera el operador.")


if __name__ == "__main__":
    main()
