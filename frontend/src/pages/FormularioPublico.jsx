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
      setError("Describe la emergencia para poder enviar el reporte.");
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
          <div className="icono-ok" aria-hidden="true">
            ✓
          </div>
          <h1>Reporte recibido</h1>
          <p>
            Tu reporte quedó registrado y se atenderá según su prioridad. Si hay vidas en
            riesgo y todavía no has llamado, marca al <strong>911</strong>.
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
        <div className="marca">
          <h1>SIREC</h1>
          <span className="rotulo">Protección Civil</span>
        </div>
        <p>Reporta una emergencia. No necesitas registrarte.</p>
      </header>

      {/* El aviso del 911 va antes de enviar, no escondido en la confirmación. */}
      <aside className="aviso-911">
        <span aria-hidden="true">⚠</span>
        <span>
          Si hay <strong>vidas en riesgo ahora</strong>, llama al <strong>911</strong>. Este
          formulario registra el reporte para su atención, no sustituye una llamada de
          emergencia.
        </span>
      </aside>

      <form className="formulario" onSubmit={manejarEnvio}>
        <div className="grupo-campo">
          <label htmlFor="texto">¿Qué está pasando? *</label>
          <textarea
            id="texto"
            className="campo-control"
            rows={5}
            placeholder="Ej.: Se está metiendo el agua a mi casa en la calle Hidalgo, ya cubrió la banqueta."
            value={texto}
            onChange={(e) => setTexto(e.target.value)}
            required
          />
          <span className="ayuda-campo">
            Cuenta dónde es y si hay personas en peligro. Con tus palabras está bien.
          </span>
        </div>

        <div className="grupo-campo">
          <label htmlFor="colonia">Colonia (opcional)</label>
          <input
            id="colonia"
            className="campo-control"
            type="text"
            placeholder="Ej.: Las Brisas"
            value={colonia}
            onChange={(e) => setColonia(e.target.value)}
          />
        </div>

        <div className="grupo-campo">
          <label htmlFor="telefono">Teléfono de contacto (opcional)</label>
          <input
            id="telefono"
            className="campo-control"
            type="tel"
            inputMode="tel"
            autoComplete="tel"
            placeholder="Ej.: 229 123 4567"
            value={telefono}
            onChange={(e) => setTelefono(e.target.value)}
          />
          <span className="ayuda-campo">Sirve para llamarte si hace falta más información.</span>
        </div>

        {error && (
          <p className="mensaje-error" role="alert">
            {error}
          </p>
        )}

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
