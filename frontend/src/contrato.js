// Etiquetas visibles del contrato de datos (sección 1 del plan).
// Fuente única de verdad del frontend para categorías y urgencias.
// NO debe divergir del backend .NET ni del microservicio Python.

export const CATEGORIAS = {
  inundacion: "Inundación",
  persona_en_riesgo: "Persona en riesgo",
  caida_poste_cable: "Caída de poste o cable",
  deslave: "Deslave",
  incendio: "Incendio",
  dano_estructural: "Daño estructural",
  otro: "Otro",
};

export const URGENCIAS = {
  alta: "Alta",
  media: "Media",
  baja: "Baja",
};

export const ESTADOS = {
  pendiente: "Pendiente",
  en_atencion: "En atención",
  atendido: "Atendido",
};

// Etiqueta visible con respaldo por si llegara un valor no mapeado.
export const etiquetaCategoria = (c) => CATEGORIAS[c] ?? c;
export const etiquetaUrgencia = (u) => URGENCIAS[u] ?? u;
export const etiquetaEstado = (e) => ESTADOS[e] ?? e;

// Siguiente estado en el flujo pendiente → en_atencion → atendido (null si es final).
export const siguienteEstado = (estado) =>
  ({ pendiente: "en_atencion", en_atencion: "atendido" }[estado] ?? null);
