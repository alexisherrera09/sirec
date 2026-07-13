# -*- coding: utf-8 -*-
"""
Genera reporte_corpus.md (trazabilidad exigida por el evaluador) a partir de
corpus_etiquetado.csv (real) y corpus_sintetico.csv. Reejecutar cuando el corpus cambie:

    py generar_reporte_corpus.py

Solo usa la librería estándar.
"""
import csv, io, collections, os

BASE = os.path.dirname(os.path.abspath(__file__))
REAL = os.path.join(BASE, "corpus_etiquetado.csv")
SINT = os.path.join(BASE, "corpus_sintetico.csv")
OUT  = os.path.join(BASE, "reporte_corpus.md")

CATS = ["persona_en_riesgo", "inundacion", "caida_poste_cable", "deslave",
        "incendio", "dano_estructural", "otro"]
URGS = ["alta", "media", "baja"]


def load(p):
    with io.open(p, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def dist(rows, key):
    return collections.Counter((r.get(key) or "").strip() for r in rows)


def main():
    real = [r for r in load(REAL) if (r.get("origen") or "").strip() == "real"]
    sint = load(SINT) if os.path.exists(SINT) else []
    rc, ru = dist(real, "categoria"), dist(real, "urgencia")
    sc, su = dist(sint, "categoria"), dist(sint, "urgencia")
    tot_real, tot_sint = len(real), len(sint)
    tot = tot_real + tot_sint
    pct = lambda n, d: ("%.1f%%" % (100.0 * n / d)) if d else "0%"

    cross = collections.defaultdict(collections.Counter)
    for r in real:
        cross[(r.get("etiquetador") or "").strip()][(r.get("categoria") or "").strip()] += 1

    L = []
    A = L.append
    A("# Reporte de trazabilidad del corpus — SIREC\n")
    A("> Requisito del evaluador: origen cuantificado de los reportes (% real / % sintético) y")
    A("> distribución por clase. El **conjunto de prueba del modelo es 100% real** (regla innegociable).")
    A("> Generado automáticamente a partir de `corpus_etiquetado.csv` (real) y `corpus_sintetico.csv`.\n")
    A("## 1. Origen de los datos (trazabilidad)\n")
    A("| Origen | Reportes | % del total | Uso |")
    A("|---|---:|---:|---|")
    A("| `real` (recolectado y anonimizado) | %d | %s | Entrenamiento + **conjunto de prueba** |" % (tot_real, pct(tot_real, tot)))
    A("| `sintetico` (generado con IA, declarado) | %d | %s | Solo aumento de entrenamiento; **nunca** en prueba |" % (tot_sint, pct(tot_sint, tot)))
    A("| `redactado` (reescrito por el equipo) | 0 | 0.0% | — |")
    A("| **Total** | **%d** | **100%%** | |\n" % tot)
    A("Los %d reportes reales fueron recolectados y etiquetados por integrantes del equipo a partir" % tot_real)
    A("de publicaciones públicas de contingencias en Veracruz, anonimizados según la guía de etiquetado.\n")
    A("## 2. Distribución por categoría\n")
    A("| Categoría | Real | Sintético | Total |")
    A("|---|---:|---:|---:|")
    for c in CATS:
        A("| `%s` | %d | %d | %d |" % (c, rc.get(c, 0), sc.get(c, 0), rc.get(c, 0) + sc.get(c, 0)))
    A("| **Total** | **%d** | **%d** | **%d** |\n" % (tot_real, tot_sint, tot))
    A("## 3. Distribución por urgencia\n")
    A("| Urgencia | Real | Sintético | Total |")
    A("|---|---:|---:|---:|")
    for u in URGS:
        A("| `%s` | %d | %d | %d |" % (u, ru.get(u, 0), su.get(u, 0), ru.get(u, 0) + su.get(u, 0)))
    A("| **Total** | **%d** | **%d** | **%d** |\n" % (tot_real, tot_sint, tot))
    A("## 4. Corpus real por anotador (categoría)\n")
    A("| Anotador | " + " | ".join("`%s`" % c for c in CATS) + " | Total |")
    A("|---" * (len(CATS) + 2) + "|")
    for e in sorted(cross):
        A("| %s | " % e + " | ".join(str(cross[e].get(c, 0)) for c in CATS) + " | %d |" % sum(cross[e].values()))
    A("")
    with io.open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    print("Escrito:", OUT, "| real=%d sintetico=%d" % (tot_real, tot_sint))


if __name__ == "__main__":
    main()
