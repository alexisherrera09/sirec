"""Genera 'Entrega 2 Final.docx' sobre la plantilla oficial de UNIR.

Uso:
    cd /home/ubuntu/proyectos/sirec/entregas
    .venv-docs/bin/python build/construir.py        # ruta relativa a 'entregas'

El documento se reconstruye completo en cada ejecucion: la fuente de verdad son
los modulos de contenido, nunca el .docx generado.
"""

import importlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from doc_builder import Documento  # noqa: E402

TITULO = ("Sistema Inteligente de Reportes de Emergencia Ciudadana (SIREC): "
          "clasificación y priorización automática de reportes ciudadanos "
          "de emergencia mediante procesamiento del lenguaje natural")

TITULO_CORTO = ("SIREC: clasificación y priorización automática de reportes "
                "ciudadanos de emergencia")

INTEGRANTES = [
    "Alexis Salvador Herrera García",
    "Edy Nahum De León Gálvez",
    "Ricardo Gurrola Palacios",
]

# Orden de los modulos de contenido. Los que aun no existen se omiten con aviso.
MODULOS = [
    "cap1_introduccion",
    "cap2_objetivos",
    "cap3_0_intro",
    "cap3_1_empatizar",
    "cap3_2_definir",
    "cap3_3a_teorico",
    "cap3_3b_estado_arte",
    "cap3_4_idear",
    "cap3_5_prototipar",
    "cap3_6_seleccion",
    "cap3_7_evaluacion",
    "referencias",
    "anexo_a",
    "anexo_b",
]


def main():
    d = Documento("plantilla.docx")

    d.portada(
        titulo=TITULO,
        integrantes=INTEGRANTES,
        fecha="Veracruz, México, agosto de 2026",
    )
    d.encabezado(
        autores="Alexis Salvador Herrera García · Edy Nahum De León Gálvez · Ricardo Gurrola Palacios",
        titulo_tfe=TITULO_CORTO,
    )

    faltantes = []
    for nombre in MODULOS:
        try:
            mod = importlib.import_module(nombre)
        except ModuleNotFoundError:
            faltantes.append(nombre)
            continue
        mod.escribir(d)

    salida = "Entrega 2 Final.docx"
    d.guardar(salida)

    print(f"generado: {salida}")
    print(f"  tablas: {d.n_tabla} | figuras: {d.n_figura}")
    if faltantes:
        print("  modulos pendientes: " + ", ".join(faltantes))


if __name__ == "__main__":
    main()
