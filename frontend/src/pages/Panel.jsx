import { useEffect, useState, useCallback } from "react";
import { Link } from "react-router-dom";
import { login, listarReportes, obtenerResumen, cambiarEstado } from "../api.js";
import {
  CATEGORIAS,
  URGENCIAS,
  ESTADOS,
  etiquetaCategoria,
  etiquetaUrgencia,
  etiquetaEstado,
  siguienteEstado,
} from "../contrato.js";
import { tiempoTranscurrido } from "../util.js";

const INTERVALO_POLLING_MS = 12000; // Refresco automático cada 12 s (Fase C2).
const RETARDO_BUSQUEDA_MS = 350; // Espera antes de consultar mientras se escribe.

// Un filtro por cada campo del modelo 1.4. Cadena vacía = sin filtrar.
const FILTROS_VACIOS = {
  texto: "",
  colonia: "",
  telefono: "",
  categoria: "",
  urgencia: "",
  estado: "",
  requiereRevision: "",
  bandaConfCategoria: "",
  bandaConfUrgencia: "",
  desde: "",
  hasta: "",
};

// Bandas de confianza del clasificador. Los topes no se traslapan porque la API
// redondea las confianzas a 4 decimales: 0.8999 es el valor más alto por debajo de 0.9.
const BANDAS_CONFIANZA = {
  alta: { etiqueta: "Alta (≥ 90%)", min: 0.9 },
  media: { etiqueta: "Media (70–90%)", min: 0.7, max: 0.8999 },
  baja: { etiqueta: "Baja (< 70%)", max: 0.6999 },
};

// Traduce el estado del formulario a los parámetros que espera la API.
function aParametrosDeConsulta(f) {
  const params = {
    texto: f.texto.trim(),
    colonia: f.colonia.trim(),
    telefono: f.telefono.trim(),
    categoria: f.categoria,
    urgencia: f.urgencia,
    estado: f.estado,
    requiereRevision: f.requiereRevision,
    desde: f.desde,
    hasta: f.hasta,
  };
  const banda = (clave, prefijo) => {
    const b = BANDAS_CONFIANZA[f[clave]];
    if (!b) return;
    if (b.min !== undefined) params[`${prefijo}Min`] = b.min;
    if (b.max !== undefined) params[`${prefijo}Max`] = b.max;
  };
  banda("bandaConfCategoria", "confianzaCategoria");
  banda("bandaConfUrgencia", "confianzaUrgencia");
  return params;
}

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
  const [filtros, setFiltros] = useState(FILTROS_VACIOS);
  // Los campos de texto no consultan en cada tecla: se aplica el filtro tras una pausa.
  const [filtrosAplicados, setFiltrosAplicados] = useState(FILTROS_VACIOS);
  const [error, setError] = useState("");

  useEffect(() => {
    const id = setTimeout(() => setFiltrosAplicados(filtros), RETARDO_BUSQUEDA_MS);
    return () => clearTimeout(id);
  }, [filtros]);

  const cargar = useCallback(async () => {
    try {
      const [lista, res] = await Promise.all([
        listarReportes(token, aParametrosDeConsulta(filtrosAplicados)),
        obtenerResumen(token),
      ]);
      setReportes(lista);
      setResumen(res);
      setError("");
    } catch (err) {
      setError(err.message);
    }
  }, [token, filtrosAplicados]);

  const cambiar = (campo) => (e) =>
    setFiltros((f) => ({ ...f, [campo]: e.target.value }));
  const hayFiltros = Object.values(filtros).some((v) => v !== "");

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

      <section className="filtros" aria-label="Filtros de reportes">
        <div className="filtros-encabezado">
          <h2>Filtros</h2>
          <button
            className="boton-secundario boton-limpiar"
            onClick={() => setFiltros(FILTROS_VACIOS)}
            disabled={!hayFiltros}
          >
            Limpiar filtros
          </button>
        </div>

        <div className="filtros-rejilla">
          <Campo id="f-texto" etiqueta="Buscar en el texto">
            <input
              id="f-texto"
              type="search"
              placeholder="p. ej. agua, poste, atrapado"
              value={filtros.texto}
              onChange={cambiar("texto")}
            />
          </Campo>

          <Campo id="f-colonia" etiqueta="Colonia">
            <input
              id="f-colonia"
              type="search"
              placeholder="p. ej. Las Brisas"
              value={filtros.colonia}
              onChange={cambiar("colonia")}
            />
          </Campo>

          <Campo id="f-telefono" etiqueta="Teléfono">
            <input
              id="f-telefono"
              type="search"
              placeholder="lada o terminación"
              value={filtros.telefono}
              onChange={cambiar("telefono")}
            />
          </Campo>

          <Campo id="f-categoria" etiqueta="Categoría">
            <select id="f-categoria" value={filtros.categoria} onChange={cambiar("categoria")}>
              <option value="">Todas</option>
              {Object.entries(CATEGORIAS).map(([valor, etiqueta]) => (
                <option key={valor} value={valor}>
                  {etiqueta}
                </option>
              ))}
            </select>
          </Campo>

          <Campo id="f-urgencia" etiqueta="Urgencia">
            <select id="f-urgencia" value={filtros.urgencia} onChange={cambiar("urgencia")}>
              <option value="">Todas</option>
              {Object.entries(URGENCIAS).map(([valor, etiqueta]) => (
                <option key={valor} value={valor}>
                  {etiqueta}
                </option>
              ))}
            </select>
          </Campo>

          <Campo id="f-estado" etiqueta="Estado">
            <select id="f-estado" value={filtros.estado} onChange={cambiar("estado")}>
              <option value="">Todos</option>
              {Object.entries(ESTADOS).map(([valor, etiqueta]) => (
                <option key={valor} value={valor}>
                  {etiqueta}
                </option>
              ))}
            </select>
          </Campo>

          <Campo id="f-revision" etiqueta="Revisión manual">
            <select
              id="f-revision"
              value={filtros.requiereRevision}
              onChange={cambiar("requiereRevision")}
            >
              <option value="">Todos</option>
              <option value="true">Solo los marcados</option>
              <option value="false">Solo los no marcados</option>
            </select>
          </Campo>

          <Campo id="f-conf-cat" etiqueta="Confianza de categoría">
            <select
              id="f-conf-cat"
              value={filtros.bandaConfCategoria}
              onChange={cambiar("bandaConfCategoria")}
            >
              <option value="">Cualquiera</option>
              {Object.entries(BANDAS_CONFIANZA).map(([valor, { etiqueta }]) => (
                <option key={valor} value={valor}>
                  {etiqueta}
                </option>
              ))}
            </select>
          </Campo>

          <Campo id="f-conf-urg" etiqueta="Confianza de urgencia">
            <select
              id="f-conf-urg"
              value={filtros.bandaConfUrgencia}
              onChange={cambiar("bandaConfUrgencia")}
            >
              <option value="">Cualquiera</option>
              {Object.entries(BANDAS_CONFIANZA).map(([valor, { etiqueta }]) => (
                <option key={valor} value={valor}>
                  {etiqueta}
                </option>
              ))}
            </select>
          </Campo>

          <Campo id="f-desde" etiqueta="Desde">
            <input id="f-desde" type="date" value={filtros.desde} onChange={cambiar("desde")} />
          </Campo>

          <Campo id="f-hasta" etiqueta="Hasta">
            <input id="f-hasta" type="date" value={filtros.hasta} onChange={cambiar("hasta")} />
          </Campo>
        </div>
      </section>

      {error && <p className="mensaje-error">{error}</p>}

      <p className="conteo-resultados">
        {reportes.length === 1 ? "1 reporte" : `${reportes.length} reportes`}
        {hayFiltros && " con los filtros aplicados"}
      </p>

      <section className="lista-reportes">
        {reportes.length === 0 && (
          <p className="vacio">
            {hayFiltros
              ? "Ningún reporte coincide con los filtros."
              : "No hay reportes que mostrar."}
          </p>
        )}
        {reportes.map((r) => (
          <TarjetaReporte key={r.id} reporte={r} onAvanzar={() => avanzarEstado(r)} />
        ))}
      </section>
    </main>
  );
}

// Envoltura de un filtro: etiqueta asociada a su control.
function Campo({ id, etiqueta, children }) {
  return (
    <div className="filtro-campo">
      <label htmlFor={id}>{etiqueta}</label>
      {children}
    </div>
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
