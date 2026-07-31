using System.ComponentModel.DataAnnotations;
using SirecApi.Models;

namespace SirecApi.Dtos;

/// <summary>Cuerpo del POST público /api/reportes (Fase B2).</summary>
public class CrearReporteDto
{
    [Required(ErrorMessage = "El texto del reporte es obligatorio.")]
    [MinLength(1, ErrorMessage = "El texto del reporte no puede estar vacío.")]
    public string Texto { get; set; } = string.Empty;

    public string? Colonia { get; set; }

    public string? Telefono { get; set; }
}

/// <summary>Representación de un reporte que devuelve la API.</summary>
public class ReporteDto
{
    public Guid Id { get; set; }
    public string Texto { get; set; } = string.Empty;
    public string? Colonia { get; set; }
    public string? Telefono { get; set; }
    public string Categoria { get; set; } = string.Empty;
    public string Urgencia { get; set; } = string.Empty;
    public double ConfianzaCategoria { get; set; }
    public double ConfianzaUrgencia { get; set; }
    public string Estado { get; set; } = string.Empty;
    public bool RequiereRevision { get; set; }
    public DateTimeOffset CreadoEn { get; set; }

    public static ReporteDto DesdeEntidad(Reporte r) => new()
    {
        Id = r.Id,
        Texto = r.Texto,
        Colonia = r.Colonia,
        Telefono = r.Telefono,
        Categoria = r.Categoria,
        Urgencia = r.Urgencia,
        ConfianzaCategoria = r.ConfianzaCategoria,
        ConfianzaUrgencia = r.ConfianzaUrgencia,
        Estado = r.Estado,
        RequiereRevision = r.RequiereRevision,
        CreadoEn = r.CreadoEn,
    };
}

/// <summary>
/// Filtros del GET /api/reportes del panel. Todos son opcionales y se combinan con AND.
/// Cubre los campos del modelo 1.4: texto, colonia, teléfono, categoría, urgencia, estado,
/// marca de revisión, las dos confianzas y la fecha de creación.
/// </summary>
public class FiltroReportesDto
{
    /// <summary>Subcadena a buscar en el texto del reporte (sin distinguir mayúsculas ni acentos de más).</summary>
    public string? Texto { get; set; }

    /// <summary>Subcadena a buscar en la colonia.</summary>
    public string? Colonia { get; set; }

    /// <summary>Subcadena a buscar en el teléfono (útil para localizar por lada o terminación).</summary>
    public string? Telefono { get; set; }

    /// <summary>Categoría exacta, una de las 7 del contrato.</summary>
    public string? Categoria { get; set; }

    /// <summary>Urgencia exacta: alta / media / baja.</summary>
    public string? Urgencia { get; set; }

    /// <summary>Estado exacto: pendiente / en_atencion / atendido.</summary>
    public string? Estado { get; set; }

    /// <summary>true = solo los marcados para revisión humana; false = solo los no marcados.</summary>
    public bool? RequiereRevision { get; set; }

    /// <summary>Confianza mínima y máxima de la categoría, en [0,1].</summary>
    public double? ConfianzaCategoriaMin { get; set; }
    public double? ConfianzaCategoriaMax { get; set; }

    /// <summary>Confianza mínima y máxima de la urgencia, en [0,1].</summary>
    public double? ConfianzaUrgenciaMin { get; set; }
    public double? ConfianzaUrgenciaMax { get; set; }

    /// <summary>Fecha de creación desde (inclusive) y hasta (inclusive), en días completos UTC.</summary>
    public DateOnly? Desde { get; set; }
    public DateOnly? Hasta { get; set; }
}

/// <summary>Cuerpo del PATCH /api/reportes/{id}/estado (Fase B3).</summary>
public class CambiarEstadoDto
{
    [Required]
    public string Estado { get; set; } = string.Empty;
}

/// <summary>Resumen de contadores para el panel (Fase B3).</summary>
public class ResumenDto
{
    public int Alta { get; set; }
    public int Media { get; set; }
    public int Baja { get; set; }
    public int TotalHoy { get; set; }
}
