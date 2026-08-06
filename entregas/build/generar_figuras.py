"""Genera las figuras propias del documento (C13).

    .venv-docs/bin/python build/generar_figuras.py

Salida: build/figuras/arquitectura.png, formulario.png, panel.png
Diseno sobrio, legible en impresion a escala de grises, con las entradas y
salidas rotuladas sobre las conexiones.
"""

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figuras")
os.makedirs(DIR, exist_ok=True)

AZUL = "#0098CD"
AZUL_OSC = "#00688F"
GRIS = "#5A5A5A"
GRIS_CLARO = "#EDEDED"
ROJO = "#C0392B"
AMBAR = "#E8A33D"
VERDE = "#4B8B3B"


def caja(ax, x, y, w, h, titulo, lineas, color=AZUL, fs_t=9.5, fs_l=8):
    """Caja con titulo (admite varias lineas) y lineas de detalle debajo."""
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.12,rounding_size=0.18",
        linewidth=1.6, edgecolor=color, facecolor="white", zorder=3))
    n_titulo = titulo.count("\n") + 1
    ax.text(x + w / 2, y + h - 0.34, titulo, ha="center", va="top",
            fontsize=fs_t, fontweight="bold", color=color, zorder=4,
            linespacing=1.35)
    y0 = y + h - 0.34 - n_titulo * 0.40 - 0.16
    for i, ln in enumerate(lineas):
        ax.text(x + w / 2, y0 - i * 0.34, ln, ha="center", va="top",
                fontsize=fs_l, color=GRIS, zorder=4)


def flecha(ax, p1, p2, etiqueta="", dy=0.22, color=GRIS, estilo="-|>", fs=7.6,
           conn="arc3,rad=0"):
    ax.add_patch(FancyArrowPatch(
        p1, p2, arrowstyle=estilo, mutation_scale=13, linewidth=1.3,
        color=color, connectionstyle=conn, zorder=2))
    if etiqueta:
        mx, my = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2
        ax.text(mx, my + dy, etiqueta, ha="center", va="bottom", fontsize=fs,
                color=color, style="italic", zorder=5,
                bbox=dict(boxstyle="round,pad=0.18", facecolor="white",
                          edgecolor="none", alpha=0.92))


# --------------------------------------------------------------- arquitectura
def arquitectura():
    """Diagrama de modulos con entradas y salidas rotuladas (C13).

    Las cajas llevan poco texto y los huecos son anchos: a este tamano de
    insercion (16 cm) todo debe leerse sin que las etiquetas pisen las cajas.
    """
    fig, ax = plt.subplots(figsize=(8.6, 3.7))
    ax.set_xlim(0, 27.4)
    ax.set_ylim(0.6, 11.2)
    ax.axis("off")

    caja(ax, 0.2, 7.6, 3.4, 2.6, "Ciudadano", ["Redacta el", "reporte"],
         color=GRIS, fs_t=9, fs_l=7.5)
    caja(ax, 0.2, 1.4, 3.4, 2.6, "Operador", ["Atiende y", "despacha"],
         color=GRIS, fs_t=9, fs_l=7.5)

    caja(ax, 7.0, 7.6, 4.6, 2.6, "Módulo 1\nFormulario",
         ["Texto libre", "React"], color=AZUL, fs_t=9, fs_l=7.5)
    caja(ax, 14.4, 7.6, 4.6, 2.6, "Módulo 2\nAPI backend",
         ["Orquesta y", "persiste · .NET 8"], color=AZUL, fs_t=9, fs_l=7.5)
    caja(ax, 21.6, 7.6, 5.0, 2.6, "Módulo 3\nClasificador",
         ["BETO + TF-IDF", "FastAPI"], color=AZUL_OSC, fs_t=9, fs_l=7.5)
    caja(ax, 14.4, 1.4, 4.6, 2.6, "Módulo 4\nBase de datos",
         ["Etiquetas y traza", "PostgreSQL"], color=AZUL, fs_t=9, fs_l=7.5)
    caja(ax, 7.0, 1.4, 4.6, 2.6, "Módulo 5\nPanel",
         ["Lista priorizada", "React"], color=AZUL, fs_t=9, fs_l=7.5)

    flecha(ax, (3.6, 8.9), (7.0, 8.9), "texto del\nreporte", dy=0.16, fs=7.2)
    flecha(ax, (11.6, 8.9), (14.4, 8.9), "POST\n/reportes", dy=0.16, fs=7.2)
    flecha(ax, (19.0, 9.6), (21.6, 9.6), "texto", dy=0.14, fs=7.2)
    flecha(ax, (21.6, 8.3), (19.0, 8.3), "etiquetas y\nconfianza", dy=-1.45,
           color=AZUL_OSC, fs=7.2)
    flecha(ax, (16.7, 7.6), (16.7, 4.0), "reporte, etiquetas\ny confianza", dy=0.1, fs=7.2)
    flecha(ax, (14.4, 2.7), (11.6, 2.7), "consulta\npriorizada", dy=0.16, fs=7.2)
    flecha(ax, (7.0, 2.7), (3.6, 2.7), "lista\npriorizada", dy=0.16, fs=7.2)
    flecha(ax, (1.9, 4.0), (1.9, 7.6), "atención y\ndespacho", dy=0.1, color=VERDE, fs=7.2)

    ax.text(13.3, 0.7, "El conjunto se despliega en una única instancia de servidor; el "
                       "clasificador se ejecuta en infraestructura propia y no envía datos a "
                       "servicios de terceros.",
            ha="center", va="bottom", fontsize=7.6, color=GRIS, style="italic")

    fig.tight_layout()
    fig.savefig(os.path.join(DIR, "arquitectura.png"), dpi=200,
                bbox_inches="tight", facecolor="white")
    plt.close(fig)


# ------------------------------------------------------------------ formulario
def formulario():
    fig, ax = plt.subplots(figsize=(5.6, 4.1))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis("off")

    ax.add_patch(Rectangle((0.3, 0.3), 9.4, 11.4, linewidth=1.6,
                           edgecolor=GRIS, facecolor="white"))
    ax.add_patch(Rectangle((0.3, 10.5), 9.4, 1.2, linewidth=0, facecolor=AZUL))
    ax.text(0.9, 11.1, "SIREC · Reportar una emergencia", fontsize=11,
            color="white", va="center", fontweight="bold")

    ax.text(0.9, 9.9, "Describa lo que está ocurriendo", fontsize=9.5,
            fontweight="bold", color=GRIS)
    ax.add_patch(Rectangle((0.9, 7.6), 8.2, 2.0, linewidth=1.2,
                           edgecolor=GRIS, facecolor=GRIS_CLARO))
    ax.text(1.15, 9.25, "«Se cayó un poste y hay cables sobre la\n"
                        "banqueta, una señora quedó atrapada\n"
                        "entre el poste y su carro»",
            fontsize=9, color="#333333", va="top", style="italic")
    ax.text(0.9, 7.25, "Texto libre · sin formularios rígidos ni catálogos que elegir",
            fontsize=7.8, color=GRIS, style="italic")

    ax.text(0.9, 5.9, "Ubicación aproximada (opcional)", fontsize=9.5,
            fontweight="bold", color=GRIS)
    ax.add_patch(Rectangle((0.9, 4.9), 8.2, 0.8, linewidth=1.2,
                           edgecolor=GRIS, facecolor="white"))
    ax.text(1.15, 5.3, "Calle o referencia cercana", fontsize=8.6, color="#999999",
            va="center")

    ax.text(0.9, 4.35, "Teléfono de contacto (opcional)", fontsize=9.5,
            fontweight="bold", color=GRIS)
    ax.add_patch(Rectangle((0.9, 3.35), 8.2, 0.8, linewidth=1.2,
                           edgecolor=GRIS, facecolor="white"))
    ax.text(1.15, 3.75, "10 dígitos", fontsize=8.6, color="#999999", va="center")

    ax.add_patch(FancyBboxPatch((0.9, 2.1), 3.5, 0.9,
                                boxstyle="round,pad=0.05,rounding_size=0.12",
                                linewidth=0, facecolor=AZUL))
    ax.text(2.65, 2.55, "Enviar reporte", ha="center", va="center", fontsize=9.5,
            color="white", fontweight="bold")

    ax.add_patch(Rectangle((0.9, 0.7), 8.2, 1.1, linewidth=1.1,
                           edgecolor=VERDE, facecolor="#F1F8EE"))
    ax.text(1.15, 1.25, "Reporte recibido. Se clasificó como «persona en riesgo»\n"
                        "con urgencia alta y ya aparece en el panel de atención.",
            fontsize=8.4, color=VERDE, va="center")

    fig.tight_layout()
    fig.savefig(os.path.join(DIR, "formulario.png"), dpi=200,
                bbox_inches="tight", facecolor="white")
    plt.close(fig)


# ----------------------------------------------------------------------- panel
def panel():
    fig, ax = plt.subplots(figsize=(9.0, 3.8))
    ax.set_xlim(0, 22)
    ax.set_ylim(1.6, 12)
    ax.axis("off")

    ax.add_patch(Rectangle((0.3, 1.9), 21.4, 9.8, linewidth=1.6,
                           edgecolor=GRIS, facecolor="white"))
    ax.add_patch(Rectangle((0.3, 10.6), 21.4, 1.1, linewidth=0, facecolor=AZUL))
    ax.text(0.9, 11.15, "SIREC · Panel del operador", fontsize=11, color="white",
            va="center", fontweight="bold")
    ax.text(21.1, 11.15, "Ordenado por prioridad", fontsize=8.6, color="white",
            va="center", ha="right", style="italic")

    X_URG, X_CAT, X_TXT, X_CONF, X_BARRA, X_EST, X_MARCA = (
        0.9, 3.3, 7.6, 14.3, 15.1, 17.2, 19.4)
    cols = [("Urgencia", X_URG), ("Categoría", X_CAT), ("Reporte", X_TXT),
            ("Confianza", X_CONF), ("Estado", X_EST), ("Revisión", X_MARCA)]
    ax.add_patch(Rectangle((0.5, 9.7), 21.0, 0.8, linewidth=0, facecolor=GRIS_CLARO))
    for nombre, x in cols:
        ax.text(x, 10.1, nombre, fontsize=8.8, fontweight="bold", color=GRIS,
                va="center")

    filas = [
        (ROJO, "ALTA", "Persona en riesgo",
         "«hay una señora atrapada entre el poste»", "0.96", "Sin atender", None),
        (ROJO, "ALTA", "Inundación",
         "«el agua entró a la casa y sigue subiendo»", "0.91", "Sin atender", None),
        (AMBAR, "MEDIA", "Poste o cable caído",
         "«se cayó un cable, nadie cerca»", "0.58", "Sin atender",
         "revisar"),
        (AMBAR, "MEDIA", "Daño estructural",
         "«se cuarteó la barda de la escuela»", "0.87", "En atención", None),
    ]

    y = 8.6
    for color, urg, cat, txt, conf, estado, marca in filas:
        ax.add_patch(Rectangle((0.5, y), 21.0, 1.5, linewidth=0.8,
                               edgecolor="#DDDDDD", facecolor="white"))
        ax.add_patch(Rectangle((0.5, y), 0.22, 1.5, linewidth=0, facecolor=color))
        ax.add_patch(FancyBboxPatch((X_URG, y + 0.45), 1.75, 0.62,
                                    boxstyle="round,pad=0.03,rounding_size=0.1",
                                    linewidth=0, facecolor=color))
        ax.text(X_URG + 0.88, y + 0.76, urg, ha="center", va="center", fontsize=8.4,
                color="white", fontweight="bold")
        ax.text(X_CAT, y + 0.76, cat, fontsize=8.4, color="#333333", va="center")
        ax.text(X_TXT, y + 0.76, txt, fontsize=7.6, color="#555555", va="center",
                style="italic")
        ax.text(X_CONF, y + 0.76, conf, fontsize=8.4, color="#333333", va="center")
        ax.add_patch(Rectangle((X_BARRA, y + 0.62), 1.4, 0.28, linewidth=0.6,
                               edgecolor=GRIS, facecolor="white"))
        ax.add_patch(Rectangle((X_BARRA, y + 0.62), 1.4 * float(conf), 0.28,
                               linewidth=0, facecolor=color))
        ax.text(X_EST, y + 0.76, estado, fontsize=8.4, color=GRIS, va="center")
        if marca:
            ax.add_patch(FancyBboxPatch((X_MARCA, y + 0.45), 1.9, 0.62,
                                        boxstyle="round,pad=0.03,rounding_size=0.1",
                                        linewidth=1.0, edgecolor=AMBAR,
                                        facecolor="#FDF6EA"))
            ax.text(X_MARCA + 0.95, y + 0.76, marca, ha="center", va="center",
                    fontsize=7.6, color="#9A6B14", fontweight="bold")
        y -= 1.62

    ax.text(0.9, 2.2,
            "La franja lateral y la etiqueta indican la urgencia; la barra muestra la "
            "confianza del modelo. Cuando la confianza queda por debajo\ndel umbral, el "
            "reporte se marca para revisión humana sin perder su posición en la lista. El "
            "operador puede corregir la\nclasificación, y esa corrección se registra como "
            "traza de retroalimentación.",
            fontsize=8, color=GRIS, va="bottom", style="italic", linespacing=1.5)

    fig.tight_layout()
    fig.savefig(os.path.join(DIR, "panel.png"), dpi=200, bbox_inches="tight",
                facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    arquitectura()
    formulario()
    panel()
    print("figuras generadas en", DIR)
    for f in sorted(os.listdir(DIR)):
        print("  ", f, os.path.getsize(os.path.join(DIR, f)) // 1024, "KB")
