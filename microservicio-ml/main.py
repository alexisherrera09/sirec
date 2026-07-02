"""
Microservicio de clasificación SIREC — API FastAPI (Componente A).

Expone el contrato 1.3 del plan:
    POST /clasificar  → clasifica un reporte (categoría + urgencia + confianzas)
    GET  /salud       → estado del servicio y modo actual (simulado / modelo)

Arranca en MODO SIMULADO (reglas por palabras clave). La variable de entorno
SIREC_MODO permite alternar a 'modelo' en la Fase A2 sin cambiar el contrato.

Puerto fijo en local: 8000 (uvicorn main:app --port 8000).
"""

import os

from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator

from clasificador_simulado import clasificar as clasificar_simulado

# Modo de operación: 'simulado' (Fase A1) o 'modelo' (Fase A2). Por defecto simulado.
MODO = os.getenv("SIREC_MODO", "simulado")

app = FastAPI(
    title="SIREC — Microservicio de clasificación",
    description="Clasifica reportes ciudadanos de emergencia por categoría y urgencia.",
    version="0.1.0",
)


class ReporteEntrada(BaseModel):
    """Cuerpo de la petición a /clasificar (contrato 1.3)."""

    texto: str = Field(..., description="Texto libre del reporte ciudadano.")

    @field_validator("texto")
    @classmethod
    def texto_no_vacio(cls, valor: str) -> str:
        """Rechaza texto vacío o compuesto solo por espacios (→ 422)."""
        recortado = valor.strip()
        if not recortado:
            raise ValueError("El texto del reporte no puede estar vacío.")
        return recortado


class ClasificacionSalida(BaseModel):
    """Respuesta de /clasificar (contrato 1.3)."""

    categoria: str
    urgencia: str
    confianza_categoria: float = Field(..., ge=0.0, le=1.0)
    confianza_urgencia: float = Field(..., ge=0.0, le=1.0)


@app.get("/salud")
def salud() -> dict:
    """Devuelve el estado del servicio y el modo activo."""
    return {"estado": "ok", "modo": MODO}


@app.post("/clasificar", response_model=ClasificacionSalida)
def clasificar_reporte(reporte: ReporteEntrada) -> dict:
    """
    Clasifica el texto del reporte y devuelve categoría, urgencia y confianzas.

    En modo simulado usa reglas por palabras clave; en modo modelo (A2) usará BETO.
    El contrato de salida es idéntico en ambos modos.
    """
    if MODO == "modelo":
        # Fase A2: aquí se enchufará la inferencia real de BETO sin tocar el contrato.
        from clasificador_modelo import clasificar as clasificar_modelo  # import diferido
        return clasificar_modelo(reporte.texto)

    return clasificar_simulado(reporte.texto)
