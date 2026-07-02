using System.Text;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.EntityFrameworkCore;
using Microsoft.IdentityModel.Tokens;
using SirecApi.Auth;
using SirecApi.Data;
using SirecApi.Services;

var builder = WebApplication.CreateBuilder(args);

// --- Configuración fuertemente tipada ---
var jwtOptions = builder.Configuration.GetSection("Jwt").Get<JwtOptions>() ?? new JwtOptions();
var operadorOptions = builder.Configuration.GetSection("Operador").Get<OperadorOptions>() ?? new OperadorOptions();
builder.Services.AddSingleton(jwtOptions);
builder.Services.AddSingleton(operadorOptions);
builder.Services.AddSingleton<JwtService>();

// --- Base de datos (EF Core + PostgreSQL) ---
var cadenaConexion = builder.Configuration.GetConnectionString("Sirec")
    ?? "Host=localhost;Port=5433;Database=sirec;Username=postgres;Password=sirec";
builder.Services.AddDbContext<SirecDbContext>(opciones => opciones.UseNpgsql(cadenaConexion));

// --- Cliente HTTP hacia el microservicio de clasificación (contrato 1.3) ---
var urlClasificador = builder.Configuration["Clasificador:Url"] ?? "http://localhost:8000";
builder.Services.AddHttpClient<ClasificadorClient>(cliente =>
{
    cliente.BaseAddress = new Uri(urlClasificador);
    cliente.Timeout = TimeSpan.FromSeconds(5); // Timeout corto: si tarda, se usa el fallback (B2).
});

// --- Autenticación JWT (Fase B4) ---
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(opciones =>
    {
        opciones.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuer = true,
            ValidIssuer = jwtOptions.Emisor,
            ValidateAudience = true,
            ValidAudience = jwtOptions.Audiencia,
            ValidateIssuerSigningKey = true,
            IssuerSigningKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(jwtOptions.Secreto)),
            ValidateLifetime = true,
        };
    });
builder.Services.AddAuthorization();

// --- CORS para el frontend (Fase B5) ---
const string PoliticaCors = "FrontendLocal";
var origenesFrontend = builder.Configuration.GetSection("Cors:Origenes").Get<string[]>()
    ?? new[] { "http://localhost:5173" };
builder.Services.AddCors(opciones =>
{
    opciones.AddPolicy(PoliticaCors, politica =>
        politica.WithOrigins(origenesFrontend)
            .AllowAnyHeader()
            .AllowAnyMethod());
});

builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

// --- Aplica migraciones pendientes al arrancar (comodidad en local) ---
using (var scope = app.Services.CreateScope())
{
    var db = scope.ServiceProvider.GetRequiredService<SirecDbContext>();
    db.Database.Migrate();
}

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

// En local NO se usa HTTPS (comunicación directa por localhost, sección 0 del plan).
app.UseCors(PoliticaCors);
app.UseAuthentication();
app.UseAuthorization();
app.MapControllers();

app.Run();

// Necesario para pruebas de integración con WebApplicationFactory.
public partial class Program { }
