# Cómo transcribir videos (guía para futuros videos)

Este proceso convierte cualquier video en un archivo de texto **Markdown** con el mismo
nombre del video. Corre **100% en local** (en tu CPU), **sin conexión y sin gastar tokens de IA**.

Herramienta: [faster-whisper](https://github.com/SYSTRAN/faster-whisper) (transcripción por voz).

---

## Requisito (instalar una sola vez)

```powershell
py -m pip install faster-whisper
```

No hace falta instalar `ffmpeg` aparte: `faster-whisper` trae su propio decodificador.

---

## Uso

1. Copia tu video dentro de esta carpeta `videos/`.
2. Abre PowerShell en la carpeta y corre:

```powershell
cd videos
py transcribir.py
```

Eso transcribe **todos los videos que aún no tengan su `.md`** y crea, junto a cada video,
un archivo con **el mismo nombre** en formato Markdown.
Ejemplo: `1 Design thinking.mp4` → `1 Design thinking.md`.

### Opciones

- Transcribir un video específico:
  ```powershell
  py transcribir.py "1 Design thinking.mp4"
  ```
- Elegir el modelo (calidad vs. tiempo):
  ```powershell
  py transcribir.py --modelo medium
  ```
- Cambiar idioma (por defecto español):
  ```powershell
  py transcribir.py --idioma en
  ```

### Qué modelo elegir (en CPU)

| Modelo | Velocidad (para ~1 h de video) | Precisión | Cuándo usarlo |
|---|---|---|---|
| `base` | ~8-15 min | Baja | Borrador rápido |
| `small` | ~15-30 min | Media | Uso general |
| `medium` | ~45-90 min | Alta | **Recomendado** cuando el contenido importa (instrucciones, clases) |
| `large-v3` | 2-3 h o más (descarga ~3 GB) | Máxima | Solo si vas a citar textual palabra por palabra |

---

## Qué genera

Cada `.md` incluye:
- Una cabecera con el nombre del video, duración y modelo usado.
- La **transcripción con marcas de tiempo** (útil para ubicar un momento del video).
- El **texto corrido** al final (útil para leer o citar sin las marcas).

## Notas

- La carpeta `videos/` está en `.gitignore` (los videos no se versionan por su tamaño).
  Si quieres versionar una transcripción, copia el `.md` a otra carpeta del proyecto.
- El primer uso de un modelo lo descarga desde internet; los siguientes ya son offline.
