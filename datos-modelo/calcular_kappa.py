"""
Cálculo del kappa de Cohen (Fase D3.4) — SIREC.

Mide el acuerdo entre DOS anotadores humanos que etiquetaron el mismo subconjunto
de reportes de forma independiente (requisito del evaluador: el kappa demuestra que
las etiquetas son objetivas y no arbitrarias).

Solo usa la librería estándar de Python (no requiere instalar nada).

Entrada esperada: uno o más CSV con columnas
    texto, categoria, urgencia, etiquetador, origen
Cada uno de los dos anotadores etiquetó `reportes_kappa.csv` con la herramienta
(cada quien con su nombre), produciendo filas con etiquetador=<nombreA> y
etiquetador=<nombreB> para los MISMOS textos.

Uso típico (un archivo combinado que contiene a ambos):
    py calcular_kappa.py --entrada corpus_kappa_etiquetado.csv

O dos archivos separados (uno por anotador):
    py calcular_kappa.py --entrada kappa_ricardo.csv kappa_nahum.csv

Reporta kappa para `categoria` y para `urgencia`, el % de acuerdo bruto,
la interpretación (escala de Landis & Koch) y los desacuerdos por clase.
"""

import argparse
import csv
import io
import collections


def norm(t):
    return " ".join((t or "").lower().split())


def cargar(rutas):
    filas = []
    for ruta in rutas:
        with io.open(ruta, encoding="utf-8-sig", newline="") as f:
            for r in csv.DictReader(f):
                filas.append({
                    "texto": (r.get("texto") or "").strip(),
                    "categoria": (r.get("categoria") or "").strip(),
                    "urgencia": (r.get("urgencia") or "").strip(),
                    "etiquetador": (r.get("etiquetador") or "").strip(),
                })
    return filas


def kappa_cohen(pares):
    """pares: lista de (etiqueta_A, etiqueta_B). Devuelve (kappa, po, n, categorias)."""
    n = len(pares)
    if n == 0:
        return None, None, 0, []
    cats = sorted({a for a, _ in pares} | {b for _, b in pares})
    acuerdo = sum(1 for a, b in pares if a == b)
    po = acuerdo / n
    # Probabilidad esperada por azar.
    ca = collections.Counter(a for a, _ in pares)
    cb = collections.Counter(b for _, b in pares)
    pe = sum((ca[c] / n) * (cb[c] / n) for c in cats)
    kappa = (po - pe) / (1 - pe) if (1 - pe) != 0 else 1.0
    return kappa, po, n, cats


def interpretar(k):
    if k is None:
        return "sin datos"
    if k < 0:    return "pobre (peor que el azar)"
    if k < 0.20: return "leve (slight)"
    if k < 0.40: return "aceptable (fair)"
    if k < 0.60: return "moderado (moderate)"
    if k < 0.80: return "considerable (substantial)"
    return "casi perfecto (almost perfect)"


def emparejar(filas, campo):
    """Empareja por texto normalizado las etiquetas de exactamente dos anotadores."""
    etiquetadores = sorted({f["etiquetador"] for f in filas if f["etiquetador"]})
    if len(etiquetadores) != 2:
        raise SystemExit(
            "Se necesitan EXACTAMENTE dos anotadores distintos. Encontrados: %s" % etiquetadores)
    a, b = etiquetadores
    por_texto = collections.defaultdict(dict)
    for f in filas:
        if f["etiquetador"] in (a, b) and f[campo]:
            por_texto[norm(f["texto"])][f["etiquetador"]] = f[campo]
    pares = []
    solo_uno = 0
    for _, d in por_texto.items():
        if a in d and b in d:
            pares.append((d[a], d[b]))
        else:
            solo_uno += 1
    return (a, b), pares, solo_uno


def reporte(filas, campo):
    (a, b), pares, solo_uno = emparejar(filas, campo)
    k, po, n, cats = kappa_cohen(pares)
    print("\n" + "=" * 60)
    print("KAPPA DE COHEN — campo: %s   (anotadores: %s vs %s)" % (campo, a, b))
    print("=" * 60)
    print("Reportes emparejados (ambos etiquetaron): %d" % n)
    if solo_uno:
        print("Reportes que solo uno etiquetó (excluidos): %d" % solo_uno)
    if n == 0:
        print("No hay pares comparables.")
        return
    print("Acuerdo bruto (po): %.3f  (%d/%d idénticos)" % (po, round(po * n), n))
    print("Kappa de Cohen: %.3f  ->  %s" % (k, interpretar(k)))
    # Desacuerdos por combinación de clases.
    desac = collections.Counter((x, y) for x, y in pares if x != y)
    if desac:
        print("\nPrincipales desacuerdos (%s_%s -> %s_%s : conteo):" % (a, "", b, ""))
        for (x, y), c in desac.most_common(12):
            print("   %-22s vs %-22s : %d" % (x, y, c))
    # Recall crítico: coincidencia en las clases sensibles.
    if campo == "categoria":
        criticos = [(x, y) for x, y in pares if x == "persona_en_riesgo" or y == "persona_en_riesgo"]
        ok = sum(1 for x, y in criticos if x == y)
        if criticos:
            print("\nAcuerdo en 'persona_en_riesgo' (clase crítica): %d/%d = %.1f%%"
                  % (ok, len(criticos), 100.0 * ok / len(criticos)))
    if campo == "urgencia":
        criticos = [(x, y) for x, y in pares if x == "alta" or y == "alta"]
        ok = sum(1 for x, y in criticos if x == y)
        if criticos:
            print("\nAcuerdo en urgencia 'alta' (clase crítica): %d/%d = %.1f%%"
                  % (ok, len(criticos), 100.0 * ok / len(criticos)))


def main():
    ap = argparse.ArgumentParser(description="Kappa de Cohen entre dos anotadores (SIREC D3.4).")
    ap.add_argument("--entrada", nargs="+", default=["corpus_kappa_etiquetado.csv"],
                    help="Uno o dos CSV con columnas texto,categoria,urgencia,etiquetador,origen.")
    args = ap.parse_args()
    filas = cargar(args.entrada)
    if not filas:
        raise SystemExit("No se leyeron filas. Revisa la ruta de --entrada.")
    reporte(filas, "categoria")
    reporte(filas, "urgencia")
    print("\nNota: el kappa mide acuerdo entre DOS personas reales. "
          "Una IA etiquetando no cuenta como acuerdo entre anotadores.")


if __name__ == "__main__":
    main()
