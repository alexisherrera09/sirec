"""
Pruebas del microservicio de clasificación (Fase A1).

Cubren el mínimo exigido por el plan:
- Caso válido: el endpoint responde 200 y clasifica coherentemente.
- Caso de texto vacío: devuelve 422 (validación).
- Verificación de que categoría y urgencia SIEMPRE pertenecen a los valores permitidos.
"""

from fastapi.testclient import TestClient

from main import app
from contrato import CATEGORIAS_VALIDAS, URGENCIAS_VALIDAS

client = TestClient(app)


def test_salud_modo_simulado():
    """El servicio reporta estado ok y modo simulado por defecto."""
    r = client.get("/salud")
    assert r.status_code == 200
    assert r.json() == {"estado": "ok", "modo": "simulado"}


def test_clasificar_inundacion():
    """Un texto de inundación se clasifica como categoria=inundacion."""
    r = client.post("/clasificar", json={"texto": "se inundó la calle"})
    assert r.status_code == 200
    assert r.json()["categoria"] == "inundacion"


def test_clasificar_persona_en_riesgo_alta():
    """Persona atrapada → persona_en_riesgo con urgencia alta (caso crítico)."""
    r = client.post("/clasificar", json={"texto": "hay una persona atrapada en el segundo piso"})
    datos = r.json()
    assert r.status_code == 200
    assert datos["categoria"] == "persona_en_riesgo"
    assert datos["urgencia"] == "alta"


def test_clasificar_texto_vacio_devuelve_422():
    """Texto vacío debe rechazarse con 422 (contrato 1.3)."""
    r = client.post("/clasificar", json={"texto": ""})
    assert r.status_code == 422


def test_clasificar_solo_espacios_devuelve_422():
    """Texto de solo espacios también debe rechazarse con 422."""
    r = client.post("/clasificar", json={"texto": "   "})
    assert r.status_code == 422


def test_categoria_y_urgencia_siempre_validas():
    """Para textos variados, categoría y urgencia pertenecen a los valores permitidos."""
    textos = [
        "se cayó un poste con cables en la avenida",
        "hay un incendio en la bodega",
        "se está metiendo el agua a mi casa",
        "hay una grieta enorme en el muro de la casa",
        "vi un perro en la calle",  # sin coincidencia → otro
        "hubo un deslave en el cerro y tapó el camino",
    ]
    for texto in textos:
        datos = client.post("/clasificar", json={"texto": texto}).json()
        assert datos["categoria"] in CATEGORIAS_VALIDAS
        assert datos["urgencia"] in URGENCIAS_VALIDAS
        assert 0.0 <= datos["confianza_categoria"] <= 1.0
        assert 0.0 <= datos["confianza_urgencia"] <= 1.0
