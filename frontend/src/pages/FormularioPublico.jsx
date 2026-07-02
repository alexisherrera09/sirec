import { useState } from "react";
import { Link } from "react-router-dom";
import { crearReporte } from "../api.js";

// Formulario público (Fase C1): cualquier ciudadano reporta una emergencia sin
// registro. Móvil primero. Al enviar, confirma que el reporte fue recibido.
export default function FormularioPublico() {
  const [texto, setTexto] = useState("");
  const [colonia, setColonia] = useState("");
  const [telefono, setTelefono] = useState("");
  const [enviando, setEnviando] = useState(false);
  const [enviado, setEnviado] = useState(false);
  const [error, setError] = useState("");

  async function manejarEnvio(e) {
    e.preventDefault();
    setError("");
    if (!texto.trim()) {
      setError("Por favor describe la emergencia.");
      return;
    }
    setEnviando(true);
    try {
      await crearReporte({
        texto: texto.trim(),
        colonia: colonia.trim() || null,
        telefono: telefono.trim() || null,
      });
      setEnviado(true);
      setTexto("");
      setColonia("");
      setTelefono("");
    } catch (err) {
      setError(err.message);
    } finally {
      setEnviando(false);
    }
  }

  if (enviado) {
    return (
      <main className="contenedor-publico">
        <div className="tarjeta-confirmacion">
          <div className="icono-ok">✓</div>
          <h1>Reporte recibido</h1>
          <p>
            Gracias. Tu reporte fue registrado y será atendido según su prioridad.
            Si es una emergencia con vidas en riesgo y no has llamado, marca al 911.
          </p>
          <button className="boton-primario" onClick={() => setEnviado(false)}>
            Enviar otro reporte
          </button>
        </div>
      </main>
    );
  }

  return (
    <main className="contenedor-publico">
      <header className="encabezado-publico">
        <h1>SIREC</h1>
        <p>Reporta una emergencia a Protección Civil</p>
      </header>

      <form className="formulario" onSubmit={manejarEnvio}>
        <label htmlFor="texto">Describe tu emergencia *</label>
        <textarea
          id="texto"
          rows={5}
          placeholder="Ej.: Se está metiendo el agua a mi casa en la calle Hidalgo, ya cubrió la banqueta."
          value={texto}
          onChange={(e) => setTexto(e.target.value)}
          required
        />

        <label htmlFor="colonia">Colonia (opcional)</label>
        <input
          id="colonia"
          type="text"
          placeholder="Ej.: Las Brisas"
          value={colonia}
          onChange={(e) => setColonia(e.target.value)}
        />

        <label htmlFor="telefono">Teléfono de contacto (opcional)</label>
        <input
          id="telefono"
          type="tel"
          placeholder="Ej.: 229 123 4567"
          value={telefono}
          onChange={(e) => setTelefono(e.target.value)}
        />

        {error && <p className="mensaje-error">{error}</p>}

        <button className="boton-primario" type="submit" disabled={enviando}>
          {enviando ? "Enviando…" : "Enviar reporte"}
        </button>
      </form>

      <footer className="pie-publico">
        <Link to="/panel">Acceso operador</Link>
      </footer>
    </main>
  );
}
