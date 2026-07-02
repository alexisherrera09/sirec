using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;
using Microsoft.IdentityModel.Tokens;

namespace SirecApi.Auth;

/// <summary>Opciones de configuración del JWT (sección Jwt de appsettings).</summary>
public class JwtOptions
{
    public string Secreto { get; set; } = string.Empty;
    public string Emisor { get; set; } = "sirec";
    public string Audiencia { get; set; } = "sirec-panel";
    public int MinutosVigencia { get; set; } = 480;
}

/// <summary>Credenciales del operador (sección Operador de appsettings, Fase B4).</summary>
public class OperadorOptions
{
    public string Usuario { get; set; } = string.Empty;
    public string Contrasena { get; set; } = string.Empty;
}

/// <summary>Genera tokens JWT para el operador autenticado.</summary>
public class JwtService
{
    private readonly JwtOptions _opciones;

    public JwtService(JwtOptions opciones)
    {
        _opciones = opciones;
    }

    /// <summary>Emite un token firmado para el usuario indicado.</summary>
    public (string token, DateTimeOffset expira) GenerarToken(string usuario)
    {
        var clave = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(_opciones.Secreto));
        var credenciales = new SigningCredentials(clave, SecurityAlgorithms.HmacSha256);
        var expira = DateTimeOffset.UtcNow.AddMinutes(_opciones.MinutosVigencia);

        var claims = new[]
        {
            new Claim(JwtRegisteredClaimNames.Sub, usuario),
            new Claim(ClaimTypes.Name, usuario),
            new Claim("rol", "operador"),
        };

        var token = new JwtSecurityToken(
            issuer: _opciones.Emisor,
            audience: _opciones.Audiencia,
            claims: claims,
            expires: expira.UtcDateTime,
            signingCredentials: credenciales);

        return (new JwtSecurityTokenHandler().WriteToken(token), expira);
    }
}
