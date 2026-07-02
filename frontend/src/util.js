// Devuelve una cadena de tiempo transcurrido desde una fecha ISO (ej. "hace 5 min").
export function tiempoTranscurrido(fechaIso) {
  const ahora = new Date();
  const fecha = new Date(fechaIso);
  const segundos = Math.max(0, Math.floor((ahora - fecha) / 1000));

  if (segundos < 60) return "hace unos segundos";
  const minutos = Math.floor(segundos / 60);
  if (minutos < 60) return `hace ${minutos} min`;
  const horas = Math.floor(minutos / 60);
  if (horas < 24) return `hace ${horas} h`;
  const dias = Math.floor(horas / 24);
  return `hace ${dias} d`;
}
