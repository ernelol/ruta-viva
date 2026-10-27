"""Ejemplo de punta a punta: arma un catálogo de lugares (inventado, no son coordenadas
GPS reales) y planifica un recorrido para alguien con movilidad reducida.

Correr con: .venv/bin/python3 ejemplo.py
"""

from ruta_viva import (
    Clima,
    Franja,
    MinimaCaminata,
    Mirador,
    Momento,
    Museo,
    ParadaDeDescanso,
    Plaza,
    Planificador,
    Restaurante,
)

CATALOGO = (
    Museo(
        nombre="Museo del Carnaval", x=100, y=50, duracion_visita_min=45, costo=150,
        es_accesible=True, horario_apertura=Franja.MANIANA, horario_cierre=Franja.TARDE,
    ),
    Plaza(
        nombre="Plaza Independencia", x=300, y=80, duracion_visita_min=20, costo=0,
        es_accesible=True,
    ),
    Restaurante(
        nombre="Mercado del Puerto", x=150, y=600, duracion_visita_min=60, costo=400,
        es_accesible=True, horario_apertura=Franja.MANIANA, horario_cierre=Franja.NOCHE,
    ),
    Mirador(
        nombre="Mirador del Cerro", x=4000, y=3500, duracion_visita_min=25, costo=0,
        es_accesible=False,  # tiene una escalinata sin rampa — queda afuera del recorrido
    ),
    ParadaDeDescanso(
        nombre="Banco accesible, Peatonal Sarandí", x=250, y=60, duracion_visita_min=10,
        costo=0, es_accesible=True,
    ),
)

PARTIDA = Plaza(nombre="Hotel (punto de partida)", x=0, y=0, duracion_visita_min=0, costo=0, es_accesible=True)


def main() -> None:
    planificador = Planificador(catalogo=CATALOGO, criterio=MinimaCaminata())
    momento = Momento(franja=Franja.MANIANA, clima=Clima.SOLEADO)

    recorrido = planificador.planificar(PARTIDA, momento, tiempo_disponible_min=180)

    print(f"Recorrido para {momento.franja.name.lower()}, clima {momento.clima.name.lower()}:")
    for i, parada in enumerate(recorrido.paradas, start=1):
        tipo_tramo = type(parada.tramo).__name__
        print(f"  {i}. {parada.lugar.nombre} — llegada por {tipo_tramo}, {parada.tramo.metros_caminados()}m caminados")
    print()
    print(f"Total caminado: {recorrido.metros_caminados_total()} m")
    print(f"Duración total: {recorrido.duracion_total_min()} min")
    print(f"Costo total: ${recorrido.costo_total():.0f}")
    print()
    print("(Mirador del Cerro quedó afuera — no es accesible, se filtra antes de puntuar.)")


if __name__ == "__main__":
    main()
