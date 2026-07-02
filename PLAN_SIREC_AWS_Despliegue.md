# SIREC — Plan de despliegue en AWS

> Documento de especificación para Claude Code.
> Se ejecuta SOLO DESPUÉS de que el sistema completo funcione en local
> (ver PLAN_SIREC_ClaudeCode_total.md, CHECKPOINT C2 y CHECKPOINT A2 superados).

---

## 0. Arquitectura de despliegue

A diferencia de local (donde todo corre junto en la misma máquina), en AWS el sistema se reparte en dos lugares:

| Componente | Dónde vive en AWS | Por qué |
|---|---|---|
| **Frontend React** | **S3** (sitio web estático) | Es solo HTML/JS/CSS compilado; no necesita servidor, es más barato y simple en S3 |
| **Backend .NET 8** | **EC2** (bajo systemd) | Necesita ejecutar un proceso continuo |
| **Microservicio Python (BETO)** | **EC2** (misma instancia, bajo systemd) | Necesita ejecutar el modelo en memoria |
| **PostgreSQL** | **EC2** (misma instancia) | Base de datos, vive junto al backend |
| **Nginx** | **EC2** (misma instancia) | Proxy inverso solo para el backend y el microservicio; el frontend NO pasa por aquí |

**Regla clave:** el frontend en S3 le habla a la API directamente por internet (HTTPS), no a través de Nginx ni de la instancia EC2. Nginx en EC2 solo enruta tráfico hacia el backend .NET y, si hace falta exponerlo, hacia el microservicio Python.

---

## 1. Diagrama de flujo en producción

```
Ciudadano / Operador (navegador)
        │
        ├──► S3 (sitio estático: HTML/JS/CSS del frontend React)
        │         │
        │         └──► el JS del navegador llama directo a:
        │
        └──► https://api.dominio.com  (Nginx en EC2, HTTPS)
                  │
                  ├──► Backend .NET 8 (Kestrel, puerto local 5000, vía systemd)
                  │         │
                  │         └──► PostgreSQL (en la misma EC2, solo localhost:5432)
                  │         │
                  │         └──► Microservicio Python (localhost:8000, vía systemd)
                  │                    │
                  │                    └──► Modelo BETO cargado en memoria
```

---

## 2. Parte 1 — Instancia EC2 (backend + microservicio + base de datos)

### 2.1 Elección de instancia
- Mínimo recomendado: **t3.small** (2 GB RAM) o **t3.medium** (4 GB RAM) si hay créditos educativos (AWS Academy/Educate).
- Motivo: BETO cargado en memoria consume ~1.5-2 GB; sumado a PostgreSQL y el backend .NET, una t3.micro (1 GB) se queda corta.
- Sistema operativo: Ubuntu Server 24.04 LTS.
- Configurar **AWS Budgets con alerta a $5 USD** antes de continuar, como medida de seguridad de gasto.

### 2.2 Security Group (firewall de la instancia)
| Puerto | Origen permitido | Uso |
|---|---|---|
| 22 (SSH) | Solo IPs del equipo | Administración |
| 80 (HTTP) | 0.0.0.0/0 | Redirección a HTTPS |
| 443 (HTTPS) | 0.0.0.0/0 | Tráfico de la API hacia el frontend en S3 |
| 5432 (PostgreSQL) | **Ningún origen externo** | Solo localhost, nunca exponer |
| 8000 (Python) | **Ningún origen externo** | Solo localhost, nunca exponer |
| 5000 (.NET) | **Ningún origen externo** | Solo localhost; Nginx es el único que lo toca |

### 2.3 Instalación base en la instancia
Pasos en orden, cada uno con su verificación:

1. **Actualizar el sistema:** `sudo apt update && sudo apt upgrade -y`
2. **Instalar .NET 8 runtime:** seguir el repositorio oficial de Microsoft para Ubuntu 24.04.
   - Verificar: `dotnet --version` debe mostrar 8.x
3. **Instalar Python 3.11+ y pip:** `sudo apt install python3 python3-pip python3-venv -y`
   - Verificar: `python3 --version`
4. **Instalar PostgreSQL 16:** `sudo apt install postgresql postgresql-contrib -y`
   - Verificar: `sudo systemctl status postgresql` (debe estar `active`)
5. **Instalar Nginx:** `sudo apt install nginx -y`
   - Verificar: `sudo systemctl status nginx` (debe estar `active`)
6. **Instalar Certbot (para HTTPS):** `sudo apt install certbot python3-certbot-nginx -y`

### 2.4 Base de datos PostgreSQL
- Crear base de datos y usuario dedicado para SIREC (no usar el superusuario `postgres` desde la app).
- Configurar PostgreSQL para escuchar **solo en localhost** (`listen_addresses = 'localhost'` en `postgresql.conf`).
- Migrar el esquema con Entity Framework Core (`dotnet ef database update`) usando la cadena de conexión de producción.

**CHECKPOINT 2.4:** `psql -U sirec_user -d sirec -h localhost` conecta correctamente y la tabla `reportes` existe.

### 2.5 Backend .NET como servicio systemd
- Publicar el backend en modo release: `dotnet publish -c Release -o /var/www/sirec-api`
- Crear archivo de servicio systemd (`/etc/systemd/system/sirec-api.service`) que ejecute `dotnet /var/www/sirec-api/SIREC.Api.dll`, escuchando en `http://localhost:5000`.
- Variables de entorno de producción (cadena de conexión a PostgreSQL, URL del microservicio Python, secreto JWT) en el archivo de servicio o en un `.env` protegido, **nunca en el código fuente**.
- Habilitar e iniciar: `sudo systemctl enable sirec-api && sudo systemctl start sirec-api`

**CHECKPOINT 2.5:** `curl http://localhost:5000/api/reportes` (con token válido) responde correctamente desde dentro de la instancia.

### 2.6 Microservicio Python como servicio systemd
- Entorno virtual de Python con las dependencias instaladas (`requirements.txt`).
- El modelo BETO entrenado (Componente D, Fase D5) copiado a la instancia.
- Ejecutar con Gunicorn + Uvicorn workers (más robusto que `uvicorn --reload` de desarrollo).
- Crear archivo de servicio systemd (`/etc/systemd/system/sirec-ml.service`) escuchando en `http://localhost:8000`.
- Habilitar e iniciar: `sudo systemctl enable sirec-ml && sudo systemctl start sirec-ml`

**CHECKPOINT 2.6:** `curl http://localhost:8000/salud` desde dentro de la instancia responde `{"estado":"ok","modo":"modelo"}`.

### 2.7 Nginx como proxy inverso + HTTPS
- Configurar un dominio o subdominio apuntando a la IP pública/elástica de la instancia (ej. `api.sirec.ejemplo.com`), o usar un servicio gratuito como DuckDNS si no hay dominio propio.
- Nginx enruta `https://api.sirec.ejemplo.com/*` hacia `http://localhost:5000` (el backend .NET). El microservicio Python (puerto 8000) NO se expone a internet; solo el backend .NET le habla por localhost.
- Generar certificado HTTPS con Certbot: `sudo certbot --nginx -d api.sirec.ejemplo.com`
- Configurar CORS en el backend .NET para aceptar el origen del frontend en S3 (la URL pública del bucket o del dominio asociado).

**CHECKPOINT 2.7:** desde fuera de la instancia (tu laptop), `curl https://api.sirec.ejemplo.com/api/reportes` responde con HTTPS válido (sin advertencia de certificado) y sin poder acceder directamente a los puertos 5432, 8000 ni 5000.

---

## 3. Parte 2 — Frontend en S3 (sitio estático)

### 3.1 Antes de subir: apuntar el frontend a producción
- En el proyecto React, la URL base de la API debe ser configurable (variable de entorno de build, ej. `VITE_API_URL`), no estar fija en `localhost:5000`.
- Generar el build de producción apuntando a la URL real de la API: `VITE_API_URL=https://api.sirec.ejemplo.com npm run build`
- Esto genera una carpeta `dist/` con HTML/CSS/JS estáticos.

### 3.2 Crear y configurar el bucket S3
- Crear un bucket S3 (nombre único, ej. `sirec-frontend`).
- Habilitar **"Static website hosting"** en las propiedades del bucket.
- Documento de índice: `index.html`. Documento de error: `index.html` también (necesario porque React maneja sus propias rutas internas; sin esto, refrescar una página interna del panel daría error 404).
- Política de bucket que permita lectura pública de los objetos (`s3:GetObject`) — el frontend es público por naturaleza, no contiene secretos.

### 3.3 Subir el build
- Subir el contenido de `dist/` a la raíz del bucket (vía consola, AWS CLI `aws s3 sync dist/ s3://sirec-frontend --delete`, o como prefiera Claude Code automatizarlo).

**CHECKPOINT 3.3:** la URL del sitio web de S3 (formato `http://sirec-frontend.s3-website-<region>.amazonaws.com`) carga el formulario público de SIREC.

### 3.4 (Opcional, recomendado) CloudFront delante de S3
- Para tener HTTPS en el frontend (S3 website hosting solo da HTTP) y mejor rendimiento, colocar **CloudFront** delante del bucket S3.
- CloudFront da automáticamente HTTPS con un dominio `*.cloudfront.net`, o un dominio propio con certificado de ACM.
- Si se omite este paso, el frontend quedaría en HTTP mientras la API está en HTTPS, lo cual los navegadores modernos pueden bloquear (contenido mixto). **Por eso se recomienda no omitir este paso** si el tiempo lo permite; si se omite, hay que verificar que no haya bloqueo de contenido mixto antes de la demo.

**CHECKPOINT 3.4:** la URL de CloudFront (o el dominio propio) carga el sitio por HTTPS y el formulario logra comunicarse con la API sin errores de CORS ni de contenido mixto.

---

## 4. Verificación final de extremo a extremo en producción

```
1. Abrir la URL pública del frontend (CloudFront o S3).
2. Enviar un reporte de prueba desde el formulario público.
3. Iniciar sesión en el panel del operador (misma URL del frontend).
4. Verificar que el reporte aparece clasificado y priorizado.
5. Cambiar su estado y confirmar que se actualiza.
6. Verificar en la instancia EC2 (logs de systemd: `journalctl -u sirec-api -f` 
   y `journalctl -u sirec-ml -f`) que no hay errores durante el flujo.
```

Cuando este checkpoint pasa, SIREC está funcionando de extremo a extremo en producción.

---

## 5. Consideraciones de costo y apagado

- La instancia EC2 cobra por hora encendida. Si no se necesita disponibilidad 24/7 (por ejemplo, fuera de las sesiones de trabajo o de la defensa), puede **detenerse** (no terminarse) para no generar costo, y encenderse de nuevo cuando se necesite (la IP pública puede cambiar salvo que se use una IP elástica, lo que afectaría temporalmente al dominio si no se actualiza el DNS).
- S3 y CloudFront tienen costos mínimos y no es necesario apagarlos.
- Revisar AWS Billing Dashboard periódicamente durante el desarrollo.

---

## 6. Checklist de seguridad antes de la entrega/defensa

- [ ] PostgreSQL no accesible desde internet (solo localhost).
- [ ] Microservicio Python (puerto 8000) no accesible desde internet.
- [ ] Backend .NET (puerto 5000) no accesible directamente desde internet (solo vía Nginx).
- [ ] HTTPS funcionando en la API (certificado válido, no autofirmado).
- [ ] CORS configurado solo para el dominio real del frontend, no con `*` abierto.
- [ ] Variables sensibles (cadena de conexión, secreto JWT) fuera del código fuente y fuera del repositorio Git.
- [ ] Contraseña de PostgreSQL y credenciales del operador no son las de prueba/desarrollo.
