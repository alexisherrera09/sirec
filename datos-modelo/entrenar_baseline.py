"""
Baseline clásico (Fase D4) — SIREC.

Modelo de referencia OBLIGATORIO exigido por el evaluador: TF-IDF + clasificador lineal
(Regresión Logística y SVM lineal), para comparar contra BETO. NO se despliega.

Requisitos del evaluador integrados:
  - Métricas POR CLASE (precisión, recall, F1) — no solo accuracy global.
  - Foco en RECALL y FALSOS NEGATIVOS de las clases críticas
    (categoría `persona_en_riesgo`, urgencia `alta`), porque en emergencias un falso
    negativo es más grave que otros errores.
  - El conjunto de prueba es 100% real (origen=real). Los datos sintéticos, si se usan,
    van SOLO en entrenamiento y se declara.

Uso:
    py entrenar_baseline.py                      # entrena solo con real (test = held-out real)
    py entrenar_baseline.py --con-sintetico      # aumenta el entrenamiento con corpus_sintetico
    py entrenar_baseline.py --cv                 # validación cruzada estratificada 5-fold (real)

Dependencias: scikit-learn, pandas, numpy  (ver requirements-modelo.txt)
"""

import argparse
import os
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_predict
from sklearn.metrics import classification_report, confusion_matrix, f1_score, recall_score

BASE = os.path.dirname(os.path.abspath(__file__))
REAL = os.path.join(BASE, "corpus_etiquetado.csv")
SINT = os.path.join(BASE, "corpus_sintetico.csv")

CRITICO = {"categoria": "persona_en_riesgo", "urgencia": "alta"}
SEED = 42


def cargar():
    real = pd.read_csv(REAL, encoding="utf-8-sig")
    real = real[real["origen"] == "real"].copy()
    return real


def construir_pipeline(clf):
    # TF-IDF de palabra + de carácter (char_wb). Los n-gramas de carácter capturan
    # la violencia/gravedad ofuscada del corpus real (p.ej. "f4ll3c3", "bale4das",
    # "L3S10N4D4S") que los n-gramas de palabra no ven. Mejora uniforme medida en D4.
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


def modelos():
    return {
        "LogReg": LogisticRegression(max_iter=2000, class_weight="balanced", C=3.0),
        "LinearSVM": LinearSVC(class_weight="balanced", C=1.0),
    }


def evaluar(nombre_tarea, y_true, y_pred, etiquetas):
    print("\n" + "-" * 66)
    print("TAREA: %s" % nombre_tarea)
    print("-" * 66)
    print(classification_report(y_true, y_pred, labels=etiquetas, digits=3, zero_division=0))
    crit = CRITICO[nombre_tarea]
    if crit in etiquetas:
        # Falsos negativos de la clase crítica = casos crít. reales que el modelo NO detectó.
        yt = np.array(y_true); yp = np.array(y_pred)
        pos = yt == crit
        fn = int(np.sum(pos & (yp != crit)))
        rec = recall_score(yt, yp, labels=[crit], average="macro", zero_division=0)
        print(">>> Clase crítica '%s': recall = %.3f | falsos negativos = %d de %d reales"
              % (crit, rec, fn, int(pos.sum())))
    print("Matriz de confusión (filas=real, cols=predicho); orden = %s" % etiquetas)
    print(confusion_matrix(y_true, y_pred, labels=etiquetas))


def correr(df, tarea, con_sintetico, usar_cv):
    X = df["texto"].astype(str).values
    y = df[tarea].astype(str).values
    etiquetas = sorted(pd.unique(y))

    for nombre, clf in modelos().items():
        print("\n" + "=" * 66)
        print("MODELO: %s  |  TAREA: %s  |  %s"
              % (nombre, tarea, "5-fold CV (real)" if usar_cv else "holdout 75/25 (test 100% real)"))
        print("=" * 66)
        pipe = construir_pipeline(clf)

        if usar_cv:
            skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
            y_pred = cross_val_predict(pipe, X, y, cv=skf)
            evaluar(tarea, y, y_pred, etiquetas)
        else:
            Xtr, Xte, ytr, yte = train_test_split(
                X, y, test_size=0.25, stratify=y, random_state=SEED)
            if con_sintetico and os.path.exists(SINT):
                sint = pd.read_csv(SINT, encoding="utf-8-sig")
                Xtr = np.concatenate([Xtr, sint["texto"].astype(str).values])
                ytr = np.concatenate([ytr, sint[tarea].astype(str).values])
                print("Entrenamiento aumentado con %d sintéticos (declarado). Test sigue 100%% real."
                      % len(sint))
            pipe.fit(Xtr, ytr)
            evaluar(tarea, yte, pipe.predict(Xte), etiquetas)
            print("Macro-F1 test: %.3f" % f1_score(yte, pipe.predict(Xte), average="macro", zero_division=0))


def main():
    ap = argparse.ArgumentParser(description="Baseline TF-IDF + lineal (SIREC D4).")
    ap.add_argument("--con-sintetico", action="store_true",
                    help="Aumentar SOLO el entrenamiento con corpus_sintetico.csv (test sigue 100%% real).")
    ap.add_argument("--cv", action="store_true",
                    help="Validación cruzada estratificada 5-fold sobre el corpus real (más estable con pocas muestras).")
    args = ap.parse_args()

    df = cargar()
    print("Corpus real cargado: %d reportes (origen=real)." % len(df))
    for tarea in ("categoria", "urgencia"):
        correr(df, tarea, args.con_sintetico, args.cv)

    print("\nRecordatorio: este baseline es solo comparación; el modelo servido es BETO (D5). "
          "Prioriza recall en clases críticas por el criterio del evaluador.")


if __name__ == "__main__":
    main()
