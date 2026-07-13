# Guía de etiquetado — SIREC

> Documento operativo para las personas que etiquetan el corpus de reportes ciudadanos.
> Define **cómo asignar categoría y urgencia** de forma consistente entre anotadores.
> Es requisito del evaluador (procedimiento de etiquetado + criterio de urgencia explícito).
>
> **[HUMANO] El equipo debe leer y aprobar esta guía (o pedir ajustes) antes de la Fase D3.**

---

## 1. Qué se etiqueta

Cada reporte recibe **dos etiquetas independientes**:

1. **Categoría temática** — una de 7 (de qué trata el reporte).
2. **Nivel de urgencia** — uno de 3 (qué tan rápido debe atenderse).

Se etiqueta **lo que dice el texto**, no lo que el anotador imagina. Si el texto no da
información suficiente para una categoría específica, se usa `otro`. Ante la duda de
urgencia, se prioriza la seguridad de las personas (ver sección 3).

---

## 2. Categorías (definición operativa + 3 ejemplos)

### 2.1 `inundacion` — Inundación
Entrada o acumulación de agua que afecta viviendas, calles o negocios: desbordamientos,
encharcamientos graves, agua que sube dentro de inmuebles.
- "Se metió el agua a la casa, ya nos llega a las rodillas."
- "La calle Reforma está totalmente inundada, no pasan los carros."
- "El río se desbordó y el agua entró a los locales del mercado."

### 2.2 `persona_en_riesgo` — Persona en riesgo
Hay una o más personas cuya vida o integridad está en peligro **inmediato**: atrapadas,
arrastradas, heridas de gravedad, incomunicadas por el agua, en riesgo de ahogarse.
- "Hay una señora atrapada en el techo, el agua sigue subiendo."
- "Un niño fue arrastrado por la corriente en el arroyo."
- "Mi abuelo está adentro y no puede salir, necesita oxígeno."

### 2.3 `caida_poste_cable` — Caída de poste o cable
Postes de luz derribados o inclinados, cables eléctricos caídos o colgando, transformadores
dañados o haciendo chispas. Riesgo eléctrico.
- "Se cayó un poste de luz y los cables están sobre la banqueta."
- "Hay un cable chispeando en plena avenida."
- "El poste está a punto de caer sobre los coches estacionados."

### 2.4 `deslave` — Deslave
Deslizamiento de tierra, lodo o rocas desde cerros, laderas o taludes; derrumbes de
material que bloquean caminos o amenazan viviendas.
- "Se vino un deslave en el cerro y tapó el camino a la comunidad."
- "Está cayendo lodo y piedras sobre las casas de la parte alta."
- "El talud de la carretera se derrumbó, hay tierra en toda la vía."

### 2.5 `incendio` — Incendio
Fuego activo en viviendas, negocios, vehículos, pastizales o basura; presencia de llamas
o humo que indica combustión en curso.
- "Se está incendiando la casa de junto, hay mucho humo."
- "Un carro se prendió en fuego en el estacionamiento."
- "Hay un incendio en el pastizal detrás de la escuela."

### 2.6 `dano_estructural` — Daño estructural
Daños en construcciones sin fuego ni deslave: grietas, muros o bardas caídas o a punto de
caer, techos colapsados, edificios debilitados por la lluvia o el viento.
- "Se cayó una barda por el aire y bloquea la entrada."
- "Hay una grieta enorme en el muro de la casa, se está abriendo."
- "El techo de la bodega se colapsó con la lluvia."

### 2.7 `otro` — Otro
Reportes que no encajan claramente en las 6 anteriores, o cuya información es insuficiente
para clasificarlos. Incluye solicitudes de información, quejas generales y avisos vagos.
- "¿A qué hora reabren el albergue?"
- "Se fue la luz en toda la colonia." (sin poste/cable caído reportado)
- "Hay basura acumulada por la lluvia."

**Regla de desempate entre categorías:** si un reporte menciona a una persona en peligro
inmediato *además* de otra situación (inundación, incendio, deslave…), la categoría es
**`persona_en_riesgo`**, porque es lo que define la respuesta prioritaria. Ejemplo:
"se incendia la casa y hay alguien adentro" → `persona_en_riesgo` (no `incendio`).

---

## 3. Criterio de urgencia (explícito)

La urgencia mide **qué tan rápido debe atenderse**, no la categoría. Se decide por las
**señales textuales** presentes en el reporte.

### 3.1 `alta` — Vidas en riesgo o peligro inmediato
Se asigna cuando el texto indica (explícita o razonablemente):
- Personas **atrapadas, heridas, arrastradas, incomunicadas o en riesgo de ahogarse**.
- **Fuego activo con personas cerca** o en viviendas habitadas.
- **Cables energizados caídos en vía transitada** o contacto eléctrico posible con personas.
- **Deslave o colapso en curso sobre viviendas habitadas**.
- Menciones de **población vulnerable** en peligro (niños, ancianos, personas enfermas o con discapacidad).

Ejemplos: "hay gente atrapada", "el agua ya cubrió el primer piso y estamos arriba",
"cable haciendo chispas donde pasan los niños".

### 3.2 `media` — Daño material en curso, sin personas afectadas todavía
Se asigna cuando hay un problema real y en desarrollo, pero **no hay indicios de personas
en peligro inmediato**:
- Daño a bienes (inundación de calle o local sin gente atrapada, poste caído sin contacto).
- Riesgo **potencial** que aún no afecta a personas.

Ejemplos: "la calle está inundada y no puedo sacar el carro", "se cayó un poste en un
terreno baldío", "hay una grieta en la barda del patio".

### 3.3 `baja` — Situación controlada, informativa o daño menor
Se asigna cuando:
- La situación ya **pasó o está controlada**.
- El reporte es **informativo, una consulta o una queja** sin riesgo.
- El daño es **menor** y no escala.

Ejemplos: "ya bajó el agua pero quedó lodo", "¿dónde puedo llevar despensa?",
"se cayeron unas ramas por el viento".

### 3.4 Principio rector (para el modelo y los anotadores)
En emergencias, **un falso negativo de urgencia alta es más grave** que sobrestimar.
Ante duda razonable entre `alta` y `media`, y si hay cualquier señal de personas
potencialmente expuestas, se etiqueta **`alta`**. Esta preferencia se traslada luego al
modelo priorizando el **recall** de las clases críticas (`persona_en_riesgo`, `urgencia=alta`).

---

## 4. Casos de frontera resueltos (mínimo 5)

Estos casos fijan criterio común. Los anotadores deben resolver casos parecidos igual.

**Caso 1 — Inundación junto a escuela en horario de clases.**
"Se está inundando la calle frente a la primaria y son las 10 am."
→ Categoría `inundacion`; **urgencia `alta`**. Justificación: aunque no se menciona una
persona atrapada, hay exposición previsible de menores (población vulnerable) en un entorno
con agua creciente. El principio rector (3.4) inclina a `alta`.

**Caso 2 — Incendio con persona adentro.**
"Se quema la casa de la esquina y dicen que hay alguien adentro."
→ Categoría **`persona_en_riesgo`** (no `incendio`, por la regla de desempate 2.7);
urgencia `alta`.

**Caso 3 — Poste caído sin contacto con personas.**
"Un poste se cayó en la madrugada en la calle cerrada, no hay nadie cerca."
→ Categoría `caida_poste_cable`; **urgencia `media`**. Justificación: hay riesgo eléctrico
y daño, pero el texto indica ausencia de personas expuestas y vía cerrada. No hay señal de
peligro inmediato a personas.

**Caso 4 — Situación ya resuelta.**
"Hubo un conato de incendio en el basurero pero los vecinos ya lo apagaron."
→ Categoría `incendio` (es de lo que trata); **urgencia `baja`**. Justificación: el texto
indica que ya está controlado.

**Caso 5 — Reporte vago / insuficiente.**
"Está feo esto, manden ayuda."
→ Categoría **`otro`** (no hay información para una categoría específica); urgencia `media`
por precaución (hay una solicitud de ayuda pero sin señales concretas de vidas en riesgo).
Si el reporte incluyera "hay heridos", pasaría a `persona_en_riesgo`/`alta`.

**Caso 6 — Deslave que amenaza casas habitadas.**
"Se está deslavando el cerro arriba de las casas y la gente sigue adentro."
→ Categoría `deslave`; **urgencia `alta`**. Justificación: deslave en curso sobre viviendas
habitadas (señal de 3.1).

**Caso 7 — Grieta reportada como informe, sin riesgo inmediato.**
"Quiero avisar que salió una grieta chica en la barda del patio."
→ Categoría `dano_estructural`; **urgencia `baja`**. Daño menor, sin escalamiento ni personas
expuestas.

---

## 5. Columnas del corpus etiquetado

La herramienta de etiquetado (Fase D2) guarda cada reporte con estas columnas:

| Columna | Contenido |
|---|---|
| `texto` | Reporte (anonimizado si es real) |
| `categoria` | Una de las 7 |
| `urgencia` | `alta` / `media` / `baja` |
| `etiquetador` | Identificador de quien etiquetó (para el doble etiquetado / kappa) |
| `origen` | `real`, `redactado` o `sintetico` (trazabilidad exigida por el evaluador) |

**Reglas de origen:**
- `real`: reporte recolectado de fuentes reales (redes, prensa, transcripciones), anonimizado.
- `redactado`: basado en un hecho real pero reescrito por el equipo.
- `sintetico`: generado con IA (declarado explícitamente; nunca se usa para el conjunto de prueba).

El **conjunto de prueba se forma exclusivamente con reportes `origen=real`** (regla innegociable).

---

## 6. Aprobación del equipo

- Revisada y **aprobada por: Alexis Herrera — 2026-07-13**.
- Ajustes pedidos: ninguno.
- Con esta aprobación queda cerrada la **Tarea 1 (D1)**. Ricardo y Nahum usan esta versión
  como criterio para el etiquetado y el doble etiquetado del kappa (D3.4).
