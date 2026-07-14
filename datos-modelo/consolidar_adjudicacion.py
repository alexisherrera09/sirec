"""
Consolida la adjudicación del kappa en un conjunto "gold" (SIREC, D3.4).

Toma `adjudicacion_kappa.csv` YA LLENO por el tercer anotador (Alexis) —donde las
celdas en desacuerdo tienen ahora una etiqueta final— y produce:

  1. `gold_kappa.csv`  : los 180 reportes con la etiqueta final consensuada
                         (columnas texto, categoria, urgencia, origen), lista para
                         usarse como conjunto de prueba de alta calidad.
  2. Un reporte por consola del proceso de conciliación (cuántos se resolvieron,
     hacia qué clase se inclinó cada campo), para documentar en la memoria.

Valida que no queden celdas *_final vacías (si faltan, avisa y no genera el gold).

Uso:
    py consolidar_adjudicacion.py
"""

import csv
import io
import collections

ENTRADA = "adjudicacion_kappa.csv"
SALIDA = "gold_kappa.csv"

CATEGORIAS = {"inundacion", "persona_en_riesgo", "caida_poste_cable", "deslave",
              "incendio", "dano_estructural", "otro"}
URGENCIAS = {"alta", "media", "baja"}


def main():
    with io.open(ENTRADA, encoding="utf-8-sig", newline="") as f:
        filas = list(csv.DictReader(f))
    if not filas:
        raise SystemExit("No se leyeron filas de %s" % ENTRADA)

    faltantes = []
    invalidas = []
    gold = []
    resueltos_cat = 0
    resueltos_urg = 0
    for i, r in enumerate(filas, start=2):  # +2: encabezado + base 1
        texto = (r.get("texto") or "").strip()
        cat = (r.get("categoria_final") or "").strip()
        urg = (r.get("urgencia_final") or "").strip()
        if not cat or not urg:
            faltantes.append(i)
            continue
        if cat not in CATEGORIAS:
            invalidas.append((i, "categoria_final", cat))
        if urg not in URGENCIAS:
            invalidas.append((i, "urgencia_final", urg))
        # ¿fue un desacuerdo resuelto? (los anotadores difieren en ese campo)
        cols = list(r.keys())
        cat_cols = [c for c in cols if c.startswith("categoria_") and c != "categoria_final"]
        urg_cols = [c for c in cols if c.startswith("urgencia_") and c != "urgencia_final"]
        if len({(r.get(c) or "").strip() for c in cat_cols}) > 1:
            resueltos_cat += 1
        if len({(r.get(c) or "").strip() for c in urg_cols}) > 1:
            resueltos_urg += 1
        gold.append({"texto": texto, "categoria": cat, "urgencia": urg, "origen": "real"})

    if faltantes:
        raise SystemExit(
            "Faltan celdas *_final por llenar en %d fila(s): líneas %s...\n"
            "Completa la adjudicación antes de consolidar."
            % (len(faltantes), faltantes[:10]))
    if invalidas:
        for ln, col, val in invalidas:
            print("  ADVERTENCIA línea %d: %s='%s' no es una etiqueta válida" % (ln, col, val))
        raise SystemExit("Corrige las etiquetas inválidas antes de consolidar.")

    with io.open(SALIDA, "w", encoding="utf-8-sig", newline="") as out:
        w = csv.DictWriter(out, fieldnames=["texto", "categoria", "urgencia", "origen"])
        w.writeheader()
        w.writerows(gold)

    print("Conjunto gold generado: %s (%d reportes)" % (SALIDA, len(gold)))
    print("Desacuerdos resueltos por adjudicación:")
    print("   categoria: %d" % resueltos_cat)
    print("   urgencia:  %d" % resueltos_urg)
    print("\nDistribución final por categoría:")
    for c, n in collections.Counter(g["categoria"] for g in gold).most_common():
        print("   %-20s %d" % (c, n))
    print("Distribución final por urgencia:")
    for u, n in collections.Counter(g["urgencia"] for g in gold).most_common():
        print("   %-20s %d" % (u, n))


if __name__ == "__main__":
    main()
