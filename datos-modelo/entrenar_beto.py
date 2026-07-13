"""
Fine-tuning de BETO (Fase D5) — SIREC.

Ajusta `dccuchile/bert-base-spanish-wwm-cased` (BETO) para las dos tareas de clasificación
del proyecto: `categoria` (7 clases) y `urgencia` (3 clases). Entrena un modelo por tarea.

Diseñado para correr en Google Colab con GPU gratuita (o cualquier máquina con GPU).
El modelo entrenado se exporta para que el microservicio Python (FastAPI) lo sirva,
reemplazando el modo simulado SIN cambiar el contrato de datos.

Requisitos del evaluador integrados:
  - Conjunto de prueba 100% real (origen=real); los sintéticos solo aumentan el entrenamiento.
  - Métricas POR CLASE + foco en recall de clases críticas (persona_en_riesgo / urgencia alta).
  - Pérdida ponderada por clase (class weights) para el fuerte desbalance del corpus real.

Uso (Colab):
    !pip install "transformers>=4.40" "datasets>=2.19" "accelerate>=0.30" scikit-learn pandas
    !python entrenar_beto.py --tarea categoria --con-sintetico --salida ./beto_categoria
    !python entrenar_beto.py --tarea urgencia  --con-sintetico --salida ./beto_urgencia

Ver también el cuaderno equivalente: entrenar_beto_colab.ipynb (mismo flujo, celda por celda).
"""

import argparse
import os
import numpy as np
import pandas as pd
import torch
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, f1_score, recall_score
from sklearn.utils.class_weight import compute_class_weight
from datasets import Dataset
from transformers import (
    AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer,
)

MODELO_BASE = "dccuchile/bert-base-spanish-wwm-cased"
CRITICO = {"categoria": "persona_en_riesgo", "urgencia": "alta"}
SEED = 42


def cargar(base, tarea, con_sintetico):
    real = pd.read_csv(os.path.join(base, "corpus_etiquetado.csv"), encoding="utf-8-sig")
    real = real[real["origen"] == "real"].copy()
    # Test 100% real: separamos ANTES de mezclar sintéticos.
    tr, te = train_test_split(real, test_size=0.25, stratify=real[tarea], random_state=SEED)
    if con_sintetico:
        sint = pd.read_csv(os.path.join(base, "corpus_sintetico.csv"), encoding="utf-8-sig")
        tr = pd.concat([tr, sint], ignore_index=True)
        print("Entrenamiento aumentado con %d sintéticos. Test = %d, 100%% real." % (len(sint), len(te)))
    return tr.reset_index(drop=True), te.reset_index(drop=True)


class TrainerPonderado(Trainer):
    """Trainer con pérdida ponderada por clase (para el desbalance del corpus real)."""
    def __init__(self, pesos, *a, **k):
        super().__init__(*a, **k)
        self.pesos = pesos

    def compute_loss(self, model, inputs, return_outputs=False, **kwargs):
        labels = inputs.pop("labels")
        out = model(**inputs)
        loss = torch.nn.functional.cross_entropy(
            out.logits, labels, weight=self.pesos.to(out.logits.device))
        return (loss, out) if return_outputs else loss


def main():
    ap = argparse.ArgumentParser(description="Fine-tuning de BETO (SIREC D5).")
    ap.add_argument("--tarea", choices=["categoria", "urgencia"], required=True)
    ap.add_argument("--con-sintetico", action="store_true")
    ap.add_argument("--salida", default="./beto_modelo")
    ap.add_argument("--epocas", type=int, default=4)
    ap.add_argument("--batch", type=int, default=16)
    args = ap.parse_args()

    base = os.path.dirname(os.path.abspath(__file__))
    tr, te = cargar(base, args.tarea, args.con_sintetico)

    clases = sorted(pd.unique(pd.read_csv(
        os.path.join(base, "corpus_etiquetado.csv"), encoding="utf-8-sig")[args.tarea]))
    id2lab = {i: c for i, c in enumerate(clases)}
    lab2id = {c: i for i, c in id2lab.items()}

    tok = AutoTokenizer.from_pretrained(MODELO_BASE)

    def preparar(df):
        d = Dataset.from_pandas(pd.DataFrame({
            "text": df["texto"].astype(str).values,
            "labels": [lab2id[c] for c in df[args.tarea].astype(str).values],
        }))
        return d.map(lambda b: tok(b["text"], truncation=True, max_length=128), batched=True)

    ds_tr, ds_te = preparar(tr), preparar(te)

    # Pesos de clase a partir del entrenamiento.
    y_tr = np.array([lab2id[c] for c in tr[args.tarea].astype(str).values])
    pesos = compute_class_weight("balanced", classes=np.arange(len(clases)), y=y_tr)
    pesos_t = torch.tensor(pesos, dtype=torch.float)

    modelo = AutoModelForSequenceClassification.from_pretrained(
        MODELO_BASE, num_labels=len(clases), id2label=id2lab, label2id=lab2id)

    def metricas(pred):
        y = pred.label_ids
        yhat = np.argmax(pred.predictions, axis=1)
        crit_id = lab2id.get(CRITICO[args.tarea])
        rec_crit = recall_score(y, yhat, labels=[crit_id], average="macro", zero_division=0) \
            if crit_id is not None else 0.0
        return {"macro_f1": f1_score(y, yhat, average="macro", zero_division=0),
                "recall_critico": rec_crit}

    ta = TrainingArguments(
        output_dir=args.salida, num_train_epochs=args.epocas,
        per_device_train_batch_size=args.batch, per_device_eval_batch_size=args.batch,
        learning_rate=2e-5, eval_strategy="epoch", save_strategy="epoch",
        load_best_model_at_end=True, metric_for_best_model="recall_critico",
        seed=SEED, logging_steps=20, report_to="none")

    trainer = TrainerPonderado(
        pesos_t, model=modelo, args=ta, train_dataset=ds_tr, eval_dataset=ds_te,
        tokenizer=tok, compute_metrics=metricas)
    trainer.train()

    # Reporte final por clase sobre el test 100% real.
    pred = trainer.predict(ds_te)
    yhat = np.argmax(pred.predictions, axis=1)
    ynames = [id2lab[i] for i in pred.label_ids]
    phat = [id2lab[i] for i in yhat]
    print("\n=== BETO — %s — test 100%% real ===" % args.tarea)
    print(classification_report(ynames, phat, digits=3, zero_division=0))

    trainer.save_model(args.salida)
    tok.save_pretrained(args.salida)
    print("Modelo guardado en:", args.salida)


if __name__ == "__main__":
    main()
