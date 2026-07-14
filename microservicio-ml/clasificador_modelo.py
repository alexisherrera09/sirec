"""
Clasificador real con BETO (Fase A2 / D5) — SIREC.

Carga los dos modelos BETO fine-tuned (uno por tarea) y clasifica el texto del
reporte devolviendo EXACTAMENTE el mismo contrato 1.3 que el modo simulado:
    (categoria, urgencia, confianza_categoria, confianza_urgencia).

Los modelos se cargan una sola vez (perezoso, en la primera petición) y se
reutilizan. La confianza es la probabilidad softmax de la clase predicha.

Ubicación de los modelos (carpetas exportadas desde Colab, dentro de beto_modelos.zip):
    <SIREC_MODELO_DIR>/beto_categoria/
    <SIREC_MODELO_DIR>/beto_urgencia/
Por defecto SIREC_MODELO_DIR = ./modelos (junto a este archivo). Configurable por env.

Requiere: torch, transformers  (ver requirements.txt, sección modo modelo).
"""

import os
import functools

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from contrato import CATEGORIAS_VALIDAS, URGENCIAS_VALIDAS

BASE = os.path.dirname(os.path.abspath(__file__))
MODELO_DIR = os.getenv("SIREC_MODELO_DIR", os.path.join(BASE, "modelos"))

# Clases válidas por tarea, para verificar que el modelo cargado es coherente con el contrato.
_VALIDAS = {"categoria": CATEGORIAS_VALIDAS, "urgencia": URGENCIAS_VALIDAS}


class _ModeloTarea:
    """Envuelve un modelo BETO fine-tuned para una tarea (categoria o urgencia)."""

    def __init__(self, tarea: str):
        ruta = os.path.join(MODELO_DIR, "beto_%s" % tarea)
        if not os.path.isdir(ruta):
            raise FileNotFoundError(
                "No se encontró el modelo de '%s' en %s. Extrae beto_modelos.zip ahí "
                "(carpetas beto_categoria/ y beto_urgencia/)." % (tarea, ruta))
        self.tok = AutoTokenizer.from_pretrained(ruta)
        self.modelo = AutoModelForSequenceClassification.from_pretrained(ruta)
        self.modelo.eval()
        self.id2label = self.modelo.config.id2label
        # Verificación de coherencia con el contrato (no debe divergir).
        etiquetas = set(self.id2label.values())
        if not etiquetas <= _VALIDAS[tarea]:
            raise ValueError(
                "El modelo de '%s' tiene etiquetas fuera del contrato: %s"
                % (tarea, etiquetas - _VALIDAS[tarea]))

    @torch.no_grad()
    def predecir(self, texto: str):
        """Devuelve (etiqueta, confianza) para el texto dado."""
        entradas = self.tok(texto, truncation=True, max_length=128, return_tensors="pt")
        logits = self.modelo(**entradas).logits[0]
        probs = torch.softmax(logits, dim=-1)
        idx = int(torch.argmax(probs))
        return self.id2label[idx], float(probs[idx])


@functools.lru_cache(maxsize=1)
def _cargar():
    """Carga perezosa y única de ambos modelos (categoría y urgencia)."""
    return _ModeloTarea("categoria"), _ModeloTarea("urgencia")


def clasificar(texto: str) -> dict:
    """
    Clasifica el texto con BETO y devuelve el contrato 1.3.

    La validación de texto vacío se hace en la capa de la API (main.py).
    """
    modelo_cat, modelo_urg = _cargar()
    categoria, conf_cat = modelo_cat.predecir(texto)
    urgencia, conf_urg = modelo_urg.predecir(texto)
    return {
        "categoria": categoria,
        "urgencia": urgencia,
        "confianza_categoria": round(conf_cat, 4),
        "confianza_urgencia": round(conf_urg, 4),
    }
