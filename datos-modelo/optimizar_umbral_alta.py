# -*- coding: utf-8 -*-
"""
Optimización del recall de urgencia=alta (Fase D4, mejora) — SIREC.

En triage de emergencias un FALSO NEGATIVO de urgencia `alta` (clasificar como `media`
algo que era urgente) es más grave que un falso positivo. Este script mide el compromiso
recall↔precisión de `alta` al bajar el UMBRAL de decisión, con TF-IDF palabra+carácter,
en 5-fold CV sobre el corpus real. Sirve para elegir y justificar el punto de operación.

Uso:
    py optimizar_umbral_alta.py                 # 5-fold CV sobre el corpus real
    py optimizar_umbral_alta.py --gold-test     # entrena 220 reales + sintéticos; evalúa sobre 180 gold

Solo compara; no guarda modelo. Reproducible (semilla 42).
"""
import argparse
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


def norm(t):
    return " ".join(str(t or "").lower().split())


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


def proba_gold(con_sintetico):
    """Entrena con los 220 reales restantes (+ sintéticos opcionales) y devuelve
    (y_test_gold, proba_gold) sobre los 180 reportes gold adjudicados."""
    real = pd.read_csv(os.path.join(BASE, "corpus_etiquetado.csv"), encoding="utf-8-sig")
    real = real[real["origen"] == "real"]
    gold = pd.read_csv(os.path.join(BASE, "gold_kappa.csv"), encoding="utf-8-sig")
    textos_gold = {norm(t) for t in gold["texto"]}
    train = real[~real["texto"].map(norm).isin(textos_gold)]
    Xtr = train["texto"].astype(str).values
    ytr = train["urgencia"].astype(str).values
    if con_sintetico:
        sint = pd.read_csv(os.path.join(BASE, "corpus_sintetico.csv"), encoding="utf-8-sig")
        Xtr = np.concatenate([Xtr, sint["texto"].astype(str).values])
        ytr = np.concatenate([ytr, sint["urgencia"].astype(str).values])
    Xte = gold["texto"].astype(str).values
    yte = gold["urgencia"].astype(str).values
    pipe = Pipeline([("v", vectorizador()),
                     ("c", LogisticRegression(max_iter=3000, C=3.0, class_weight="balanced"))])
    pipe.fit(Xtr, ytr)
    cols = list(pipe.named_steps["c"].classes_)
    idx = [cols.index(c) for c in CLASSES]
    return yte, pipe.predict_proba(Xte)[:, idx], len(Xtr)


def main():
    ap = argparse.ArgumentParser(description="Umbral de recall de urgencia=alta (SIREC D4).")
    ap.add_argument("--gold-test", action="store_true",
                    help="Entrena 220 reales + sintéticos y evalúa el umbral sobre los 180 gold.")
    args = ap.parse_args()

    if args.gold_test:
        y, proba, n_tr = proba_gold(con_sintetico=True)
        print("Test = 180 gold adjudicado | entrenamiento = %d (220 reales + sintéticos)" % n_tr)
        print("'alta' en gold: %d | Modelo: TF-IDF palabra+carácter + LogReg(balanced)\n"
              % int(np.sum(y == "alta")))
    else:
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
