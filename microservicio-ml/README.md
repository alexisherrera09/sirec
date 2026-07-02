# Microservicio de clasificación — SIREC (Componente A)

Microservicio Python (FastAPI) que clasifica reportes ciudadanos de emergencia por
**categoría** (7 posibles) y **urgencia** (alta/media/baja). Arranca en **modo simulado**
(reglas por palabras clave) y en la Fase A2 se conecta al modelo BETO real **sin cambiar
el contrato** de la API.

Puerto fijo en local: **8000**.

## Requisitos

- Python 3.11+ (probado con 3.13 vía el lanzador `py` de Windows).

## Instalación (Windows / PowerShell)

```powershell
cd microservicio-ml
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

En Linux/macOS: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`.

## Arranque

```powershell
uvicorn main:app --port 8000
```

Documentación interactiva: http://localhost:8000/docs

## Modo de operación

Variable de entorno `SIREC_MODO`:

- `simulado` (por defecto): clasifica por palabras clave. No requiere el modelo.
- `modelo`: usa BETO ajustado (Fase A2; requiere `../datos-modelo/modelo_exportado/`).

```powershell
$env:SIREC_MODO = "simulado"   # o "modelo"
uvicorn main:app --port 8000
```

## Contrato de la API (contrato 1.3 del plan)

### `GET /salud`
```json
{ "estado": "ok", "modo": "simulado" }
```

### `POST /clasificar`
```json
// petición
{ "texto": "Se está metiendo el agua a mi casa en Las Brisas" }

// respuesta
{
  "categoria": "inundacion",
  "urgencia": "alta",
  "confianza_categoria": 0.94,
  "confianza_urgencia": 0.88
}
```

Reglas: `categoria` ∈ {inundacion, persona_en_riesgo, caida_poste_cable, deslave,
incendio, dano_estructural, otro}; `urgencia` ∈ {alta, media, baja}; confianzas en
[0.0, 1.0]; texto vacío o solo espacios → **HTTP 422**.

## Pruebas

```powershell
pytest
```

## Archivos

| Archivo | Función |
|---|---|
| `main.py` | API FastAPI: endpoints `/salud` y `/clasificar` |
| `contrato.py` | Enums de categorías y urgencias (fuente única de verdad del componente) |
| `clasificador_simulado.py` | Lógica por palabras clave (Fase A1) |
| `clasificador_modelo.py` | Inferencia BETO real (Fase A2 — se crea al integrar el modelo) |
| `test_main.py` | Pruebas pytest del endpoint |
