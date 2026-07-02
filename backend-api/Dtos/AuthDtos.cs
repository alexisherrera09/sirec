using System.ComponentModel.DataAnnotations;

namespace SirecApi.Dtos;

/// <summary>Credenciales de login del operador (Fase B4).</summary>
public class LoginDto
{
    [Required]
    public string Usuario { get; set; } = string.Empty;

    [Required]
    public string Contrasena { get; set; } = string.Empty;
}

/// <summary>Respuesta con el token JWT emitido.</summary>
public class TokenDto
{
    public string Token { get; set; } = string.Empty;
    public DateTimeOffset Expira { get; set; }
}
