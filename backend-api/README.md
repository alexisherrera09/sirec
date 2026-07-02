# Backend API — SIREC (Componente B)

API REST en **.NET 8 (ASP.NET Core, C#)**. Recibe reportes ciudadanos, los clasifica
llamando al microservicio Python (contrato 1.3), los persiste en PostgreSQL vía EF Core
y expone el panel del operador protegido con JWT.

Puerto fijo en local: **5000** (HTTP, sin HTTPS en local).

## Requisitos

- .NET 8 SDK (probado con 8.0.421). El repo incluye `global.json` que fija el SDK 8.
- Docker (para PostgreSQL local).
- Microservicio de clasificación corriendo en `http://localhost:8000` (Componente A).

## Base de datos (PostgreSQL en Docker)

> **Nota de puerto (local):** el plan fija el 5432, pero esta máquina ya tiene un
> PostgreSQL 18 instalado ocupando el 5432. Para no interferir con él, el contenedor
> de SIREC se mapea al **5433** en local. Es un detalle exclusivo de desarrollo:
> en producción (EC2) PostgreSQL usa su puerto estándar. Si en otra máquina el 5432
> está libre, puede volverse a 5432 cambiando el mapeo y la cadena de conexión.

```powershell
docker run --name sirec-db -e POSTGRES_PASSWORD=sirec -e POSTGRES_DB=sirec -p 5433:5432 -d postgres:16
```

## Arranque

```powershell
cd backend-api
dotnet run
```

Al arrancar aplica automáticamente las migraciones pendientes. Swagger: http://localhost:5000/swagger

## Configuración

`appsettings.json` (no sensible) y `appsettings.Development.json` (secreto JWT y
credenciales del operador, solo para local). En producción todo va por variables de
entorno y las credenciales son distintas.

| Clave | Descripción |
|---|---|
| `ConnectionStrings:Sirec` | Cadena de conexión a PostgreSQL |
| `Clasificador:Url` | URL del microservicio Python (por defecto `http://localhost:8000`) |
| `Jwt:Secreto` | Clave de firma del JWT |
| `Operador:Usuario` / `Operador:Contrasena` | Credenciales del operador del panel |
| `Cors:Origenes` | Orígenes permitidos (por defecto `http://localhost:5173`) |

Credenciales de desarrollo: usuario `operador`, contraseña `sirec-local`.

## Endpoints

| Método | Ruta | Auth | Descripción |
|---|---|---|---|
| POST | `/api/reportes` | Público | Crea un reporte (lo clasifica y guarda). Resiliente: si el microservicio cae, guarda con fallback y `requiereRevision=true` |
| GET | `/api/reportes` | JWT | Lista ordenada por urgencia (alta→media→baja) y fecha desc. Filtros `?categoria=` y `?estado=` |
| GET | `/api/reportes/{id}` | JWT | Un reporte por id |
| PATCH | `/api/reportes/{id}/estado` | JWT | Cambia estado (pendiente→en_atencion→atendido; rechaza transiciones inválidas) |
| GET | `/api/reportes/resumen` | JWT | Contadores {alta, media, baja, totalHoy} |
| POST | `/api/auth/login` | Público | Devuelve token JWT |

## Estructura

| Carpeta/archivo | Función |
|---|---|
| `Models/Contrato.cs` | Categorías, urgencias, estados y reglas de transición (fuente única de verdad del backend) |
| `Models/Reporte.cs` | Entidad del reporte (modelo 1.4) |
| `Data/SirecDbContext.cs` | DbContext EF Core |
| `Services/ClasificadorClient.cs` | Cliente HTTP al microservicio con fallback resiliente |
| `Auth/JwtService.cs` | Emisión de tokens JWT |
| `Controllers/` | `ReportesController`, `AuthController` |
| `Migrations/` | Migraciones EF Core |
