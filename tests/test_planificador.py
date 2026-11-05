from ruta_viva import Clima, Franja, MinimaCaminata, Momento, Plaza, Planificador

MOMENTO = Momento(franja=Franja.TARDE, clima=Clima.SOLEADO)


def _plaza(nombre: str, x: float, y: float, es_accesible: bool = True) -> Plaza:
    return Plaza(nombre=nombre, x=x, y=y, duracion_visita_min=15, costo=0, es_accesible=es_accesible)


def test_descarta_lugares_no_accesibles():
    partida = _plaza("Partida", 0, 0)
    catalogo = (
        _plaza("Cercano accesible", 50, 0),
        _plaza("Más cercano pero no accesible", 10, 0, es_accesible=False),
    )
    planificador = Planificador(catalogo=catalogo, criterio=MinimaCaminata())

    recorrido = planificador.planificar(partida, MOMENTO, tiempo_disponible_min=120)

    nombres_visitados = [parada.lugar.nombre for parada in recorrido.paradas]
    assert "Cercano accesible" in nombres_visitados
    assert "Más cercano pero no accesible" not in nombres_visitados


def test_respeta_el_tiempo_disponible():
    partida = _plaza("Partida", 0, 0)
    catalogo = tuple(_plaza(f"Lugar {i}", i * 200, 0) for i in range(1, 11))  # 10 lugares lejos entre sí
    planificador = Planificador(catalogo=catalogo, criterio=MinimaCaminata())

    recorrido = planificador.planificar(partida, MOMENTO, tiempo_disponible_min=60)

    assert recorrido.duracion_total_min() <= 60
    assert len(recorrido.paradas) < len(catalogo)  # no le alcanzó el tiempo para todos


def test_visita_siempre_el_mas_cercano_disponible():
    partida = _plaza("Partida", 0, 0)
    cerca = _plaza("Cerca", 100, 0)
    lejos = _plaza("Lejos", 900, 0)
    catalogo = (lejos, cerca)  # a propósito en el orden "equivocado"
    planificador = Planificador(catalogo=catalogo, criterio=MinimaCaminata())

    recorrido = planificador.planificar(partida, MOMENTO, tiempo_disponible_min=300)

    nombres_en_orden = [parada.lugar.nombre for parada in recorrido.paradas]
    assert nombres_en_orden == ["Cerca", "Lejos"]
