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
