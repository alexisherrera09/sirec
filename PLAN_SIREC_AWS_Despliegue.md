# SIREC — Plan de despliegue en AWS

> Documento de especificación para Claude Code.
> Se ejecuta SOLO DESPUÉS de que el sistema completo funcione en local
> (ver PLAN_SIREC_ClaudeCode_total.md, CHECKPOINT C2 y CHECKPOINT A2 superados).
>
> **Topología acordada (2026-07-13): SOLO EC2 + Route 53.** Todo (frontend, backend,
> microservicio, base de datos, HTTPS) vive en UNA instancia EC2; Route 53 solo aporta el DNS.
> **No se usa S3 ni CloudFront.** El equipo ya tiene un dominio en Route 53.
>
> ⚠️ **[PENDIENTE / recordatorio para Claude Code]** El dominio real aún no está definido en este
> documento; en todo el plan aparece como marcador `sirec.midominio.com`. **Al iniciar el despliegue,
> lo PRIMERO es preguntarle a Alexis cuál es el dominio/subdominio exacto** y sustituirlo en el registro
> A de Route 53, en la configuración de Nginx, en el comando de Certbot y en `VITE_API_URL` del frontend.

---

## 0. Arquitectura de despliegue

Todo el sistema corre en **una sola instancia EC2** (igual que en local, pero con Nginx y HTTPS
al frente). El frontend se sirve como archivos estáticos desde el mismo Nginx que hace de proxy de la API.

| Componente | Dónde vive en AWS | Notas |
|---|---|---|
| **Frontend React** (build estático) | **EC2** — servido por **Nginx** en `/` | Archivos de `dist/`; no necesita servidor propio |
| **Backend .NET 8** | **EC2** (systemd, `localhost:5000`) | Proceso continuo |
| **Microservicio Python (BETO)** | **EC2** (systemd, `localhost:8000`) | Modelo en memoria |
| **PostgreSQL** | **EC2** (`localhost:5432`) | Base de datos |
| **Nginx** | **EC2** | Sirve el frontend **y** hace proxy de `/api` al backend; único proceso expuesto (80/443) |
| **DNS** | **Route 53** | Registro A del dominio → **IP Elástica** de la instancia |

**Ventaja de esta topología:** frontend y API quedan en el **mismo dominio y mismo origen**, así que
**no hay problema de CORS ni de contenido mixto** (ambos por HTTPS, mismo host). El microservicio Python,
el backend .NET y PostgreSQL solo escuchan en `localhost` y jamás se exponen a internet.

---

## 1. Diagrama de flujo en producción

```
Ciudadano / Operador (navegador)
        │
        └──► https://sirec.midominio.com   (Route 53 → IP Elástica → Nginx en EC2, HTTPS)
                  │
                  ├──► /            → Nginx sirve el frontend React estático (/var/www/sirec-frontend)
                  │
                  └──► /api/*       → proxy a Backend .NET 8 (Kestrel, localhost:5000, systemd)
                                          │
                                          ├──► PostgreSQL (localhost:5432)
                                          │
                                          └──► Microservicio Python (localhost:8000, systemd)
                                                     │
                                                     └──► Modelo BETO cargado en memoria
```

---

## 2. Recursos de AWS (los crea el equipo en la consola / Route 53)

Esta es la parte que Claude Code **no** puede hacer desde la instancia; el equipo la prepara antes:

### 2.1 Instancia EC2
- Tipo: **t3.small** (2 GB) o **t3.medium** (4 GB) si hay créditos educativos. BETO en memoria consume
  ~1.5–2 GB; con PostgreSQL y .NET, una t3.micro (1 GB) se queda corta.
- SO: **Ubuntu Server 24.04 LTS**.
- **IP Elástica** asociada a la instancia (para que la IP no cambie al apagar/encender).
- **AWS Budgets con alerta a $5 USD** configurado **antes** de crear recursos.

### 2.2 Security Group (firewall de la instancia) — CRÍTICO
| Puerto | Origen permitido | Uso |
|---|---|---|
| 22 (SSH) | **Solo la IP del equipo** | Administración |
| 80 (HTTP) | 0.0.0.0/0 | Redirección a HTTPS + reto de Certbot |
| 443 (HTTPS) | 0.0.0.0/0 | Todo el tráfico público (frontend + API) |
| 5432 (PostgreSQL) | **Ninguno** | Solo localhost, nunca exponer |
| 8000 (Python) | **Ninguno** | Solo localhost, nunca exponer |
| 5000 (.NET) | **Ninguno** | Solo localhost; Nginx es el único que lo toca |

### 2.3 Route 53 (DNS)
- Crear un **registro A** para el dominio/subdominio elegido (ej. `sirec.midominio.com`) → **IP Elástica** de la instancia.
- Este registro debe existir y propagarse **antes** de que Claude Code corra Certbot (el certificado
  se valida contra el dominio y necesita el puerto 80 abierto).

**CHECKPOINT 2:** `dig +short sirec.midominio.com` (o `nslookup`) devuelve la IP Elástica de la instancia.

---

## 3. Configuración de la instancia (la hace Claude Code por SSH)

### 3.1 Instalación base
Pasos en orden, cada uno con su verificación:

1. **Actualizar el sistema:** `sudo apt update && sudo apt upgrade -y`
2. **Instalar .NET 8 runtime** (repositorio oficial de Microsoft para Ubuntu 24.04).
   - Verificar: `dotnet --version` → 8.x
3. **Instalar Python 3.11+ y venv:** `sudo apt install python3 python3-pip python3-venv -y`
4. **Instalar PostgreSQL 16:** `sudo apt install postgresql postgresql-contrib -y`
   - Verificar: `sudo systemctl status postgresql` (`active`)
5. **Instalar Nginx:** `sudo apt install nginx -y`
6. **Instalar Certbot:** `sudo apt install certbot python3-certbot-nginx -y`
7. **(Opcional) Firewall del SO** `ufw`: permitir 22/80/443, denegar el resto (defensa en profundidad
   además del Security Group).

### 3.2 Base de datos PostgreSQL
- Crear base de datos y **usuario dedicado** para SIREC (no usar el superusuario `postgres` desde la app).
- PostgreSQL escuchando **solo en localhost** (`listen_addresses = 'localhost'`).
- Migrar el esquema con EF Core (`dotnet ef database update`) usando la cadena de conexión de producción.

**CHECKPOINT 3.2:** `psql -U sirec_user -d sirec -h localhost` conecta y la tabla `reportes` existe.

### 3.3 Backend .NET como servicio systemd
- Publicar en release: `dotnet publish -c Release -o /var/www/sirec-api`
- Servicio systemd (`/etc/systemd/system/sirec-api.service`) que ejecute la DLL escuchando en `http://localhost:5000`.
- Variables de entorno de producción (cadena de conexión, URL del microservicio, secreto JWT) en el
  archivo de servicio o un `.env` protegido, **nunca en el código fuente**.
- `sudo systemctl enable sirec-api && sudo systemctl start sirec-api`

**CHECKPOINT 3.3:** `curl http://localhost:5000/api/reportes` (con token válido) responde desde la instancia.

### 3.4 Microservicio Python como servicio systemd
- Entorno virtual con `requirements.txt`; el **modelo BETO** (Fase D5) copiado a la instancia.
- Ejecutar con **Gunicorn + Uvicorn workers** (no `--reload` de desarrollo).
- Servicio systemd (`/etc/systemd/system/sirec-ml.service`) escuchando en `http://localhost:8000`.
- `sudo systemctl enable sirec-ml && sudo systemctl start sirec-ml`

**CHECKPOINT 3.4:** `curl http://localhost:8000/salud` responde `{"estado":"ok","modo":"modelo"}`.

### 3.5 Frontend: build y publicación en la instancia
- La URL base de la API en el frontend debe ser configurable (`VITE_API_URL`). Como frontend y API
  comparten dominio, se usa una **ruta relativa**: `VITE_API_URL=/api`.
- Generar el build de producción: `VITE_API_URL=/api npm run build` → genera `dist/`.
- Copiar el contenido de `dist/` a `/var/www/sirec-frontend`.

### 3.6 Nginx: sirve el frontend + proxy de la API + HTTPS
- Un solo `server` block para el dominio (`sirec.midominio.com`):
  - `location / { root /var/www/sirec-frontend; try_files $uri /index.html; }`
    (el `try_files … /index.html` es el **fallback SPA**: refrescar una ruta interna del panel no da 404).
  - `location /api/ { proxy_pass http://localhost:5000; }` (+ headers `Host`, `X-Forwarded-*`).
- El microservicio Python (8000) **no** se expone; solo el backend .NET le habla por localhost.
- Emitir el certificado HTTPS: `sudo certbot --nginx -d sirec.midominio.com`
- Como es mismo origen, el **CORS del backend se simplifica** (o basta con permitir el propio dominio).

**CHECKPOINT 3.6:** desde fuera de la instancia, `https://sirec.midominio.com` carga el frontend con
HTTPS válido (sin advertencia de certificado), `https://sirec.midominio.com/api/reportes` responde, y
**no** se puede acceder directamente a 5432, 8000 ni 5000.

---

## 4. Verificación final de extremo a extremo en producción

```
1. Abrir https://sirec.midominio.com en el navegador.
2. Enviar un reporte de prueba desde el formulario público.
3. Iniciar sesión en el panel del operador (misma URL).
4. Verificar que el reporte aparece clasificado y priorizado.
5. Cambiar su estado y confirmar que se actualiza.
6. En la instancia, revisar logs (`journalctl -u sirec-api -f` y `journalctl -u sirec-ml -f`)
   y confirmar que no hay errores durante el flujo.
```

Cuando este checkpoint pasa, SIREC funciona de extremo a extremo en producción.

---

## 5. Consideraciones de costo y apagado

- La instancia EC2 cobra por hora encendida. Fuera de las sesiones de trabajo o de la defensa puede
  **detenerse** (no terminarse) para no generar costo, y encenderse de nuevo cuando se necesite.
- Con **IP Elástica** la IP no cambia al apagar/encender, así que el registro de Route 53 sigue válido.
  (Ojo: una IP Elástica **asignada pero no asociada** a una instancia en marcha puede generar un cargo mínimo.)
- Route 53 cobra ~$0.50 USD/mes por hosted zone + consultas (mínimo). No requiere apagado.
- Revisar el AWS Billing Dashboard periódicamente.

---

## 6. Checklist de seguridad antes de la entrega/defensa

- [ ] PostgreSQL no accesible desde internet (solo localhost).
- [ ] Microservicio Python (puerto 8000) no accesible desde internet.
- [ ] Backend .NET (puerto 5000) no accesible directamente desde internet (solo vía Nginx).
- [ ] Security Group: solo 22 (IP del equipo), 80 y 443 abiertos; nada más.
- [ ] HTTPS funcionando (certificado válido de Let's Encrypt, no autofirmado).
- [ ] CORS restringido al propio dominio (o innecesario por ser mismo origen), nunca `*` abierto.
- [ ] Variables sensibles (cadena de conexión, secreto JWT) fuera del código fuente y del repositorio Git.
- [ ] Contraseña de PostgreSQL y credenciales del operador distintas a las de prueba/desarrollo.
