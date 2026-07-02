using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using SirecApi.Auth;
using SirecApi.Dtos;

namespace SirecApi.Controllers;

/// <summary>
/// Autenticación del operador (Fase B4). Emite un JWT tras validar las
/// credenciales configuradas (no hay registro de usuarios: es un operador fijo).
/// </summary>
[ApiController]
[Route("api/auth")]
public class AuthController : ControllerBase
{
    private readonly OperadorOptions _operador;
    private readonly JwtService _jwt;

    public AuthController(OperadorOptions operador, JwtService jwt)
    {
        _operador = operador;
        _jwt = jwt;
    }

    /// <summary>(PÚBLICO) Valida usuario/contraseña y devuelve un token JWT.</summary>
    [HttpPost("login")]
    [AllowAnonymous]
    public ActionResult<TokenDto> Login([FromBody] LoginDto dto)
    {
        // Comparación simple contra las credenciales de configuración. En producción
        // deben venir de variables de entorno y ser distintas a las de desarrollo.
        var credencialesOk =
            string.Equals(dto.Usuario, _operador.Usuario, StringComparison.Ordinal) &&
            string.Equals(dto.Contrasena, _operador.Contrasena, StringComparison.Ordinal);

        if (!credencialesOk)
            return Unauthorized(new { error = "Usuario o contraseña incorrectos." });

        var (token, expira) = _jwt.GenerarToken(dto.Usuario);
        return new TokenDto { Token = token, Expira = expira };
    }
}
