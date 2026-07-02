namespace SirecApi.Models;

/// <summary>
/// Contrato de datos compartido (sección 1 del plan). Fuente única de verdad
/// del backend para categorías, urgencias y estados. NO debe divergir del
/// microservicio Python ni del frontend.
/// </summary>
public static class Contrato
{
    /// <summary>Las 7 categorías temáticas fijas (contrato 1.1).</summary>
    public static readonly string[] Categorias =
    {
        "inundacion",
        "persona_en_riesgo",
        "caida_poste_cable",
        "deslave",
        "incendio",
        "dano_estructural",
        "otro",
    };

    /// <summary>Los 3 niveles de urgencia fijos (contrato 1.2).</summary>
    public static readonly string[] Urgencias = { "alta", "media", "baja" };

    /// <summary>Estados del ciclo de vida de un reporte (contrato 1.4).</summary>
    public const string EstadoPendiente = "pendiente";
    public const string EstadoEnAtencion = "en_atencion";
    public const string EstadoAtendido = "atendido";

    public static readonly string[] Estados = { EstadoPendiente, EstadoEnAtencion, EstadoAtendido };

    /// <summary>Categoría/urgencia de respaldo cuando el microservicio no responde (B2).</summary>
    public const string CategoriaFallback = "otro";
    public const string UrgenciaFallback = "media";

    /// <summary>
    /// Prioridad numérica para ordenar en el panel (alta=1 primero, baja=3 último).
    /// Se usa en la consulta del panel (B3).
    /// </summary>
    public static int PrioridadUrgencia(string urgencia) => urgencia switch
    {
        "alta" => 1,
        "media" => 2,
        "baja" => 3,
        _ => 99,
    };

    /// <summary>
    /// Transiciones de estado permitidas (B3): pendiente→en_atencion→atendido.
    /// No se permite retroceder ni saltar etapas.
    /// </summary>
    public static bool TransicionValida(string actual, string nuevo) =>
        (actual, nuevo) switch
        {
            (EstadoPendiente, EstadoEnAtencion) => true,
            (EstadoEnAtencion, EstadoAtendido) => true,
            _ => false,
        };
}
