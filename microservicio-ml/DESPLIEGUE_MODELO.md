# Cómo desplegar los modelos BETO (no van en el repo)

Los dos modelos BETO fine-tuned (`beto_categoria/` y `beto_urgencia/`) pesan ~440 MB
cada archivo de pesos, por lo que **no se versionan en Git** (GitHub rechaza archivos
> 100 MB). El repo trae **todo lo necesario para obtenerlos y servirlos**; los pesos se
llevan aparte. Este documento explica cómo, tanto en local como en la EC2 de AWS.

## Qué SÍ está en el repo

- `entrenar_beto_colab.ipynb` / `entrenar_beto.py`: para (re)generar los modelos.
- `clasificador_modelo.py`: carga los modelos y sirve la inferencia (contrato 1.3).
- `requirements.txt`: incluye `torch` y `transformers` (modo modelo).
- El corpus y el conjunto gold para reproducir el entrenamiento.

## Obtener los modelos (una de dos)

**Opción A — reutilizar los ya entrenados (rápido):** toma el `beto_modelos.zip` que se
descargó de Colab.

**Opción B — reentrenar (reproducible):** corre `entrenar_beto_colab.ipynb` en Colab con
GPU (o `py entrenar_beto.py --tarea categoria --gold-test --con-sintetico` con GPU local).

## Instalar en LOCAL

```powershell
cd microservicio-ml
mkdir modelos
# extrae beto_modelos.zip dentro de modelos/  ->  modelos/beto_categoria y modelos/beto_urgencia
py -m pip install torch transformers
$env:SIREC_MODO = "modelo"
py -m uvicorn main:app --port 8000
```

Estructura esperada:
```
microservicio-ml/modelos/beto_categoria/   (config.json, model.safetensors, tokenizer...)
microservicio-ml/modelos/beto_urgencia/
```

## Instalar en la EC2 de AWS

El zip **no está en GitHub**, así que se copia a la instancia por SCP (Route 53/EC2, sin S3):

```bash
# desde tu máquina: subir el zip a la EC2
scp -i tu_llave.pem beto_modelos.zip ec2-user@TU_IP_ELASTICA:/opt/sirec/microservicio-ml/

# en la EC2:
cd /opt/sirec/microservicio-ml
unzip beto_modelos.zip -d modelos/
python3 -m pip install -r requirements.txt      # incluye torch + transformers
# el microservicio corre bajo systemd con SIREC_MODO=modelo (solo localhost:8000)
```

> Nota: `torch` en CPU es suficiente para la inferencia de un reporte a la vez (la EC2
> t3.small/medium no tiene GPU). La primera carga baja el tokenizer/config; los pesos ya
> están en `modelos/`. Ruta configurable con la variable `SIREC_MODELO_DIR`.

## Verificación

```bash
curl -X POST http://localhost:8000/clasificar -H "Content-Type: application/json" \
  -d '{"texto":"Hay una persona atrapada en el techo, el agua sigue subiendo"}'
# -> categoria=persona_en_riesgo, urgencia=alta, con confianzas reales (no 0.9 fijo)
curl http://localhost:8000/salud   # -> {"estado":"ok","modo":"modelo"}
```
