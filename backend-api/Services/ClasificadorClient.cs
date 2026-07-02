using System.Text.Json;
using System.Text.Json.Serialization;
using SirecApi.Models;

namespace SirecApi.Services;

/// <summary>Resultado de la clasificación (mapea el contrato 1.3 del microservicio).</summary>
public class ResultadoClasificacion
{
    [JsonPropertyName("categoria")]
    public string Categoria { get; set; } = Contrato.CategoriaFallback;

    [JsonPropertyName("urgencia")]
    public string Urgencia { get; set; } = Contrato.UrgenciaFallback;

    [JsonPropertyName("confianza_categoria")]
    public double ConfianzaCategoria { get; set; }

    [JsonPropertyName("confianza_urgencia")]
    public double ConfianzaUrgencia { get; set; }

    /// <summary>
    /// True si este resultado proviene del fallback (el microservicio no respondió),
    /// en cuyo caso el reporte debe marcarse para revisión humana.
    /// </summary>
    [JsonIgnore]
    public bool EsFallback { get; set; }
}

/// <summary>
/// Cliente HTTP que consume el microservicio de clasificación Python (contrato 1.3).
/// Implementa la resiliencia exigida en la Fase B2: si el microservicio no responde,
/// nunca se pierde el reporte; se devuelve un resultado de respaldo marcado como
/// que requiere revisión humana.
/// </summary>
public class ClasificadorClient
{
    private readonly HttpClient _http;
    private readonly ILogger<ClasificadorClient> _logger;

    private static readonly JsonSerializerOptions OpcionesJson = new()
    {
        PropertyNameCaseInsensitive = true,
    };

    public ClasificadorClient(HttpClient http, ILogger<ClasificadorClient> logger)
    {
        _http = http;
        _logger = logger;
    }

    /// <summary>
    /// Clasifica un texto llamando al microservicio. Ante cualquier fallo (timeout,
    /// error de red, respuesta inválida) registra el problema y devuelve el fallback
    /// (otro/media) con EsFallback=true, para no perder nunca el reporte.
    /// </summary>
    public async Task<ResultadoClasificacion> ClasificarAsync(string texto, CancellationToken ct = default)
    {
        try
        {
            var respuesta = await _http.PostAsJsonAsync("/clasificar", new { texto }, ct);
            respuesta.EnsureSuccessStatusCode();

            var resultado = await respuesta.Content.ReadFromJsonAsync<ResultadoClasificacion>(OpcionesJson, ct);
            if (resultado is null || !EsValido(resultado))
            {
                _logger.LogWarning("El microservicio devolvió una respuesta inválida; se usa el fallback.");
                return Fallback();
            }

            return resultado;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Fallo al llamar al microservicio de clasificación; se usa el fallback.");
            return Fallback();
        }
    }

    /// <summary>Verifica que categoría y urgencia pertenezcan al contrato.</summary>
    private static bool EsValido(ResultadoClasificacion r) =>
        Contrato.Categorias.Contains(r.Categoria) && Contrato.Urgencias.Contains(r.Urgencia);

    private static ResultadoClasificacion Fallback() => new()
    {
        Categoria = Contrato.CategoriaFallback,
        Urgencia = Contrato.UrgenciaFallback,
        ConfianzaCategoria = 0.0,
        ConfianzaUrgencia = 0.0,
        EsFallback = true,
    };
}
