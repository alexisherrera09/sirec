# SIREC — Bitácora del despliegue real en EC2

> Ejecutado el **2026-07-31** sobre la instancia EC2 de producción (Ubuntu 26.04, 2 vCPU / 7.6 GB RAM,
> IP pública **13.221.48.89**). Implementa `PLAN_SIREC_AWS_Despliegue.md` con las desviaciones
> que se indican al final. La instancia ya alojaba otro proyecto (`coleccion`), así que SIREC
> convive con él en el mismo Nginx y el mismo PostgreSQL, en puertos y bases separadas.

## 1. Topología desplegada

```
Navegador ──► http(s)://sirec.ameinnovate.com  ──► Nginx (80/443, único proceso expuesto)
                                                     │
                                                     ├─ /       → /usr/local/proyectos/frontend_sirec (React estático, fallback SPA)
                                                     └─ /api/*  → 127.0.0.1:5000  (sirec-api, .NET 8, systemd)
                                                                      ├──► PostgreSQL 18  127.0.0.1:5432  (base `sirec`)
                                                                      └──► 127.0.0.1:8000 (sirec-ml, FastAPI, systemd)
```

`5000`, `8000` y `5432` escuchan **solo en 127.0.0.1** (verificado con `ss -ltn`) y no responden desde
internet. El frontend usa rutas relativas, así que frontend y API comparten origen: no hay CORS ni
contenido mixto.

## 2. Dónde quedó cada componente

| Componente | Ruta de despliegue | Servicio / puerto |
|---|---|---|
| Backend .NET 8 (`SirecApi.dll`) | `/usr/local/proyectos/backend_sirec/` | `sirec-api.service` → `127.0.0.1:5000` |
| Microservicio Python + venv | `/usr/local/proyectos/ml_sirec/` (incluye `.venv/`, `modelos/`) | `sirec-ml.service` → `127.0.0.1:8000` |
| Frontend React (build) | `/usr/local/proyectos/frontend_sirec/` | servido por Nginx |
| Vhost de Nginx | `/etc/nginx/sites-available/sirec` (enlazado en `sites-enabled/`) | 80 (443 tras Certbot) |
| Secretos del backend | `/etc/sirec/sirec-api.env` (root, `600`) | `EnvironmentFile` de systemd |
| Modo del clasificador | `/etc/sirec/sirec-ml.env` (`SIREC_MODO`) | `EnvironmentFile` de systemd |

El código fuente sigue en `/home/ubuntu/proyectos/sirec`; en `/usr/local/proyectos` solo vive el
resultado del build, una carpeta por componente desplegable.

## 3. Software instalado en la instancia

- **.NET 8.0.423 (SDK) + runtime 8.0.29**, instalados con `dotnet-install.sh` en `/usr/lib/dotnet`,
  **en paralelo** al .NET 10 que ya traía la máquina (el `global.json` del proyecto exige la banda 8.0.4xx).
- **Python 3.14** con venv propio del microservicio: `fastapi 0.141.1`, `uvicorn 0.52.0`,
  `pydantic 2.13.4`, `torch 2.13.0+cpu`, `transformers 4.57.6` (congelado en
  `/usr/local/proyectos/ml_sirec/requirements-instalado.txt`).
- **PostgreSQL 18** (ya instalado): base `sirec`, usuario dedicado `sirec_user`,
  `listen_addresses = localhost`. El esquema lo aplica EF Core al arrancar (`db.Database.Migrate()`):
  existen `reportes` y `__EFMigrationsHistory`.
- **Nginx 1.28.3** y **Certbot 4.0.0** (ya instalados por el proyecto anterior).

## 4. Configuración de producción

### 4.1 Acceso al panel de la ciudadanía

| | |
|---|---|
| **URL** | https://sirec.ameinnovate.com |
| **Usuario** | `sirec` |
| **Contraseña** | `123456a` |

El formulario público de reportes es la portada; el panel del operador (reportes ordenados por
urgencia, con cambio de estado) está detrás del login. La sesión dura 8 horas
(`Jwt__MinutosVigencia=480`).

> 🔴 **Credencial deliberadamente simple, elegida por el equipo el 2026-07-31 para la demo y la
> defensa.** Sirve mientras el panel solo contenga reportes de prueba. **Si en algún momento entran
> reportes reales de ciudadanos, hay que cambiarla**: el panel es alcanzable desde internet y los
> reportes guardan `telefono` y `colonia`, así que una contraseña adivinable expone datos personales.
>
> Cambiarla son dos pasos: editar `Operador__Usuario` / `Operador__Contrasena` en
> `/etc/sirec/sirec-api.env` y `sudo systemctl restart sirec-api`. Hazlo también **antes de hacer este
> repositorio público o compartirlo con el evaluador** — el historial de git es permanente, así que
> borrar la contraseña de este archivo más adelante **no** la quita de los commits anteriores.
> `Jwt__Secreto` y la contraseña de `sirec_user` siguen viviendo solo en ese archivo y **no** están en
> el repo.

### 4.2 Variables de producción (fuera del repositorio)

`/etc/sirec/sirec-api.env` contiene cadena de conexión, secreto JWT, credenciales del operador,
URL del clasificador y CORS. Todo distinto a los valores de desarrollo de
`appsettings.Development.json`; el login con la contraseña de desarrollo (`sirec-local`) responde
**401** en producción (verificado).

### 4.3 Recompilar y redesplegar

El frontend se compila con base de API vacía (`frontend/.env.production` → `VITE_API_URL=`), de modo
que `api.js` pide `/api/...` al mismo host. Reconstruir y redesplegar:

```bash
cd /home/ubuntu/proyectos/sirec/frontend && npm run build
rsync -a --delete dist/ /usr/local/proyectos/frontend_sirec/
```

Redesplegar el backend:

```bash
cd /home/ubuntu/proyectos/sirec/backend-api
dotnet publish -c Release -o /usr/local/proyectos/backend_sirec
sudo systemctl restart sirec-api
```

## 5. Verificación de extremo a extremo (ejecutada, sección 4 del plan de AWS)

Todo por Nginx (`Host: sirec.ameinnovate.com`), con los datos de prueba borrados al final:

| Prueba | Resultado |
|---|---|
| `GET /` y `GET /panel` (fallback SPA) | 200, sirve `index.html` |
| `POST /api/reportes` público | 201, clasificado (`deslave`/`alta`, `inundacion`/`media`) |
| `POST /api/auth/login` con credenciales de producción | 200 + JWT |
| `POST /api/auth/login` con credenciales de desarrollo | 401 |
| `GET /api/reportes` sin token | 401 |
| `GET /api/reportes` con token | lista ordenada por urgencia (alta → media) |
| `PATCH /api/reportes/{id}/estado` (`pendiente→en_atencion→atendido`) | 200 |
| `GET /api/reportes/resumen` | contadores correctos |
| **Resiliencia B2:** `systemctl stop sirec-ml` y enviar reporte | 201 con `otro`/`media` y `requiereRevision: true` — no se pierde el reporte |
| `GET /salud` del microservicio | `{"estado":"ok","modo":"modelo"}` (BETO real, desde 2026-07-31) |
| Puertos 5000 / 8000 / 5432 desde la IP pública | cerrados |
| Reinicio automático | ambos servicios `enabled` (arrancan al bootear) y `Restart=on-failure` |

## 6. Pendientes conocidos

1. ~~**El microservicio corre en modo `simulado`.**~~ ✅ **Resuelto (2026-07-31).** BETO real activo.
   Los pesos se copiaron con `rsync -a --exclude 'checkpoint-*'` desde `/home/ubuntu/modelos/` a
   `/usr/local/proyectos/ml_sirec/modelos/` (840 MB; se excluyeron los cuatro `checkpoint-*` de cada
   tarea, ~1.7 GB de peso muerto que `from_pretrained` no usa) y `SIREC_MODO` pasó a `modelo`.

   Dos advertencias del corte anterior quedaron descartadas al verificarlas:
   - **Los pesos no estaban truncados.** `model.safetensors` mide 439 MB en cada carpeta; la lectura
     de 911 KB que se había anotado era errónea. No hubo que volver a bajar nada de Colab.
   - **El desfase de `transformers` no importó.** Los modelos se guardaron con 5.12.1 y la instancia
     tiene 4.57.6; se probó la carga contra el venv de producción *antes* de cambiar el modo y ambos
     modelos cargaron con su `id2label` correcto. No se tocó la versión instalada.

   Verificación de punta a punta por Nginx (`POST https://sirec.ameinnovate.com/api/reportes`), con
   las confianzas reales que devuelve el softmax:

   | Texto del reporte | Categoría | Urgencia |
   |---|---|---|
   | "Se metio el agua a mi casa… ya nos llega a la rodilla" | `inundacion` 0.9873 | `media` 0.9921 |
   | "Hay un poste caido con cables sobre la avenida" | `caida_poste_cable` 0.9902 | `media` 0.9828 |
   | "Se derrumbo el cerro y hay una familia atrapada" | `persona_en_riesgo` 0.9765 | `alta` 0.9989 |
   | "Ya paso el norte, solo quedo basura en la banqueta" | `otro` 0.9238 | `baja` 0.9985 |

   El tercer caso confirma la **regla de desempate** de `guia_etiquetado.md` (persona en peligro gana
   sobre el fenómeno: `persona_en_riesgo`, no `deslave`), y el cuarto acierta `urgencia=baja`, la clase
   que el reporte de evaluación marcaba como frágil. Las confianzas ya varían (0.9238–0.9989) en vez
   del 0.9 fijo del modo simulado, así que **los números ya sirven para la defensa académica**.

   Huella en la instancia: 309 MB de RSS con ambos modelos cargados — muy por debajo de los ~2 GB
   estimados, porque `safetensors` mapea los pesos con mmap en lugar de copiarlos a memoria. La carga
   es perezosa (`lru_cache`): la primera petición tras un reinicio tarda unos segundos y las
   siguientes responden en ~0.5 s.
2. ~~**HTTPS pendiente de DNS.**~~ ✅ **Resuelto (2026-07-31).** El registro A
   `sirec.ameinnovate.com → 13.221.48.89` ya resuelve y Certbot emitió el certificado
   (Let's Encrypt, clave ECDSA; renovación configurada en
   `/etc/letsencrypt/renewal/sirec.ameinnovate.com.conf` con autenticador e instalador `nginx`).
   El vhost redirige 80 → 443 y el sitio responde por HTTPS.
3. **`ufw` está inactivo** (igual que antes de este despliegue). El filtrado lo hace el Security Group.
   Si se quiere defensa en profundidad: `sudo ufw allow 22,80,443/tcp && sudo ufw enable`.
4. **Sin respaldo de la base.** Para la defensa conviene un `pg_dump` de `sirec` antes y después de la demo.

## 7. Desviaciones respecto a `PLAN_SIREC_AWS_Despliegue.md`

| Plan | Realidad | Motivo |
|---|---|---|
| Rutas `/var/www/sirec-api` y `/var/www/sirec-frontend` | `/usr/local/proyectos/backend_sirec`, `frontend_sirec`, `ml_sirec` | convención de la máquina: un directorio por ensamblado desplegado bajo `/usr/local/proyectos` |
| `VITE_API_URL=/api` | `VITE_API_URL=` (vacío) | `api.js` ya concatena `/api/...`; con `/api` quedaría `/api/api/...` |
| Gunicorn + workers Uvicorn | Uvicorn con `--workers 1` | un solo proceso evita duplicar BETO en memoria; la carga es de una demo |
| `dotnet ef database update` | migración automática al arrancar | `Program.cs` ya llama a `db.Database.Migrate()` |
| Instalar PostgreSQL/Nginx/Certbot | ya estaban (proyecto `coleccion`) | instancia compartida |
| t3.small/medium exclusiva | instancia compartida con `coleccion` | 7.6 GB de RAM alcanzan para ambos + BETO (~2 GB) |
