using System.ComponentModel.DataAnnotations;

namespace SirecApi.Models;

/// <summary>
/// Entidad Reporte (modelo de datos 1.4 del plan). Un reporte ciudadano de
/// emergencia, con su clasificación (categoría + urgencia) y su estado de atención.
/// </summary>
public class Reporte
{
    /// <summary>Identificador único (PK).</summary>
    public Guid Id { get; set; }

    /// <summary>Texto original del reporte ciudadano.</summary>
    [Required]
    public string Texto { get; set; } = string.Empty;

    /// <summary>Colonia (opcional).</summary>
    public string? Colonia { get; set; }

    /// <summary>Teléfono de contacto (opcional).</summary>
    public string? Telefono { get; set; }

    /// <summary>Categoría temática asignada por el clasificador (una de las 7).</summary>
    public string Categoria { get; set; } = Contrato.CategoriaFallback;

    /// <summary>Nivel de urgencia asignado (alta/media/baja).</summary>
    public string Urgencia { get; set; } = Contrato.UrgenciaFallback;

    /// <summary>Confianza del clasificador en la categoría [0,1].</summary>
    public double ConfianzaCategoria { get; set; }

    /// <summary>Confianza del clasificador en la urgencia [0,1].</summary>
    public double ConfianzaUrgencia { get; set; }

    /// <summary>Estado de atención: pendiente / en_atencion / atendido.</summary>
    public string Estado { get; set; } = Contrato.EstadoPendiente;

    /// <summary>
    /// Marca de que el reporte requiere revisión humana porque el clasificador
    /// no respondió y se usó el fallback (resiliencia, Fase B2).
    /// </summary>
    public bool RequiereRevision { get; set; }

    /// <summary>Fecha y hora de creación (UTC, con zona).</summary>
    public DateTimeOffset CreadoEn { get; set; }
}
