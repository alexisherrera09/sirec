// Cliente de la API .NET. La URL base viene de la variable de entorno VITE_API_URL.

const BASE = import.meta.env.VITE_API_URL ?? "http://localhost:5000";

// Envía un reporte ciudadano (endpoint público).
export async function crearReporte({ texto, colonia, telefono }) {
  const resp = await fetch(`${BASE}/api/reportes`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ texto, colonia, telefono }),
  });
  if (!resp.ok) {
    const detalle = await resp.text().catch(() => "");
    throw new Error(`No se pudo enviar el reporte (HTTP ${resp.status}). ${detalle}`);
  }
  return resp.json();
}

// Login del operador; devuelve { token, expira }.
export async function login({ usuario, contrasena }) {
  const resp = await fetch(`${BASE}/api/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ usuario, contrasena }),
  });
  if (resp.status === 401) throw new Error("Usuario o contraseña incorrectos.");
  if (!resp.ok) throw new Error(`Error de autenticación (HTTP ${resp.status}).`);
  return resp.json();
}

// Lista de reportes del panel (requiere token). Filtro opcional por categoría.
export async function listarReportes(token, { categoria } = {}) {
  const params = new URLSearchParams();
  if (categoria) params.set("categoria", categoria);
  const url = `${BASE}/api/reportes${params.toString() ? `?${params}` : ""}`;
  const resp = await fetch(url, { headers: { Authorization: `Bearer ${token}` } });
  if (!resp.ok) throw new Error(`No se pudo obtener la lista (HTTP ${resp.status}).`);
  return resp.json();
}

// Contadores del panel (requiere token).
export async function obtenerResumen(token) {
  const resp = await fetch(`${BASE}/api/reportes/resumen`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!resp.ok) throw new Error(`No se pudo obtener el resumen (HTTP ${resp.status}).`);
  return resp.json();
}

// Cambia el estado de un reporte (requiere token).
export async function cambiarEstado(token, id, estado) {
  const resp = await fetch(`${BASE}/api/reportes/${id}/estado`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ estado }),
  });
  if (!resp.ok) {
    const detalle = await resp.text().catch(() => "");
    throw new Error(`No se pudo cambiar el estado (HTTP ${resp.status}). ${detalle}`);
  }
  return resp.json();
}
