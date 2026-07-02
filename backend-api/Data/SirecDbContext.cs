using Microsoft.EntityFrameworkCore;
using SirecApi.Models;

namespace SirecApi.Data;

/// <summary>
/// Contexto de Entity Framework Core para SIREC. Expone la tabla de reportes
/// y configura el mapeo a PostgreSQL.
/// </summary>
public class SirecDbContext : DbContext
{
    public SirecDbContext(DbContextOptions<SirecDbContext> options) : base(options)
    {
    }

    public DbSet<Reporte> Reportes => Set<Reporte>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        var reporte = modelBuilder.Entity<Reporte>();
        reporte.ToTable("reportes");
        reporte.HasKey(r => r.Id);

        // El valor por defecto de creado_en lo pone la base de datos (now()).
        reporte.Property(r => r.CreadoEn)
            .HasDefaultValueSql("now()");

        // Índices para las consultas del panel (orden por urgencia/fecha y filtros).
        reporte.HasIndex(r => r.Urgencia);
        reporte.HasIndex(r => r.Estado);
        reporte.HasIndex(r => r.Categoria);
        reporte.HasIndex(r => r.CreadoEn);
    }
}
