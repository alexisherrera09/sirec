using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace SirecApi.Migrations
{
    /// <inheritdoc />
    public partial class InicialReportes : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "reportes",
                columns: table => new
                {
                    Id = table.Column<Guid>(type: "uuid", nullable: false),
                    Texto = table.Column<string>(type: "text", nullable: false),
                    Colonia = table.Column<string>(type: "text", nullable: true),
                    Telefono = table.Column<string>(type: "text", nullable: true),
                    Categoria = table.Column<string>(type: "text", nullable: false),
                    Urgencia = table.Column<string>(type: "text", nullable: false),
                    ConfianzaCategoria = table.Column<double>(type: "double precision", nullable: false),
                    ConfianzaUrgencia = table.Column<double>(type: "double precision", nullable: false),
                    Estado = table.Column<string>(type: "text", nullable: false),
                    RequiereRevision = table.Column<bool>(type: "boolean", nullable: false),
                    CreadoEn = table.Column<DateTimeOffset>(type: "timestamp with time zone", nullable: false, defaultValueSql: "now()")
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_reportes", x => x.Id);
                });

            migrationBuilder.CreateIndex(
                name: "IX_reportes_Categoria",
                table: "reportes",
                column: "Categoria");

            migrationBuilder.CreateIndex(
                name: "IX_reportes_CreadoEn",
                table: "reportes",
                column: "CreadoEn");

            migrationBuilder.CreateIndex(
                name: "IX_reportes_Estado",
                table: "reportes",
                column: "Estado");

            migrationBuilder.CreateIndex(
                name: "IX_reportes_Urgencia",
                table: "reportes",
                column: "Urgencia");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "reportes");
        }
    }
}
