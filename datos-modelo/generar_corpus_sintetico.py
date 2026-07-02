"""
Generador de corpus sintético SIREC (Fase D3, paso 1).

Genera ~900 reportes ciudadanos SINTÉTICOS en español de México, variados en registro
(formal/coloquial), longitud, erratas de tecleo y colonias ficticias, distribuidos entre
las 7 categorías y 3 urgencias siguiendo la guia_etiquetado.md, con cobertura extra de
`persona_en_riesgo`.

IMPORTANTE (honestidad metodológica, exigida por el evaluador):
- Todos los registros se marcan con `origen=sintetico` y `etiquetador=generador_sintetico`.
- Este corpus se usa SOLO para entrenamiento/validación, NUNCA para el conjunto de prueba
  (ese se forma exclusivamente con reportes reales etiquetados por humanos).
- La semilla es fija (reproducible): re-ejecutar produce el mismo corpus.

Salida: corpus_sintetico.csv (columnas: texto, categoria, urgencia, etiquetador, origen).
Uso: py generar_corpus_sintetico.py
"""

import csv
import os
import random

SEMILLA = 42
OBJETIVO_POR_CATEGORIA = {
    "inundacion": 140,
    "persona_en_riesgo": 180,   # cobertura extra (clase crítica).
    "caida_poste_cable": 120,
    "deslave": 120,
    "incendio": 120,
    "dano_estructural": 120,
    "otro": 100,
}
ETIQUETADOR = "generador_sintetico"
ORIGEN = "sintetico"

# --- Pools de relleno (colonias/calles/referencias ficticias) ---
COLONIAS = [
    "Las Brisas", "El Coyol", "Lomas del Sol", "Río Medio", "La Pochota",
    "Playa Linda", "El Tejar", "San Rafael", "La Palma", "Miradores del Mar",
    "Villa Rica", "Los Pinos", "La Loma", "El Manantial", "Buenavista",
    "Colinas de Santa Fe", "El Zapote", "Las Flores", "Cocolapan", "El Palmar",
]
CALLES = [
    "Hidalgo", "Juárez", "Reforma", "Insurgentes", "5 de Mayo", "Allende",
    "Morelos", "Independencia", "16 de Septiembre", "Zaragoza", "Madero", "Xalapa",
]
REFERENCIAS = [
    "junto a la primaria", "frente al mercado", "cerca de la iglesia",
    "a un lado del OXXO", "por el puente", "en la esquina de la farmacia",
    "atrás de la secundaria", "cerca del parque", "frente a la gasolinera",
]
COLETILLAS = [
    "por favor manden ayuda", "no sé a quién más avisar", "urge apoyo",
    "les agradezco cualquier apoyo", "ojalá puedan venir pronto",
    "ya nadie sabe qué hacer", "es en serio", "manden a alguien porfa",
]

# --- Plantillas por categoría: (urgencia, plantilla) ---
# Las plantillas usan {col}=colonia, {cal}=calle, {ref}=referencia.
PLANTILLAS = {
    "inundacion": [
        ("alta", "El agua ya se metió a la casa en {col} y estamos con niños en el segundo piso"),
        ("alta", "Se está inundando la calle {cal} {ref} y hay una señora que no puede salir"),
        ("alta", "En {col} el agua nos llega al pecho y hay gente adulta mayor adentro"),
        ("alta", "La corriente en la calle {cal} está muy fuerte y arrastra cosas, hay personas cruzando"),
        ("media", "Se inundó la calle {cal} en {col}, ya no pasan los carros"),
        ("media", "Hay un encharcamiento enorme {ref}, el agua entró a los locales"),
        ("media", "El agua está subiendo en {col}, todavía no entra a las casas pero va rápido"),
        ("media", "Se desbordó el canal de {col} y la calle {cal} está bajo el agua"),
        ("baja", "Ya bajó el agua en {col} pero quedó mucho lodo en la calle {cal}"),
        ("baja", "Solo quiero avisar que {ref} sigue encharcado desde ayer"),
        ("baja", "El agua de la lluvia se acumuló tantito en la banqueta de {cal}"),
    ],
    "persona_en_riesgo": [
        ("alta", "Hay una persona atrapada en el techo de una casa en {col}, el agua sigue subiendo"),
        ("alta", "Mi vecino de {col} no puede salir, está solo y es de la tercera edad"),
        ("alta", "Un niño fue arrastrado por la corriente {ref}, ayuda por favor"),
        ("alta", "Hay gente atrapada dentro de un carro en la calle {cal}, el agua los tapó"),
        ("alta", "Se está incendiando una casa en {col} y dicen que hay alguien adentro"),
        ("alta", "Una señora se cayó {ref} y no se puede levantar, está herida"),
        ("alta", "Estamos en la azotea de una vivienda en {col}, somos cuatro y no podemos bajar"),
        ("alta", "Hay un herido {ref}, se le cayó una barda encima"),
        ("alta", "Mi abuelita está atrapada en {col}, necesita su oxígeno y se fue la luz"),
        ("alta", "Se ahoga alguien en el arroyo de {col}, vengan rápido"),
        ("media", "Hay una persona en silla de ruedas atrapada por el agua en {col}, pero está a salvo por ahora"),
        ("media", "Una familia quedó incomunicada en {col} por el agua, están bien pero no pueden salir"),
    ],
    "caida_poste_cable": [
        ("alta", "Se cayó un poste con los cables encima de la banqueta en {cal} y hay niños jugando cerca"),
        ("alta", "Hay un cable haciendo chispas {ref}, la gente pasa junto"),
        ("alta", "Un transformador explotó en {col} y los cables quedaron en la calle donde pasan carros"),
        ("alta", "Cable de luz caído y energizado en la calle {cal}, alguien lo va a tocar"),
        ("media", "Se cayó un poste de luz en {col}, en un terreno baldío, no hay nadie cerca"),
        ("media", "Hay cables colgando muy bajo en la calle {cal} {ref}"),
        ("media", "Un poste quedó chueco después del norte en {col}, se ve que se va a caer"),
        ("baja", "El poste de {cal} está un poco inclinado, quería reportarlo por si acaso"),
        ("baja", "Solo aviso que hay un cable suelto {ref}, no parece de luz"),
    ],
    "deslave": [
        ("alta", "Se está deslavando el cerro arriba de las casas en {col} y la gente sigue adentro"),
        ("alta", "Cayó un derrumbe {ref} y hay un carro con personas debajo"),
        ("alta", "Está bajando lodo y piedras hacia las viviendas de {col}, hay familias ahí"),
        ("media", "Un deslave tapó el camino a {col}, no hay paso pero nadie quedó atrapado"),
        ("media", "Se derrumbó el talud de la calle {cal}, hay tierra en toda la vía"),
        ("media", "Cayó material del cerro en {col}, bloqueó media calle"),
        ("baja", "Se deslavó un poco de tierra {ref}, nada grave pero por si quieren revisar"),
        ("baja", "Quedaron unas piedras en el camino de {col} después de la lluvia"),
    ],
    "incendio": [
        ("alta", "Se está incendiando una casa en {col}, hay mucho humo y vecinos cerca"),
        ("alta", "Un carro se prendió en fuego en la calle {cal} {ref}, hay tanque de gas al lado"),
        ("alta", "Hay un incendio en un negocio de {col} y hay gente en el edificio de arriba"),
        ("alta", "Se quema el pastizal {ref} y el fuego va hacia las casas"),
        ("media", "Hay un incendio en un pastizal en las afueras de {col}, lejos de las casas"),
        ("media", "Se está quemando basura acumulada {ref}, sale bastante humo"),
        ("media", "Fuego en un lote baldío en la calle {cal}, no hay viviendas cerca"),
        ("baja", "Hubo un conato de incendio {ref} pero los vecinos ya lo apagaron"),
        ("baja", "Solo aviso que huele a quemado por {col}, no veo llamas"),
    ],
    "dano_estructural": [
        ("alta", "Se colapsó el techo de una casa en {col} y creemos que hay alguien debajo"),
        ("alta", "Una barda se está cayendo {ref} justo donde pasan los niños de la escuela"),
        ("alta", "El muro de una vivienda en {col} se botó y hay personas adentro"),
        ("media", "Hay una grieta grande en el muro de una casa en {col}, se está abriendo más"),
        ("media", "Se cayó una barda por el aire en la calle {cal}, bloquea el paso"),
        ("media", "El techo de la bodega {ref} se dañó con la lluvia y gotea feo"),
        ("baja", "Salió una grieta chica en la barda del patio en {col}, quería reportarla"),
        ("baja", "Se desprendió un pedazo de aplanado {ref}, cosa menor"),
    ],
    "otro": [
        ("media", "¿A dónde puedo llevar a mi familia? Se nos metió el agua en {col}"),
        ("media", "Necesitamos despensas y cobijas en {col}, quedamos varios sin nada"),
        ("media", "Se fue la luz en toda la colonia {col} desde hace horas"),
        ("media", "¿Van a abrir algún albergue por la zona de {cal}?"),
        ("baja", "Solo quiero saber a qué hora reabren las oficinas de protección civil"),
        ("baja", "Hay mucha basura acumulada {ref} por la lluvia de ayer"),
        ("baja", "Quería agradecer a los rescatistas que vinieron a {col}"),
        ("baja", "¿Dónde reporto un bache que salió en la calle {cal}?"),
    ],
}


def rellenar(plantilla, rnd):
    """Sustituye los marcadores de la plantilla con valores aleatorios."""
    return plantilla.format(
        col=rnd.choice(COLONIAS),
        cal=rnd.choice(CALLES),
        ref=rnd.choice(REFERENCIAS),
    )


def variar_registro(texto, rnd):
    """Aplica variación de longitud/registro: a veces agrega una coletilla coloquial."""
    if rnd.random() < 0.30:
        texto = texto + ", " + rnd.choice(COLETILLAS)
    if rnd.random() < 0.15:
        texto = texto.lower()  # registro descuidado, sin mayúscula inicial.
    return texto


def meter_erratas(texto, rnd):
    """Introduce erratas de tecleo plausibles en una fracción de los textos."""
    if rnd.random() < 0.25:
        # Quitar acentos (muy común al teclear rápido).
        tabla = str.maketrans("áéíóúÁÉÍÓÚ", "aeiouAEIOU")
        texto = texto.translate(tabla)
    if rnd.random() < 0.12:
        # Duplicar una letra al azar.
        i = rnd.randrange(len(texto))
        texto = texto[:i] + texto[i] + texto[i:]
    if rnd.random() < 0.10:
        # Omitir una letra al azar.
        i = rnd.randrange(len(texto))
        texto = texto[:i] + texto[i + 1:]
    return texto


def generar():
    rnd = random.Random(SEMILLA)
    filas = []
    vistos = set()

    for categoria, objetivo in OBJETIVO_POR_CATEGORIA.items():
        plantillas = PLANTILLAS[categoria]
        intentos = 0
        generados = 0
        while generados < objetivo and intentos < objetivo * 50:
            intentos += 1
            urgencia, plantilla = rnd.choice(plantillas)
            texto = rellenar(plantilla, rnd)
            texto = variar_registro(texto, rnd)
            texto = meter_erratas(texto, rnd)
            clave = texto.lower().strip()
            if clave in vistos:
                continue  # evitar duplicados exactos.
            vistos.add(clave)
            filas.append({
                "texto": texto,
                "categoria": categoria,
                "urgencia": urgencia,
                "etiquetador": ETIQUETADOR,
                "origen": ORIGEN,
            })
            generados += 1

    rnd.shuffle(filas)
    return filas


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    salida = os.path.join(base, "corpus_sintetico.csv")
    filas = generar()

    with open(salida, "w", encoding="utf-8", newline="") as f:
        escritor = csv.DictWriter(f, fieldnames=["texto", "categoria", "urgencia", "etiquetador", "origen"])
        escritor.writeheader()
        escritor.writerows(filas)

    # Resumen de distribución (para verificación y para reporte_corpus.md).
    print(f"Generados {len(filas)} reportes sintéticos -> {salida}")
    por_cat = {}
    por_urg = {}
    for r in filas:
        por_cat[r["categoria"]] = por_cat.get(r["categoria"], 0) + 1
        por_urg[r["urgencia"]] = por_urg.get(r["urgencia"], 0) + 1
    print("\nPor categoría:")
    for c, n in sorted(por_cat.items(), key=lambda x: -x[1]):
        print(f"  {c:20s} {n}")
    print("\nPor urgencia:")
    for u, n in sorted(por_urg.items(), key=lambda x: -x[1]):
        print(f"  {u:20s} {n}")


if __name__ == "__main__":
    main()
