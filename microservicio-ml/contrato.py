"""
Contrato de datos compartido del microservicio de clasificación SIREC.

FUENTE ÚNICA DE VERDAD para este componente (sección 1 del plan).
Las 7 categorías y los 3 niveles de urgencia NO deben divergir de los
demás componentes (.NET, frontend). Si cambian aquí, deben cambiar en todos.
"""

from enum import Enum


class Categoria(str, Enum):
    """7 categorías temáticas fijas (contrato 1.1)."""

    INUNDACION = "inundacion"
    PERSONA_EN_RIESGO = "persona_en_riesgo"
    CAIDA_POSTE_CABLE = "caida_poste_cable"
    DESLAVE = "deslave"
    INCENDIO = "incendio"
    DANO_ESTRUCTURAL = "dano_estructural"
    OTRO = "otro"


class Urgencia(str, Enum):
    """3 niveles de urgencia fijos (contrato 1.2)."""

    ALTA = "alta"
    MEDIA = "media"
    BAJA = "baja"


# Conjuntos para validación rápida (usados en las pruebas y en A2).
CATEGORIAS_VALIDAS = {c.value for c in Categoria}
URGENCIAS_VALIDAS = {u.value for u in Urgencia}
