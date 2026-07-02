"""
Clasificador simulado por palabras clave (Fase A1).

Este módulo implementa la lógica de clasificación en MODO SIMULADO: no usa
el modelo BETO, sino reglas por coincidencia de palabras clave. Sirve para
levantar toda la arquitectura (backend .NET, frontend) sin depender todavía
del modelo entrenado.

En la Fase A2 este módulo se sustituye por inferencia real de BETO, PERO el
contrato de entrada/salida (contrato 1.3) NO cambia: seguirá devolviendo
(categoria, urgencia, confianza_categoria, confianza_urgencia).
"""

from contrato import Categoria, Urgencia

# Confianza fija plausible para el modo simulado (el modelo real dará valores propios).
CONFIANZA_SIMULADA = 0.9

# Reglas por palabras clave. El orden importa: se evalúa de la más específica /
# peligrosa (persona en riesgo) a la más genérica. Se usan raíces de palabra
# (sin acentos) para tolerar variantes: "inund" cubre inunda/inundación/inundó.
# Cada regla define la categoría y una urgencia por defecto asociada.
REGLAS = [
    # Vidas en riesgo → siempre alta.
    (("atrapad", "herid", "arrastrad", "ahogan", "auxilio", "rescat", "persona"),
     Categoria.PERSONA_EN_RIESGO, Urgencia.ALTA),
    # Incendio: fuego activo → alta.
    (("incendi", "fuego", "quemand", "llamas", "humo"),
     Categoria.INCENDIO, Urgencia.ALTA),
    # Caída de poste/cable: riesgo eléctrico → alta.
    (("poste", "cable", "transformador", "chispas", "cortocircuito"),
     Categoria.CAIDA_POSTE_CABLE, Urgencia.ALTA),
    # Deslave / derrumbe de tierra.
    (("deslave", "derrumbe", "deslizamient", "cerro", "ladera", "talud"),
     Categoria.DESLAVE, Urgencia.ALTA),
    # Inundación / agua.
    (("inund", "agua", "desbord", "lluvia", "anegad", "creciente", "rio"),
     Categoria.INUNDACION, Urgencia.MEDIA),
    # Daño estructural en construcciones.
    (("grieta", "muro", "colaps", "techo", "estructura", "barda", "pared", "edificio"),
     Categoria.DANO_ESTRUCTURAL, Urgencia.MEDIA),
]

# Señales textuales que elevan la urgencia a ALTA aunque la categoría sea media.
SENALES_ALTA = (
    "atrapad", "herid", "arrastrad", "muriend", "grave", "urgent", "auxilio",
    "niño", "nino", "ancian", "bebe", "bebé", "no puede salir", "subiendo rapido",
    "un metro", "energizad", "vivo", "personas dentro",
)


def clasificar(texto: str) -> dict:
    """
    Clasifica un texto de reporte devolviendo el contrato 1.3.

    Retorna un dict con: categoria, urgencia, confianza_categoria, confianza_urgencia.
    La validación de texto vacío se hace en la capa de la API (main.py), no aquí.
    """
    t = texto.lower()

    categoria = Categoria.OTRO
    urgencia = Urgencia.MEDIA

    for claves, cat, urg in REGLAS:
        if any(clave in t for clave in claves):
            categoria = cat
            urgencia = urg
            break

    # Elevación de urgencia por señales de gravedad, sin importar la categoría.
    if any(senal in t for senal in SENALES_ALTA):
        urgencia = Urgencia.ALTA

    return {
        "categoria": categoria.value,
        "urgencia": urgencia.value,
        "confianza_categoria": CONFIANZA_SIMULADA,
        "confianza_urgencia": CONFIANZA_SIMULADA,
    }
