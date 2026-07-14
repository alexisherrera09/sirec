"""
Genera el archivo de adjudicación del kappa (SIREC, D3.4).

Empareja por texto las etiquetas de los dos anotadores (Ricardo y Nahum) y
produce un CSV donde:
  - Si ambos coincidieron en un campo -> se pre-rellena la etiqueta final (no hay que decidir).
  - Si discreparon -> la celda final queda VACÍA para que el tercer anotador (Alexis) decida.

El tercer anotador solo llena las celdas vacías (categoria_final / urgencia_final),
consultando la guía de etiquetado. Con eso se obtiene un subconjunto "gold" de los 180
y se documenta el proceso de conciliación (procedimiento académico estándar cuando el
kappa inicial de un campo queda bajo el umbral).

Uso:
    py generar_adjudicacion.py
"""

import csv
import io
import collections

RUTAS = ["kappa_ricardo.csv", "kappa_nahum.csv"]
SALIDA = "adjudicacion_kappa.csv"


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


def main():
    filas = cargar(RUTAS)
    etiquetadores = sorted({f["etiquetador"] for f in filas if f["etiquetador"]})
    if len(etiquetadores) != 2:
        raise SystemExit("Se esperaban dos anotadores. Encontrados: %s" % etiquetadores)
    a, b = etiquetadores  # nahum, ricardo (orden alfabético)

    # Emparejar por texto, preservando el orden de primera aparición.
    orden = []
    por_texto = collections.OrderedDict()
    for f in filas:
        k = norm(f["texto"])
        if k not in por_texto:
            por_texto[k] = {"texto": f["texto"]}
            orden.append(k)
        por_texto[k][f["etiquetador"]] = f

    n_cat_desac = 0
    n_urg_desac = 0
    with io.open(SALIDA, "w", encoding="utf-8-sig", newline="") as out:
        w = csv.writer(out)
        w.writerow([
            "texto",
            "categoria_%s" % a, "categoria_%s" % b, "categoria_final",
            "urgencia_%s" % a, "urgencia_%s" % b, "urgencia_final",
        ])
        for k in orden:
            d = por_texto[k]
            if a not in d or b not in d:
                continue
            cat_a, cat_b = d[a]["categoria"], d[b]["categoria"]
            urg_a, urg_b = d[a]["urgencia"], d[b]["urgencia"]
            # Coinciden -> pre-rellenar; discrepan -> vacío para adjudicar.
            cat_final = cat_a if cat_a == cat_b else ""
            urg_final = urg_a if urg_a == urg_b else ""
            if cat_final == "":
                n_cat_desac += 1
            if urg_final == "":
                n_urg_desac += 1
            w.writerow([d["texto"], cat_a, cat_b, cat_final, urg_a, urg_b, urg_final])

    total = sum(1 for k in orden if a in por_texto[k] and b in por_texto[k])
    print("Archivo generado: %s" % SALIDA)
    print("Reportes emparejados: %d" % total)
    print("Celdas a decidir por Alexis:")
    print("   categoria_final vacías (desacuerdos): %d" % n_cat_desac)
    print("   urgencia_final vacías (desacuerdos):  %d" % n_urg_desac)
    print("   TOTAL de decisiones: %d" % (n_cat_desac + n_urg_desac))


if __name__ == "__main__":
    main()
