import inspect

from ruta_viva import (
    Clima,
    Franja,
    MinimaCaminata,
    Momento,
    Parada,
    Plaza,
    Planificador,
    Recorrido,
    TramoAPie,
    candidatos_posibles,
    elegir_mejor,
)

MOMENTO = Momento(franja=Franja.TARDE, clima=Clima.SOLEADO)


def _plaza(nombre: str, x: float, y: float, es_accesible: bool = True) -> Plaza:
    return Plaza(nombre=nombre, x=x, y=y, duracion_visita_min=15, costo=0, es_accesible=es_accesible)


def test_candidatos_descartan_lugares_no_accesibles():
    partida = _plaza("Partida", 0, 0)
    catalogo = (
        _plaza("Cercano accesible", 50, 0),
        _plaza("Más cercano pero no accesible", 10, 0, es_accesible=False),
    )

    candidato = next(candidatos_posibles(partida, catalogo, MOMENTO, tiempo_disponible_min=120))

    nombres_visitados = [parada.lugar.nombre for parada in candidato.paradas]
    assert "Cercano accesible" in nombres_visitados
    assert "Más cercano pero no accesible" not in nombres_visitados


def test_candidatos_respetan_el_tiempo_disponible():
    partida = _plaza("Partida", 0, 0)
    catalogo = tuple(_plaza(f"Lugar {i}", i * 200, 0) for i in range(1, 11))  # 10 lugares lejos entre sí

    candidato = next(candidatos_posibles(partida, catalogo, MOMENTO, tiempo_disponible_min=60))

    assert candidato.duracion_total_min() <= 60
    assert len(candidato.paradas) < len(catalogo)  # no le alcanzó el tiempo para todos


def test_elegir_mejor_usa_el_criterio_para_decidir():
    corto = Recorrido(MOMENTO, (Parada(_plaza("A", 0, 0), TramoAPie(distancia_m=50)),))
    largo = Recorrido(MOMENTO, (Parada(_plaza("B", 0, 0), TramoAPie(distancia_m=800)),))

    mejor = elegir_mejor([largo, corto], MinimaCaminata())

    assert mejor is corto


def test_candidatos_posibles_es_un_generador():
    partida = _plaza("Partida", 0, 0)
    catalogo = (_plaza("A", 300, 0),)

    generador = candidatos_posibles(partida, catalogo, MOMENTO, tiempo_disponible_min=100)

    assert inspect.isgenerator(generador)


def test_planificador_elige_el_candidato_que_menos_camina():
    # Empezar por A o por B/C da resultados bien distintos: si empezás por A, el tramo
    # largo hasta B queda a mitad de camino y se camina de más; si empezás por B o C,
    # el tramo largo se hace una sola vez en transporte y el resto queda cerca y a pie.
    partida = _plaza("Partida", 0, 0)
    a = _plaza("A", 300, 0)
    b = _plaza("B", 900, 0)
    c = _plaza("C", 920, 0)
    catalogo = (a, b, c)

    candidatos = list(candidatos_posibles(partida, catalogo, MOMENTO, tiempo_disponible_min=300))
    caminatas = [candidato.metros_caminados_total() for candidato in candidatos]

    planificador = Planificador(catalogo=catalogo, criterio=MinimaCaminata())
    mejor = planificador.planificar(partida, MOMENTO, tiempo_disponible_min=300)

    assert len(candidatos) == 3  # uno por cada posible primer lugar
    assert max(caminatas) > min(caminatas)  # de verdad no da lo mismo por dónde arrancar
    assert mejor.metros_caminados_total() == min(caminatas)
