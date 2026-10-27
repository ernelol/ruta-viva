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
    armar_candidato,
    candidatos_posibles,
    elegir_mejor,
)

MOMENTO = Momento(franja=Franja.TARDE, clima=Clima.SOLEADO)


def _plaza(nombre: str, x: float, y: float, es_accesible: bool = True) -> Plaza:
    return Plaza(nombre=nombre, x=x, y=y, duracion_visita_min=15, costo=0, es_accesible=es_accesible)


def test_armar_candidato_descarta_lugares_no_accesibles():
    partida = _plaza("Partida", 0, 0)
    catalogo = (
        _plaza("Cercano accesible", 50, 0),
        _plaza("Más cercano pero no accesible", 10, 0, es_accesible=False),
    )

    recorrido = armar_candidato(partida, catalogo, MOMENTO, tiempo_disponible_min=120)

    nombres_visitados = [parada.lugar.nombre for parada in recorrido.paradas]
    assert "Cercano accesible" in nombres_visitados
    assert "Más cercano pero no accesible" not in nombres_visitados


def test_armar_candidato_respeta_el_tiempo_disponible():
    partida = _plaza("Partida", 0, 0)
    catalogo = tuple(_plaza(f"Lugar {i}", i * 200, 0) for i in range(1, 11))  # 10 lugares lejos entre sí

    recorrido = armar_candidato(partida, catalogo, MOMENTO, tiempo_disponible_min=60)

    assert recorrido.duracion_total_min() <= 60
    assert len(recorrido.paradas) < len(catalogo)  # no le alcanzó el tiempo para todos


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


def test_explorar_varios_candidatos_encuentra_menos_caminata_que_el_ingenuo():
    # A es el más cercano a la partida, así que armar_candidato (ingenuo) arranca por A
    # y después tiene que ir lejos (transporte) hasta B/C. Si en cambio se arranca por
    # B o C, el tramo largo se hace en transporte una sola vez y B-C-A queda casi todo
    # a pie — bastante menos caminata en total.
    partida = _plaza("Partida", 0, 0)
    a = _plaza("A", 300, 0)
    b = _plaza("B", 900, 0)
    c = _plaza("C", 920, 0)
    catalogo = (a, b, c)

    ingenuo = armar_candidato(partida, catalogo, MOMENTO, tiempo_disponible_min=300)

    planificador = Planificador(catalogo=catalogo, criterio=MinimaCaminata())
    mejor = planificador.planificar(partida, MOMENTO, tiempo_disponible_min=300)

    assert ingenuo.metros_caminados_total() == 320
    assert mejor.metros_caminados_total() == 20
    assert mejor.metros_caminados_total() < ingenuo.metros_caminados_total()
