# Cómo se construye «Entrega 2 Final.docx»

El documento **no se edita a mano**: se genera desde estos módulos. La fuente de
verdad son los archivos `.py` de esta carpeta, nunca el `.docx`.

```bash
cd /home/ubuntu/proyectos/sirec/entregas

# 1. figuras (solo si se tocan)
.venv-docs/bin/python build/generar_figuras.py

# 2. documento
.venv-docs/bin/python build/construir.py          # -> Entrega 2 Final.docx

# 3. control de calidad
.venv-docs/bin/python build/auditar.py "Entrega 2 Final.docx"

# 4. PDF de vista previa y conteo real de páginas
soffice --headless --convert-to pdf "Entrega 2 Final.docx"
```

## Archivos

| Archivo | Qué hace |
|---|---|
| `doc_builder.py` | Envoltura de `python-docx` sobre `plantilla.docx`: portada, encabezado, índice como campo TOC, numeración jerárquica, rótulos de tablas y figuras |
| `construir.py` | Orquesta: portada + módulos de contenido en orden y guarda el `.docx` |
| `cap1_introduccion.py` … `anexo_b.py` | Un módulo por capítulo o apartado; cada uno expone `escribir(d)` |
| `referencias.py` | Las 29 entradas APA en una lista |
| `generar_figuras.py` | Genera las 3 figuras con matplotlib en `figuras/` |
| `auditar.py` | Verifica extensión, rótulos, párrafos largos, títulos consecutivos y el circuito citas ↔ referencias |

## Reglas que respeta el generador

- **No se tocan los estilos de la plantilla** (márgenes, interlineado, tipografía).
  Todo se escribe con los estilos nombrados: `Heading 1/2/3`, `Normal`,
  `Referencias bibliográficas`, `Anexo`, `Pie de foto-tabla`, `Figuras`.
- **Los títulos se escriben sin número**: la numeración (1., 1.1, 1.1.1) la aplica
  el estilo. Escribir «1. Introducción» produciría «1. 1. Introducción».
- **Rótulo arriba, fuente abajo** en tablas y figuras, con «Tabla N.» en negrita y
  el nombre en cursiva, según el apartado 1.3 de `instrucciones.pdf`.
- **La portada solo lleva lo de la plantilla**: título, integrantes y fecha.
  Cualquier párrafo extra desplaza la tabla y parte la portada en dos páginas.
- **Extensión**: 20–30 páginas sin contar portada, índices ni anexos. El material
  tabulado que no es imprescindible en el cuerpo vive en los anexos A y B.

## Lo que hay que hacer en Word antes de entregar

1. Abrir el `.docx` y **actualizar el índice** (clic derecho › Actualizar campos, o F9).
   El documento trae `updateFields`, así que Word suele ofrecerlo al abrir.
2. Revisar el conteo de páginas del desarrollo: debe quedar entre 20 y 30
   (con LibreOffice son 30; Word puede variar en ±1).
3. Exportar a PDF para el depósito final (las entregas intermedias van en Word).
