"""Armá un recorrido por Montevideo eligiendo por terminal.

Las coordenadas salen de OpenStreetMap (© OpenStreetMap contributors, licencia ODbL) y
se copiaron acá: el programa no se conecta a nada. Accesibilidad, horarios, costos y
duraciones son DATOS DE EJEMPLO inventados, no información real de esos lugares. El banco
de Sarandí es ficticio.

Correr con: .venv/bin/python3 armar_recorrido.py
"""

import math

from ruta_viva import (
    LLUVIA,
    MANIANA,
    NOCHE,
    NUBLADO,
    SOLEADO,
    TARDE,
    MinimaCaminata,
    Mirador,
    Momento,
    Museo,
    ParadaDeDescanso,
    Plaza,
    Restaurante,
    TramoAPie,
    planificar,
)

LAT_ORIGEN, LON_ORIGEN = -34.9064755, -56.1997577  # Plaza Independencia
RADIO_TIERRA_M = 6_371_000


def _a_metros(lat, lon):
    """Pasa lat/lon a metros respecto del origen. Corrige por el coseno de la latitud
    porque un grado de longitud mide menos que uno de latitud. Sirve dentro de una ciudad."""
    x = math.radians(lon - LON_ORIGEN) * math.cos(math.radians(LAT_ORIGEN)) * RADIO_TIERRA_M
    y = math.radians(lat - LAT_ORIGEN) * RADIO_TIERRA_M
    return x, y


def _lugar(clase, nombre, lat, lon, **datos):
    x, y = _a_metros(lat, lon)
    return clase(nombre=nombre, x=x, y=y, **datos)


CATALOGO_MONTEVIDEO = (
    _lugar(Plaza, "Plaza Independencia", -34.9064755, -56.1997577,
           duracion_visita_min=15, costo=0, es_accesible=True),
    _lugar(ParadaDeDescanso, "Banco de descanso, Peatonal Sarandí", -34.9065523, -56.2015658,
           duracion_visita_min=10, costo=0, es_accesible=True),
    _lugar(Museo, "Museo Torres García", -34.9064601, -56.2013757,
           duracion_visita_min=45, costo=150, es_accesible=True,
           horario_apertura=MANIANA, horario_cierre=TARDE),
    _lugar(Museo, "Museo Gurvich", -34.9074751, -56.2042950,
           duracion_visita_min=40, costo=150, es_accesible=True,
           horario_apertura=MANIANA, horario_cierre=TARDE),
    _lugar(Restaurante, "Mercado del Puerto", -34.9056495, -56.2117422,
           duracion_visita_min=60, costo=400, es_accesible=True,
           horario_apertura=MANIANA, horario_cierre=NOCHE),
    _lugar(Mirador, "Fortaleza del Cerro", -34.8883550, -56.2599252,
           duracion_visita_min=30, costo=0, es_accesible=False),
    _lugar(Plaza, "Parque Rodó", -34.9100822, -56.1697776,
           duracion_visita_min=25, costo=0, es_accesible=True),
    _lugar(Museo, "Museo Nacional de Artes Visuales", -34.9138391, -56.1649722,
           duracion_visita_min=50, costo=0, es_accesible=True,
           horario_apertura=TARDE, horario_cierre=TARDE),
    _lugar(Plaza, "Playa Pocitos", -34.9145565, -56.1477433,
           duracion_visita_min=20, costo=0, es_accesible=True),
)


def _elegir(mensaje, opciones):
    """Muestra (valor, etiqueta) numerados y devuelve el valor elegido."""
    print(mensaje)
    for numero, (_, etiqueta) in enumerate(opciones, start=1):
        print(f"  {numero}. {etiqueta}")
    while True:
        respuesta = input("Elegí un número: ").strip()
        if respuesta.isdigit() and 1 <= int(respuesta) <= len(opciones):
            return opciones[int(respuesta) - 1][0]
        print("Opción inválida, probá de nuevo.")


def _pedir_minutos():
    while True:
        respuesta = input("¿Cuántos minutos tenés disponibles? ").strip()
        if respuesta.isdigit():
            return int(respuesta)
        print("Poné un número de minutos.")


def main():
    print("=== Armar un recorrido por Montevideo ===")
    print("Coordenadas: © OpenStreetMap contributors (ODbL). El resto son datos de ejemplo.\n")

    partida = _elegir("¿Desde dónde arrancás?", [(lugar, lugar.nombre) for lugar in CATALOGO_MONTEVIDEO])
    franja = _elegir("Momento del día:", [(MANIANA, "Mañana"), (TARDE, "Tarde"), (NOCHE, "Noche")])
    clima = _elegir("Clima:", [(SOLEADO, "Soleado"), (NUBLADO, "Nublado"), (LLUVIA, "Lluvia")])
    momento = Momento(franja, clima)
    minutos = _pedir_minutos()

    catalogo = tuple(lugar for lugar in CATALOGO_MONTEVIDEO if lugar is not partida)
    recorrido = planificar(partida, momento, minutos, catalogo, MinimaCaminata())

    print(f"\nRecorrido desde {partida.nombre}:")
    if not recorrido.paradas:
        print("  (no entró ningún lugar en el tiempo disponible)")
    for numero, parada in enumerate(recorrido.paradas, start=1):
        como = "a pie" if isinstance(parada.tramo, TramoAPie) else "en transporte"
        print(f"  {numero}. {parada.lugar.nombre} ({como}, {parada.tramo.distancia_m} m)")
    print(f"\nTotal caminado: {recorrido.metros_caminados_total()} m")
    print(f"Duración total: {recorrido.duracion_total_min()} min")
    print(f"Costo total: ${recorrido.costo_total():.0f}")



if __name__ == "__main__":
    main()
