import { useEffect, useState, useCallback } from "react";
import { Link } from "react-router-dom";
import { login, listarReportes, obtenerResumen, cambiarEstado } from "../api.js";
import {
  CATEGORIAS,
  etiquetaCategoria,
  etiquetaUrgencia,
  etiquetaEstado,
  siguienteEstado,
} from "../contrato.js";
import { tiempoTranscurrido } from "../util.js";

const INTERVALO_POLLING_MS = 12000; // Refresco automático cada 12 s (Fase C2).

// Panel del operador (Fase C2): login, tarjetas priorizadas por urgencia,
// contadores, filtro por categoría y cambio de estado. Refresco por polling.
export default function Panel() {
  const [token, setToken] = useState(null);
  return token ? (
    <TableroOperador token={token} onSalir={() => setToken(null)} />
  ) : (
    <PantallaLogin onLogin={setToken} />
  );
}

function PantallaLogin({ onLogin }) {
  const [usuario, setUsuario] = useState("");
  const [contrasena, setContrasena] = useState("");
  const [error, setError] = useState("");
  const [cargando, setCargando] = useState(false);

  async function manejarLogin(e) {
    e.preventDefault();
    setError("");
    setCargando(true);
    try {
      const { token } = await login({ usuario, contrasena });
      onLogin(token);
    } catch (err) {
      setError(err.message);
    } finally {
      setCargando(false);
    }
  }

  return (
    <main className="contenedor-login">
      <form className="formulario tarjeta-login" onSubmit={manejarLogin}>
        <h1>Panel del operador</h1>
        <label htmlFor="usuario">Usuario</label>
        <input
          id="usuario"
          value={usuario}
          onChange={(e) => setUsuario(e.target.value)}
          autoComplete="username"
          required
        />
        <label htmlFor="contrasena">Contraseña</label>
        <input
          id="contrasena"
          type="password"
          value={contrasena}
          onChange={(e) => setContrasena(e.target.value)}
          autoComplete="current-password"
          required
        />
        {error && <p className="mensaje-error">{error}</p>}
        <button className="boton-primario" type="submit" disabled={cargando}>
          {cargando ? "Entrando…" : "Entrar"}
        </button>
        <Link className="enlace-volver" to="/">
          ← Volver al formulario público
        </Link>
      </form>
    </main>
  );
}

function TableroOperador({ token, onSalir }) {
  const [reportes, setReportes] = useState([]);
  const [resumen, setResumen] = useState({ alta: 0, media: 0, baja: 0, totalHoy: 0 });
  const [filtroCategoria, setFiltroCategoria] = useState("");
  const [error, setError] = useState("");

  const cargar = useCallback(async () => {
    try {
      const [lista, res] = await Promise.all([
        listarReportes(token, { categoria: filtroCategoria || undefined }),
        obtenerResumen(token),
      ]);
      setReportes(lista);
      setResumen(res);
      setError("");
    } catch (err) {
      setError(err.message);
    }
  }, [token, filtroCategoria]);

  // Carga inicial y polling automático.
  useEffect(() => {
    cargar();
    const id = setInterval(cargar, INTERVALO_POLLING_MS);
    return () => clearInterval(id);
  }, [cargar]);

  async function avanzarEstado(reporte) {
    const nuevo = siguienteEstado(reporte.estado);
    if (!nuevo) return;
    try {
      await cambiarEstado(token, reporte.id, nuevo);
      await cargar();
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <main className="contenedor-panel">
      <header className="barra-panel">
        <h1>SIREC · Panel</h1>
        <button className="boton-secundario" onClick={onSalir}>
          Salir
        </button>
      </header>

      <section className="contadores">
        <Contador etiqueta="Alta" valor={resumen.alta} clase="urg-alta" />
        <Contador etiqueta="Media" valor={resumen.media} clase="urg-media" />
        <Contador etiqueta="Baja" valor={resumen.baja} clase="urg-baja" />
        <Contador etiqueta="Hoy" valor={resumen.totalHoy} clase="urg-total" />
      </section>

      <section className="filtros">
        <label htmlFor="filtro">Filtrar por categoría:</label>
        <select
          id="filtro"
          value={filtroCategoria}
          onChange={(e) => setFiltroCategoria(e.target.value)}
        >
          <option value="">Todas</option>
          {Object.entries(CATEGORIAS).map(([valor, etiqueta]) => (
            <option key={valor} value={valor}>
              {etiqueta}
            </option>
          ))}
        </select>
      </section>

      {error && <p className="mensaje-error">{error}</p>}

      <section className="lista-reportes">
        {reportes.length === 0 && <p className="vacio">No hay reportes que mostrar.</p>}
        {reportes.map((r) => (
          <TarjetaReporte key={r.id} reporte={r} onAvanzar={() => avanzarEstado(r)} />
        ))}
      </section>
    </main>
  );
}

function Contador({ etiqueta, valor, clase }) {
  return (
    <div className={`contador ${clase}`}>
      <span className="contador-valor">{valor}</span>
      <span className="contador-etiqueta">{etiqueta}</span>
    </div>
  );
}

function TarjetaReporte({ reporte, onAvanzar }) {
  const siguiente = siguienteEstado(reporte.estado);
  return (
    <article className={`tarjeta-reporte urg-borde-${reporte.urgencia}`}>
      <div className="tarjeta-cabecera">
        <span className={`insignia insignia-${reporte.urgencia}`}>
          {etiquetaUrgencia(reporte.urgencia)}
        </span>
        <span className="categoria">{etiquetaCategoria(reporte.categoria)}</span>
        {reporte.requiereRevision && (
          <span className="insignia insignia-revision" title="El clasificador no respondió; revisar manualmente">
            revisar
          </span>
        )}
      </div>

      <p className="texto-reporte">{reporte.texto}</p>

      <div className="tarjeta-meta">
        {reporte.colonia && <span>📍 {reporte.colonia}</span>}
        {reporte.telefono && <span>📞 {reporte.telefono}</span>}
        <span>🕒 {tiempoTranscurrido(reporte.creadoEn)}</span>
        <span className="confianza">
          conf. cat {Math.round(reporte.confianzaCategoria * 100)}% · urg{" "}
          {Math.round(reporte.confianzaUrgencia * 100)}%
        </span>
      </div>

      <div className="tarjeta-pie">
        <span className={`estado estado-${reporte.estado}`}>
          {etiquetaEstado(reporte.estado)}
        </span>
        {siguiente && (
          <button className="boton-estado" onClick={onAvanzar}>
            Marcar como {etiquetaEstado(siguiente)}
          </button>
        )}
      </div>
    </article>
  );
}
