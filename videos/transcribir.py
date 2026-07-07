"""
Transcriptor de videos (local, sin conexión, sin gastar tokens de IA).

Usa faster-whisper en CPU. Por cada video genera un archivo Markdown con el
MISMO nombre del video (ej.: "1 Design thinking.mp4" -> "1 Design thinking.md")
en esta misma carpeta.

Uso básico (transcribe todos los videos que aún no tengan su .md):
    cd videos
    py transcribir.py

Elegir modelo (calidad vs tiempo): tiny | base | small | medium | large-v3
    py transcribir.py --modelo medium

Transcribir un video específico:
    py transcribir.py "1 Design thinking.mp4"

Requisito (instalar una sola vez):
    py -m pip install faster-whisper
"""
import argparse
import os
import sys
import time

# La consola de Windows usa cp1252 y no puede imprimir algunos caracteres (→, acentos).
# Forzamos UTF-8 en la salida para que los mensajes de progreso nunca rompan el proceso.
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

VIDEO_EXTS = (".mp4", ".mkv", ".mov", ".avi", ".m4a", ".mp3", ".wav", ".webm")
CARPETA = os.path.dirname(os.path.abspath(__file__))


def hhmmss(s):
    h = int(s // 3600); m = int((s % 3600) // 60); sec = int(s % 60)
    return f"{h:02d}:{m:02d}:{sec:02d}"


def videos_pendientes(carpeta):
    """Videos en la carpeta que todavía no tienen su .md al lado."""
    pend = []
    for nombre in sorted(os.listdir(carpeta)):
        ruta = os.path.join(carpeta, nombre)
        if not os.path.isfile(ruta):
            continue
        base, ext = os.path.splitext(nombre)
        if ext.lower() in VIDEO_EXTS and not os.path.exists(os.path.join(carpeta, base + ".md")):
            pend.append(ruta)
    return pend


def transcribir(ruta_video, model, modelo_nombre, idioma):
    base = os.path.splitext(os.path.basename(ruta_video))[0]
    salida_md = os.path.join(os.path.dirname(ruta_video), base + ".md")
    t0 = time.time()
    print(f"[{time.strftime('%H:%M:%S')}] Transcribiendo: {os.path.basename(ruta_video)}", flush=True)

    segments, info = model.transcribe(
        ruta_video, language=idioma, vad_filter=True,
        vad_parameters=dict(min_silence_duration_ms=500), beam_size=5,
    )
    dur = info.duration or 0
    print(f"[{time.strftime('%H:%M:%S')}] Duración: {hhmmss(dur)}. Procesando...", flush=True)

    # Cabecera + sección con tiempos (escritura incremental para poder monitorear).
    with open(salida_md, "w", encoding="utf-8") as f:
        f.write(f"# Transcripción — {base}\n\n")
        f.write(f"- **Video:** {os.path.basename(ruta_video)}\n")
        f.write(f"- **Duración:** {hhmmss(dur)}\n")
        f.write(f"- **Modelo:** faster-whisper `{modelo_nombre}` (idioma: {info.language})\n")
        f.write(f"- **Generado:** en local, sin conexión\n\n")
        f.write("---\n\n## Transcripción con marcas de tiempo\n\n")

    texto_corrido = []
    n = 0
    for seg in segments:
        t = seg.text.strip()
        texto_corrido.append(t)
        with open(salida_md, "a", encoding="utf-8") as f:
            f.write(f"**[{hhmmss(seg.start)}]** {t}\n\n")
        n += 1
        if n % 20 == 0:
            pct = (seg.end / dur * 100) if dur else 0
            print(f"[{time.strftime('%H:%M:%S')}] {n} segmentos | ~{pct:.0f}% ({hhmmss(seg.end)}/{hhmmss(dur)})", flush=True)

    # Texto corrido (para leer/citar sin las marcas).
    with open(salida_md, "a", encoding="utf-8") as f:
        f.write("---\n\n## Texto corrido\n\n")
        f.write(" ".join(texto_corrido).strip() + "\n")

    print(f"[{time.strftime('%H:%M:%S')}] LISTO en {time.time()-t0:.0f}s -> {salida_md}", flush=True)
    return salida_md


def main():
    ap = argparse.ArgumentParser(description="Transcribe videos a Markdown (local).")
    ap.add_argument("archivo", nargs="?", help="Video específico. Si se omite, procesa los pendientes.")
    ap.add_argument("--modelo", default="medium",
                    help="tiny | base | small | medium | large-v3 (def: medium)")
    ap.add_argument("--idioma", default="es", help="Código de idioma (def: es)")
    args = ap.parse_args()

    if args.archivo:
        ruta = args.archivo if os.path.isabs(args.archivo) else os.path.join(CARPETA, args.archivo)
        objetivos = [ruta] if os.path.exists(ruta) else []
        if not objetivos:
            sys.exit(f"No existe el archivo: {ruta}")
    else:
        objetivos = videos_pendientes(CARPETA)
        if not objetivos:
            print("No hay videos pendientes (todos tienen su .md). Nada que hacer.")
            return

    print(f"Cargando modelo '{args.modelo}' (se descarga solo la 1a vez)...", flush=True)
    from faster_whisper import WhisperModel
    model = WhisperModel(args.modelo, device="cpu", compute_type="int8",
                         cpu_threads=os.cpu_count() or 4)
    print("Modelo listo.", flush=True)

    for ruta in objetivos:
        transcribir(ruta, model, args.modelo, args.idioma)
    print(f"\nTerminado. {len(objetivos)} video(s) transcrito(s).")


if __name__ == "__main__":
    main()
