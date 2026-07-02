"""
Herramienta de etiquetado SIREC (Fase D2).

App local (solo librería estándar de Python, sin dependencias) para etiquetar
reportes uno por uno con categoría y urgencia, según la guia_etiquetado.md.

- Lee un CSV de reportes sin etiquetar (columna obligatoria: `texto`; opcional: `origen`).
- Muestra cada reporte con botones (y atajos de teclado) para las 7 categorías y 3 urgencias.
- Guarda en corpus_etiquetado.csv con columnas: texto, categoria, urgencia, etiquetador, origen.
- Modo DOBLE ETIQUETADO: cada etiquetador escribe su nombre; el mismo subconjunto puede
  ser etiquetado por dos personas de forma independiente. Cada respuesta se guarda por
  separado (identificada por `etiquetador`), lo que permite calcular el kappa de Cohen (D3.4).

Uso:
    py herramienta_etiquetado.py --entrada reportes_sin_etiquetar.csv
Luego abre http://localhost:8080 e ingresa tu nombre de etiquetador.

Nota: no puede etiquetar la IA. Esta herramienta es para que la usen personas (equipo).
"""

import argparse
import csv
import json
import os
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

CATEGORIAS = [
    "inundacion", "persona_en_riesgo", "caida_poste_cable",
    "deslave", "incendio", "dano_estructural", "otro",
]
URGENCIAS = ["alta", "media", "baja"]
COLUMNAS_SALIDA = ["texto", "categoria", "urgencia", "etiquetador", "origen"]

# Candado para escrituras concurrentes al CSV de salida.
_candado = threading.Lock()

# Configuración global (se llena en main()).
CONFIG = {"entrada": "", "salida": "", "origen_por_defecto": "real"}


def cargar_reportes(ruta):
    """Lee el CSV de entrada. Devuelve lista de dicts {texto, origen}."""
    reportes = []
    with open(ruta, encoding="utf-8-sig", newline="") as f:
        lector = csv.DictReader(f)
        if "texto" not in (lector.fieldnames or []):
            raise SystemExit(f"El CSV de entrada debe tener una columna 'texto'. Columnas: {lector.fieldnames}")
        for fila in lector:
            texto = (fila.get("texto") or "").strip()
            if not texto:
                continue
            origen = (fila.get("origen") or CONFIG["origen_por_defecto"]).strip()
            reportes.append({"texto": texto, "origen": origen})
    return reportes


def textos_ya_etiquetados_por(etiquetador):
    """Conjunto de textos que este etiquetador ya guardó (para no repetirlos)."""
    ruta = CONFIG["salida"]
    hechos = set()
    if not os.path.exists(ruta):
        return hechos
    with open(ruta, encoding="utf-8", newline="") as f:
        for fila in csv.DictReader(f):
            if fila.get("etiquetador") == etiquetador:
                hechos.add(fila.get("texto"))
    return hechos


def guardar_etiqueta(registro):
    """Agrega una fila al corpus_etiquetado.csv (crea encabezado si no existe)."""
    ruta = CONFIG["salida"]
    with _candado:
        existe = os.path.exists(ruta)
        with open(ruta, "a", encoding="utf-8", newline="") as f:
            escritor = csv.DictWriter(f, fieldnames=COLUMNAS_SALIDA)
            if not existe:
                escritor.writeheader()
            escritor.writerow(registro)


def progreso(etiquetador):
    """Devuelve (siguiente_reporte | None, hechos, total) para el etiquetador."""
    reportes = cargar_reportes(CONFIG["entrada"])
    hechos = textos_ya_etiquetados_por(etiquetador)
    pendientes = [r for r in reportes if r["texto"] not in hechos]
    siguiente = pendientes[0] if pendientes else None
    return siguiente, len(hechos), len(reportes)


PAGINA = """<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Etiquetado SIREC</title>
<style>
 body{font-family:system-ui,sans-serif;max-width:720px;margin:0 auto;padding:1rem;color:#1f2937}
 h1{color:#1e3a8a}
 .oculto{display:none}
 .texto{background:#fff;border:1px solid #e5e7eb;border-left:6px solid #1d4ed8;border-radius:10px;padding:1rem;font-size:1.15rem;margin:1rem 0}
 .grupo{margin:1rem 0}
 .grupo h3{margin:.25rem 0;color:#6b7280;font-size:.9rem;text-transform:uppercase}
 button.op{margin:.25rem;padding:.6rem .8rem;border:1px solid #cbd5e1;border-radius:8px;background:#fff;cursor:pointer;font-size:1rem}
 button.op:hover{background:#eff6ff}
 button.sel{background:#1d4ed8;color:#fff;border-color:#1d4ed8}
 .barra{display:flex;justify-content:space-between;align-items:center;color:#6b7280}
 .guardar{background:#16a34a;color:#fff;border:none;border-radius:8px;padding:.8rem 1.2rem;font-size:1.05rem;cursor:pointer;margin-top:1rem}
 .guardar:disabled{opacity:.5;cursor:default}
 .saltar{background:#fff;border:1px solid #cbd5e1;border-radius:8px;padding:.8rem 1rem;cursor:pointer;margin-left:.5rem}
 .ayuda{font-size:.8rem;color:#9ca3af}
 kbd{background:#f3f4f6;border:1px solid #d1d5db;border-radius:4px;padding:0 .3rem;font-size:.75rem}
</style></head>
<body>
<h1>Etiquetado SIREC</h1>

<div id="login">
 <p>Escribe tu nombre de etiquetador (para el doble etiquetado, cada persona usa un nombre distinto):</p>
 <input id="nombre" placeholder="ej. ana / luis" style="padding:.6rem;font-size:1rem">
 <button class="guardar" onclick="entrar()">Comenzar</button>
</div>

<div id="app" class="oculto">
 <div class="barra"><span id="quien"></span><span id="prog"></span></div>
 <div class="texto" id="texto"></div>
 <div class="grupo"><h3>Categoría <span class="ayuda">(teclas 1–7)</span></h3><div id="cats"></div></div>
 <div class="grupo"><h3>Urgencia <span class="ayuda">(teclas A / M / B)</span></h3><div id="urgs"></div></div>
 <button class="guardar" id="btnGuardar" onclick="guardar()" disabled>Guardar y siguiente <span class="ayuda">(Enter)</span></button>
 <button class="saltar" onclick="cargar()">Saltar</button>
 <div id="fin" class="oculto"><h2>¡Listo! No hay más reportes pendientes para ti.</h2></div>
</div>

<script>
const CATEGORIAS=%CATS%, URGENCIAS=%URGS%;
let etiquetador="", actual=null, selCat=null, selUrg=null;

function entrar(){ const n=document.getElementById('nombre').value.trim(); if(!n)return;
 etiquetador=n; document.getElementById('login').classList.add('oculto');
 document.getElementById('app').classList.remove('oculto');
 document.getElementById('quien').textContent="Etiquetador: "+etiquetador; render(); cargar(); }

function render(){
 const c=document.getElementById('cats'); c.innerHTML="";
 CATEGORIAS.forEach((cat,i)=>{const b=document.createElement('button');b.className="op";b.textContent=(i+1)+". "+cat;
  b.onclick=()=>{selCat=cat;marcar();};b.dataset.cat=cat;c.appendChild(b);});
 const u=document.getElementById('urgs'); u.innerHTML="";
 URGENCIAS.forEach(urg=>{const b=document.createElement('button');b.className="op";b.textContent=urg.toUpperCase();
  b.onclick=()=>{selUrg=urg;marcar();};b.dataset.urg=urg;u.appendChild(b);});
}
function marcar(){
 document.querySelectorAll('[data-cat]').forEach(b=>b.classList.toggle('sel',b.dataset.cat===selCat));
 document.querySelectorAll('[data-urg]').forEach(b=>b.classList.toggle('sel',b.dataset.urg===selUrg));
 document.getElementById('btnGuardar').disabled=!(selCat&&selUrg);
}
async function cargar(){
 selCat=selUrg=null; marcar();
 const r=await fetch('/api/siguiente?etiquetador='+encodeURIComponent(etiquetador));
 const d=await r.json();
 document.getElementById('prog').textContent=d.hechos+" / "+d.total;
 if(!d.reporte){ document.getElementById('texto').classList.add('oculto'); document.getElementById('fin').classList.remove('oculto');
  document.getElementById('btnGuardar').classList.add('oculto'); return; }
 actual=d.reporte; document.getElementById('texto').textContent=actual.texto;
}
async function guardar(){
 if(!selCat||!selUrg||!actual)return;
 await fetch('/api/etiqueta',{method:'POST',headers:{'Content-Type':'application/json'},
  body:JSON.stringify({texto:actual.texto,categoria:selCat,urgencia:selUrg,etiquetador:etiquetador,origen:actual.origen})});
 cargar();
}
document.addEventListener('keydown',e=>{
 if(document.getElementById('app').classList.contains('oculto'))return;
 if(e.key>='1'&&e.key<='7'){selCat=CATEGORIAS[+e.key-1];marcar();}
 else if(e.key.toLowerCase()==='a'){selUrg='alta';marcar();}
 else if(e.key.toLowerCase()==='m'){selUrg='media';marcar();}
 else if(e.key.toLowerCase()==='b'){selUrg='baja';marcar();}
 else if(e.key==='Enter'&&selCat&&selUrg){guardar();}
});
</script>
</body></html>
"""


class Handler(BaseHTTPRequestHandler):
    def _json(self, obj, codigo=200):
        cuerpo = json.dumps(obj).encode("utf-8")
        self.send_response(codigo)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(cuerpo)))
        self.end_headers()
        self.wfile.write(cuerpo)

    def do_GET(self):
        ruta = urlparse(self.path)
        if ruta.path == "/":
            html = (PAGINA
                    .replace("%CATS%", json.dumps(CATEGORIAS))
                    .replace("%URGS%", json.dumps(URGENCIAS))).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(html)))
            self.end_headers()
            self.wfile.write(html)
        elif ruta.path == "/api/siguiente":
            etiquetador = (parse_qs(ruta.query).get("etiquetador", [""])[0]).strip()
            if not etiquetador:
                return self._json({"error": "falta etiquetador"}, 400)
            siguiente, hechos, total = progreso(etiquetador)
            self._json({"reporte": siguiente, "hechos": hechos, "total": total})
        else:
            self._json({"error": "no encontrado"}, 404)

    def do_POST(self):
        if urlparse(self.path).path != "/api/etiqueta":
            return self._json({"error": "no encontrado"}, 404)
        largo = int(self.headers.get("Content-Length", 0))
        datos = json.loads(self.rfile.read(largo) or b"{}")
        registro = {c: (datos.get(c) or "").strip() for c in COLUMNAS_SALIDA}
        if registro["categoria"] not in CATEGORIAS or registro["urgencia"] not in URGENCIAS:
            return self._json({"error": "categoria/urgencia inválida"}, 422)
        if not registro["texto"] or not registro["etiquetador"]:
            return self._json({"error": "faltan campos"}, 422)
        guardar_etiqueta(registro)
        self._json({"ok": True})

    def log_message(self, *args):
        pass  # Silencio en consola.


def main():
    parser = argparse.ArgumentParser(description="Herramienta de etiquetado SIREC (Fase D2).")
    parser.add_argument("--entrada", default="reportes_sin_etiquetar.csv",
                        help="CSV de reportes sin etiquetar (columna 'texto').")
    parser.add_argument("--salida", default="corpus_etiquetado.csv",
                        help="CSV de salida con las etiquetas.")
    parser.add_argument("--origen", default="real",
                        help="Origen por defecto si el CSV de entrada no trae columna 'origen'.")
    parser.add_argument("--puerto", type=int, default=8080)
    args = parser.parse_args()

    base = os.path.dirname(os.path.abspath(__file__))
    CONFIG["entrada"] = args.entrada if os.path.isabs(args.entrada) else os.path.join(base, args.entrada)
    CONFIG["salida"] = args.salida if os.path.isabs(args.salida) else os.path.join(base, args.salida)
    CONFIG["origen_por_defecto"] = args.origen

    if not os.path.exists(CONFIG["entrada"]):
        raise SystemExit(f"No existe el archivo de entrada: {CONFIG['entrada']}")

    # Validación temprana del CSV.
    total = len(cargar_reportes(CONFIG["entrada"]))
    print(f"Reportes a etiquetar: {total}")
    print(f"Salida: {CONFIG['salida']}")
    print(f"Abre http://localhost:{args.puerto} en el navegador.")
    print("Para doble etiquetado: cada persona ingresa un nombre distinto.")
    ThreadingHTTPServer(("127.0.0.1", args.puerto), Handler).serve_forever()


if __name__ == "__main__":
    main()
