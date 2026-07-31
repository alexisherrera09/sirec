using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using SirecApi.Data;
using SirecApi.Dtos;
using SirecApi.Models;
using SirecApi.Services;

namespace SirecApi.Controllers;

/// <summary>
/// Endpoints de reportes ciudadanos. El POST de creación es público (formulario
/// ciudadano); las rutas del panel requieren autenticación JWT (Fase B4).
/// </summary>
[ApiController]
[Route("api/reportes")]
public class ReportesController : ControllerBase
{
    private readonly SirecDbContext _db;
    private readonly ClasificadorClient _clasificador;
    private readonly ILogger<ReportesController> _logger;

    public ReportesController(SirecDbContext db, ClasificadorClient clasificador, ILogger<ReportesController> logger)
    {
        _db = db;
        _clasificador = clasificador;
        _logger = logger;
    }

    /// <summary>
    /// (PÚBLICO, Fase B2) Recibe un reporte del ciudadano, lo clasifica llamando al
    /// microservicio y lo guarda con estado 'pendiente'. Si el microservicio no
    /// responde, guarda con el fallback y marca requiere_revision (nunca se pierde).
    /// </summary>
    [HttpPost]
    [AllowAnonymous]
    public async Task<ActionResult<ReporteDto>> Crear([FromBody] CrearReporteDto dto, CancellationToken ct)
    {
        if (string.IsNullOrWhiteSpace(dto.Texto))
            return BadRequest(new { error = "El texto del reporte no puede estar vacío." });

        var clasificacion = await _clasificador.ClasificarAsync(dto.Texto.Trim(), ct);

        var reporte = new Reporte
        {
            Id = Guid.NewGuid(),
            Texto = dto.Texto.Trim(),
            Colonia = string.IsNullOrWhiteSpace(dto.Colonia) ? null : dto.Colonia.Trim(),
            Telefono = string.IsNullOrWhiteSpace(dto.Telefono) ? null : dto.Telefono.Trim(),
            Categoria = clasificacion.Categoria,
            Urgencia = clasificacion.Urgencia,
            ConfianzaCategoria = clasificacion.ConfianzaCategoria,
            ConfianzaUrgencia = clasificacion.ConfianzaUrgencia,
            Estado = Contrato.EstadoPendiente,
            RequiereRevision = clasificacion.EsFallback,
            CreadoEn = DateTimeOffset.UtcNow,
        };

        _db.Reportes.Add(reporte);
        await _db.SaveChangesAsync(ct);

        _logger.LogInformation(
            "Reporte {Id} creado: {Categoria}/{Urgencia} (revision={Revision})",
            reporte.Id, reporte.Categoria, reporte.Urgencia, reporte.RequiereRevision);

        return CreatedAtAction(nameof(ObtenerPorId), new { id = reporte.Id }, ReporteDto.DesdeEntidad(reporte));
    }

    /// <summary>(PANEL) Devuelve un reporte por id.</summary>
    [HttpGet("{id:guid}")]
    [Authorize]
    public async Task<ActionResult<ReporteDto>> ObtenerPorId(Guid id, CancellationToken ct)
    {
        var reporte = await _db.Reportes.FindAsync(new object[] { id }, ct);
        return reporte is null ? NotFound() : ReporteDto.DesdeEntidad(reporte);
    }

    /// <summary>
    /// (PANEL, Fase B3) Lista los reportes ordenados por urgencia (alta→media→baja)
    /// y fecha descendente, con filtros opcionales por cualquier campo del modelo 1.4
    /// (ver <see cref="FiltroReportesDto"/>). Los filtros se combinan con AND y se
    /// traducen a SQL: no se trae la tabla a memoria.
    /// </summary>
    [HttpGet]
    [Authorize]
    public async Task<ActionResult<IEnumerable<ReporteDto>>> Listar(
        [FromQuery] FiltroReportesDto filtro,
        CancellationToken ct = default)
    {
        // Los valores de enumeración se validan para no devolver silenciosamente la lista
        // completa cuando el cliente manda una categoría o un estado que no existe.
        if (!string.IsNullOrWhiteSpace(filtro.Categoria) && !Contrato.Categorias.Contains(filtro.Categoria))
            return BadRequest(new { error = $"Categoría inválida. Válidas: {string.Join(", ", Contrato.Categorias)}." });

        if (!string.IsNullOrWhiteSpace(filtro.Urgencia) && !Contrato.Urgencias.Contains(filtro.Urgencia))
            return BadRequest(new { error = $"Urgencia inválida. Válidas: {string.Join(", ", Contrato.Urgencias)}." });

        if (!string.IsNullOrWhiteSpace(filtro.Estado) && !Contrato.Estados.Contains(filtro.Estado))
            return BadRequest(new { error = $"Estado inválido. Válidos: {string.Join(", ", Contrato.Estados)}." });

        if (filtro.Desde is not null && filtro.Hasta is not null && filtro.Desde > filtro.Hasta)
            return BadRequest(new { error = "El rango de fechas está invertido: 'desde' es posterior a 'hasta'." });

        var consulta = _db.Reportes.AsQueryable();

        // --- Búsquedas por subcadena, sin distinguir mayúsculas (ILIKE de PostgreSQL).
        // Se escapan %, _ y \ para que el texto del operador se busque literal.
        if (!string.IsNullOrWhiteSpace(filtro.Texto))
        {
            var patron = $"%{EscaparLike(filtro.Texto)}%";
            consulta = consulta.Where(r => EF.Functions.ILike(r.Texto, patron, @"\"));
        }

        if (!string.IsNullOrWhiteSpace(filtro.Colonia))
        {
            var patron = $"%{EscaparLike(filtro.Colonia)}%";
            consulta = consulta.Where(r => r.Colonia != null && EF.Functions.ILike(r.Colonia, patron, @"\"));
        }

        if (!string.IsNullOrWhiteSpace(filtro.Telefono))
        {
            var patron = $"%{EscaparLike(filtro.Telefono)}%";
            consulta = consulta.Where(r => r.Telefono != null && EF.Functions.ILike(r.Telefono, patron, @"\"));
        }

        // --- Coincidencia exacta de los campos del contrato.
        if (!string.IsNullOrWhiteSpace(filtro.Categoria))
            consulta = consulta.Where(r => r.Categoria == filtro.Categoria);

        if (!string.IsNullOrWhiteSpace(filtro.Urgencia))
            consulta = consulta.Where(r => r.Urgencia == filtro.Urgencia);

        if (!string.IsNullOrWhiteSpace(filtro.Estado))
            consulta = consulta.Where(r => r.Estado == filtro.Estado);

        if (filtro.RequiereRevision is bool revision)
            consulta = consulta.Where(r => r.RequiereRevision == revision);

        // --- Rangos de confianza del clasificador (para auditar clasificaciones dudosas).
        if (filtro.ConfianzaCategoriaMin is double catMin)
            consulta = consulta.Where(r => r.ConfianzaCategoria >= catMin);
        if (filtro.ConfianzaCategoriaMax is double catMax)
            consulta = consulta.Where(r => r.ConfianzaCategoria <= catMax);
        if (filtro.ConfianzaUrgenciaMin is double urgMin)
            consulta = consulta.Where(r => r.ConfianzaUrgencia >= urgMin);
        if (filtro.ConfianzaUrgenciaMax is double urgMax)
            consulta = consulta.Where(r => r.ConfianzaUrgencia <= urgMax);

        // --- Rango de fechas por días completos en UTC. 'hasta' es inclusive, así que se
        // compara contra el inicio del día siguiente (Npgsql exige offset 0 en timestamptz).
        if (filtro.Desde is DateOnly desde)
        {
            var inicio = new DateTimeOffset(desde.ToDateTime(TimeOnly.MinValue), TimeSpan.Zero);
            consulta = consulta.Where(r => r.CreadoEn >= inicio);
        }
        if (filtro.Hasta is DateOnly hasta)
        {
            var fin = new DateTimeOffset(hasta.AddDays(1).ToDateTime(TimeOnly.MinValue), TimeSpan.Zero);
            consulta = consulta.Where(r => r.CreadoEn < fin);
        }

        // Orden por prioridad de urgencia (alta=1) y luego fecha descendente.
        // El CASE se traduce a SQL para no traer todo a memoria.
        var reportes = await consulta
            .OrderBy(r => r.Urgencia == "alta" ? 1 : r.Urgencia == "media" ? 2 : 3)
            .ThenByDescending(r => r.CreadoEn)
            .Select(r => ReporteDto.DesdeEntidad(r))
            .ToListAsync(ct);

        return reportes;
    }

    /// <summary>
    /// Escapa los comodines de LIKE para que la búsqueda del operador sea literal:
    /// quien escriba "50%" busca ese texto, no "cualquier cosa después de 50".
    /// </summary>
    private static string EscaparLike(string valor) => valor
        .Trim()
        .Replace(@"\", @"\\")
        .Replace("%", @"\%")
        .Replace("_", @"\_");

    /// <summary>
    /// (PANEL, Fase B3) Cambia el estado de un reporte respetando las transiciones
    /// válidas: pendiente→en_atencion→atendido. Rechaza transiciones inválidas.
    /// </summary>
    [HttpPatch("{id:guid}/estado")]
    [Authorize]
    public async Task<ActionResult<ReporteDto>> CambiarEstado(Guid id, [FromBody] CambiarEstadoDto dto, CancellationToken ct)
    {
        if (!Contrato.Estados.Contains(dto.Estado))
            return BadRequest(new { error = $"Estado inválido. Válidos: {string.Join(", ", Contrato.Estados)}." });

        var reporte = await _db.Reportes.FindAsync(new object[] { id }, ct);
        if (reporte is null)
            return NotFound();

        if (!Contrato.TransicionValida(reporte.Estado, dto.Estado))
            return BadRequest(new { error = $"Transición inválida: {reporte.Estado} → {dto.Estado}." });

        reporte.Estado = dto.Estado;
        await _db.SaveChangesAsync(ct);

        return ReporteDto.DesdeEntidad(reporte);
    }

    /// <summary>
    /// (PANEL, Fase B3) Contadores para el panel: reportes por urgencia y total de hoy.
    /// </summary>
    [HttpGet("resumen")]
    [Authorize]
    public async Task<ActionResult<ResumenDto>> Resumen(CancellationToken ct)
    {
        // Inicio del día actual en UTC con offset 0 (timestamptz exige offset 0 en Npgsql).
        var hoy = new DateTimeOffset(DateTime.UtcNow.Date, TimeSpan.Zero);

        var resumen = new ResumenDto
        {
            Alta = await _db.Reportes.CountAsync(r => r.Urgencia == "alta", ct),
            Media = await _db.Reportes.CountAsync(r => r.Urgencia == "media", ct),
            Baja = await _db.Reportes.CountAsync(r => r.Urgencia == "baja", ct),
            TotalHoy = await _db.Reportes.CountAsync(r => r.CreadoEn >= hoy, ct),
        };

        return resumen;
    }
}
