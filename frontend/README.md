# Frontend — SIREC (Componente C)

Interfaz web en **React + Vite**. Dos vistas:

- **`/`** — Formulario público (sin registro): el ciudadano describe su emergencia.
- **`/panel`** — Panel del operador (con login JWT): tarjetas priorizadas por urgencia,
  contadores, filtro por categoría, cambio de estado y refresco automático (polling 12 s).

Puerto fijo en local: **5173**. La URL de la API va en `VITE_API_URL` (archivo `.env`).

## Requisitos

- **Node.js 20+**. Esta máquina usa `nvm` con Node 16 por defecto.

> **Nota nvm (Windows):** `nvm use 20.x` necesita permisos de administrador para crear
> el symlink `C:\nvm4w\nodejs`. Si `node --version` no muestra la 20, abre una terminal
> **como administrador** y ejecuta `nvm use 20.19.0` una vez (queda fijo a nivel de
> sistema). Alternativa sin admin: invocar Node por su ruta directa
> `C:\Users\<usuario>\AppData\Local\nvm\v20.19.0\`.

## Instalación y arranque

```powershell
cd frontend
npm install
npm run dev
```

Abre http://localhost:5173

Requiere el backend (`http://localhost:5000`) y el microservicio (`http://localhost:8000`)
corriendo. Credenciales del panel en desarrollo: usuario `operador`, contraseña `sirec-local`.

## Configuración

`.env`:
```
VITE_API_URL=http://localhost:5000
```

## Estructura

| Archivo | Función |
|---|---|
| `src/main.jsx` | Ruteo (`/` y `/panel`) |
| `src/pages/FormularioPublico.jsx` | Formulario ciudadano (C1) |
| `src/pages/Panel.jsx` | Login + tablero del operador (C2) |
| `src/api.js` | Cliente de la API .NET |
| `src/contrato.js` | Etiquetas de categorías/urgencias/estados (fuente única del frontend) |
| `src/util.js` | Utilidades (tiempo transcurrido) |
| `src/index.css` | Estilos (móvil primero; rojo=alta, ámbar=media, verde=baja) |
