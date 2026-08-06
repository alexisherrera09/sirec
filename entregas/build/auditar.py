"""Auditoria mecanica del documento generado, contra la retroalimentacion del profesor.

Uso:
    .venv-docs/bin/python build/auditar.py "Entrega 2 Final.docx"

Comprueba: extension, estilos, numeracion, rotulos de tablas y figuras,
parrafos largos y cortos, titulos consecutivos sin texto, saltos de pagina,
y el circuito citas <-> referencias.
"""

import re
import sys
from collections import Counter

from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph

PALABRAS_POR_PAGINA = 375  # A4, Calibri 12, interlineado 1.5


def bloques(doc):
    for ch in doc.element.body.iterchildren():
        if ch.tag.endswith("}p"):
            yield "p", Paragraph(ch, doc)
        elif ch.tag.endswith("}tbl"):
            yield "tbl", Table(ch, doc)


def main(ruta):
    doc = Document(ruta)
    items = list(bloques(doc))

    cuerpo_pal = 0
    anexo_pal = 0
    en_anexo = False
    en_refs = False
    heads = []
    largos = []
    cortos = []
    consecutivos = []
    saltos = 0
    rot_tabla = []
    rot_figura = []
    n_tablas = 0
    n_figuras = 0
    fuentes = 0
    estilos = Counter()
    texto_total = []
    anterior_head = False

    for tipo, obj in items:
        if tipo == "tbl":
            n_tablas += 1
            anterior_head = False
            continue

        p = obj
        est = p.style.name
        txt = p.text.strip()
        estilos[est] += 1
        if "w:br" in p._p.xml and 'w:type="page"' in p._p.xml:
            saltos += 1
        if p.paragraph_format.page_break_before:
            saltos += 1

        if est == "Anexo":
            en_anexo = True
        if est == "Título 1 sin numerar" and "Referencias" in txt:
            en_refs = True

        # las imagenes van en parrafos sin texto: contarlas antes de saltarlos
        n_figuras += len(re.findall(r"<pic:pic", p._p.xml))

        if not txt:
            continue

        texto_total.append(txt)
        n_pal = len(txt.split())
        es_head = est.startswith("Heading") or est in ("Anexo", "Título 1 sin numerar")

        if es_head:
            heads.append((est, txt))
            if anterior_head:
                consecutivos.append(txt)
            anterior_head = True
        else:
            anterior_head = False
            if en_anexo:
                anexo_pal += n_pal
            elif not en_refs:
                cuerpo_pal += n_pal

        if est == "Normal":
            m = re.match(r"^(Tabla|Figura)\s+(\d+)\.", txt)
            if m:
                (rot_tabla if m.group(1) == "Tabla" else rot_figura).append(int(m.group(2)))
        if est == "Pie de foto-tabla" and txt.startswith("Fuente:"):
            fuentes += 1

        if est in ("Normal",) and not re.match(r"^(Tabla|Figura)\s+\d+\.", txt):
            if n_pal >= 120:
                largos.append((n_pal, txt[:70]))
            elif n_pal < 25 and txt.endswith("."):
                cortos.append((n_pal, txt[:70]))

    todo = " ".join(texto_total)

    # citas en texto: (Autor, 2020) / Autor (2020) / (Autor et al., 2020)
    citas = set()
    for m in re.finditer(r"\(([A-ZÁÉÍÓÚÑ][^()]{2,60}?),\s*(\d{4}[a-z]?)\)", todo):
        citas.add((m.group(1).split(" y ")[0].split(",")[0].strip(), m.group(2)))
    for m in re.finditer(r"([A-ZÁÉÍÓÚÑ][A-Za-zÁÉÍÓÚÑáéíóúñ\-]+)(?:\s+et\s+al\.)?\s*\((\d{4}[a-z]?)\)", todo):
        citas.add((m.group(1).strip(), m.group(2)))

    refs = [p.text.strip() for p in doc.paragraphs
            if p.style.name == "Referencias bibliográficas" and p.text.strip()]

    def apellido(ref):
        m = re.match(r"^([^,(]+)", ref)
        return m.group(1).strip() if m else ref[:20]

    apellidos_refs = {apellido(r): r for r in refs}
    anios_refs = {(apellido(r), (re.search(r"\((\d{4}[a-z]?)\)", r).group(1)
                                 if re.search(r"\((\d{4}[a-z]?)\)", r) else "?")) for r in refs}

    huerfanas = []
    for autor, anio in sorted(citas):
        base = autor.split()[0]
        if not any(base in a for a, _ in anios_refs):
            huerfanas.append(f"{autor} ({anio})")

    no_citadas = []
    for a, _ in sorted(anios_refs):
        base = a.split()[0]
        if base not in todo:
            no_citadas.append(a)

    print("=" * 74)
    print(f"AUDITORIA: {ruta}")
    print("=" * 74)
    print(f"Palabras de desarrollo (caps. 1-3, sin refs ni anexos): {cuerpo_pal:,}")
    print(f"  -> paginas estimadas a {PALABRAS_POR_PAGINA} pal/pag: {cuerpo_pal/PALABRAS_POR_PAGINA:.1f}"
          f"   [requisito: 20-30]")
    print(f"Palabras en anexos (no computan): {anexo_pal:,}")
    print(f"Referencias: {len(refs)}   [meta: 20-25]")
    print()
    n_tablas_contenido = n_tablas - 1  # la primera tabla es la de la portada
    print(f"Tablas de contenido: {n_tablas_contenido} | rotulos 'Tabla N.': {len(rot_tabla)} {rot_tabla}")
    print(f"Figuras insertadas: {n_figuras} | rotulos 'Figura N.': {len(rot_figura)} {rot_figura}")
    esperadas = n_tablas_contenido + len(rot_figura)
    print(f"Lineas 'Fuente:': {fuentes}   [debe ser {esperadas}]"
          + ("   OK" if fuentes == esperadas else "   <-- REVISAR"))
    print(f"Saltos de pagina / page_break_before: {saltos}")
    print()
    print(f"Encabezados: {len(heads)}")
    for est, txt in heads:
        print(f"   [{est}] {txt[:72]}")
    print()
    print(f"Titulos consecutivos sin texto entre ellos: {len(consecutivos)} {consecutivos}")
    print(f"Parrafos de >=120 palabras (~9+ renglones): {len(largos)}")
    for n, t in largos:
        print(f"   {n} pal: {t}...")
    print(f"Parrafos sospechosamente cortos (<25 palabras): {len(cortos)}")
    for n, t in cortos:
        print(f"   {n} pal: {t}...")
    print()
    print(f"Citas detectadas en el texto: {len(citas)}")
    print(f"Citas sin entrada en Referencias: {len(huerfanas)} {huerfanas}")
    print(f"Referencias no citadas en el texto: {len(no_citadas)} {no_citadas}")
    print()
    print("Estilos usados:", dict(estilos.most_common(12)))

    # --- desglose de palabras por apartado (para decidir donde recortar) ---
    print()
    print("PALABRAS POR APARTADO")
    actual = None
    acumulado = []
    en_anexo2 = False
    for tipo, obj in items:
        if tipo == "tbl":
            filas = len(obj.rows)
            if actual:
                actual[2] += filas
            continue
        p = obj
        est = p.style.name
        txt = p.text.strip()
        if est in ("Anexo", "Título 1 sin numerar"):
            en_anexo2 = True
        if est in ("Heading 1", "Heading 2"):
            actual = [est, txt, 0, 0]
            acumulado.append(actual)
        elif txt and actual and not est.startswith("Heading"):
            actual[3] += len(txt.split())
    for est, titulo, filas, pal in acumulado:
        sangria = "  " if est == "Heading 1" else "     "
        extra = f" + {filas} filas de tabla" if filas else ""
        print(f"{sangria}{titulo[:52]:54} {pal:5} pal{extra}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "Entrega 2 Final.docx")
