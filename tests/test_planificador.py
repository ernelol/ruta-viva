from ruta_viva import (
    Clima,
    Franja,
    MinimaCaminata,
    Momento,
    Parada,
    Plaza,
    Recorrido,
    TramoAPie,
    armar_candidato,
    elegir_mejor,
)

MOMENTO = Momento(franja=Franja.TARDE, clima=Clima.SOLEADO)


def _plaza(nombre: str, x: float, y: float, es_accesible: bool = True) -> Plaza:
    return Plaza(nombre=nombre, x=x, y=y, duracion_visita_min=20, costo=0, es_accesible=es_accesible)


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
