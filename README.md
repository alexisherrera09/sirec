# SIREC — Sistema Inteligente de Reportes de Emergencia Ciudadana

Plataforma web que **clasifica y prioriza automáticamente** reportes ciudadanos de emergencia
(español de México) para una coordinación municipal de protección civil. Cada reporte recibe,
al ingresar, una **categoría** (7 posibles) y un **nivel de urgencia** (alta/media/baja), y se
presenta al operador en un panel ordenado por prioridad.

> Proyecto de la Maestría en IA (UNIR). Contexto completo en
> [`CONTEXTO_SIREC.md`](CONTEXTO_SIREC.md) y plan en
> [`PLAN_SIREC_ClaudeCode_total.md`](PLAN_SIREC_ClaudeCode_total.md).
> Estado de avance y tareas del equipo en [`AVANCE_Y_TAREAS_HUMANAS.md`](AVANCE_Y_TAREAS_HUMANAS.md).

## Componentes

| Carpeta | Qué es | Puerto local |
|---|---|---|
| [`microservicio-ml/`](microservicio-ml/) | Clasificador Python/FastAPI (modo simulado → BETO) | 8000 |
| [`backend-api/`](backend-api/) | API .NET 8 + PostgreSQL + JWT | 5000 |
| [`frontend/`](frontend/) | React/Vite (formulario público + panel operador) | 5173 |
| [`datos-modelo/`](datos-modelo/) | Guía y herramienta de etiquetado, corpus, entrenamiento | — |

## Puesta en marcha en una máquina nueva

Requisitos: **.NET 8 SDK**, **Node.js 20+**, **Python 3.11+**, **Docker**, **Git**.

```powershell
# 1) Clonar
git clone https://github.com/alexisherrera22/sirec.git
cd sirec

# 2) Base de datos (PostgreSQL en Docker)
#    Nota: si el puerto 5432 está ocupado, este proyecto usa 5433 en local (ver backend-api/README.md)
docker run --name sirec-db -e POSTGRES_PASSWORD=sirec -e POSTGRES_DB=sirec -p 5433:5432 -d postgres:16

# 3) Microservicio (Python)  — restaura dependencias
cd microservicio-ml
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn main:app --port 8000
#   (deja este corriendo; abre otra terminal para lo siguiente)

# 4) Backend (.NET) — restaura y corre (aplica migraciones solo)
cd ..\backend-api
dotnet run

# 5) Frontend (React) — restaura dependencias y corre
cd ..\frontend
npm install
npm run dev
```

Luego abre http://localhost:5173 (formulario) y http://localhost:5173/panel
(panel; usuario `operador` / `sirec-local` en desarrollo).

> Las carpetas `node_modules/`, `.venv/`, `bin/`, `obj/` **no** están en el repositorio a
> propósito: se regeneran con los comandos de arriba (`npm install`, `pip install`, `dotnet run`)
> y son específicas de cada máquina/sistema operativo.

## Estado

Software (componentes A, B, C) y datos sintéticos: **completos y verificados en local**.
Pendiente: tareas humanas de datos reales + kappa (ver `AVANCE_Y_TAREAS_HUMANAS.md`) y luego
entrenamiento/evaluación del modelo (D4–D6) y despliegue AWS.
