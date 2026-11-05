from ruta_viva import MinimaCaminata, Plaza


def _plaza(nombre: str, x: float, y: float) -> Plaza:
    return Plaza(nombre=nombre, x=x, y=y, duracion_visita_min=15, costo=0, es_accesible=True)


def test_minima_caminata_elige_el_mas_cercano():
    actual = _plaza("Actual", 0, 0)
    cercano = _plaza("Cercano", 100, 0)
    lejano = _plaza("Lejano", 900, 0)

    siguiente = MinimaCaminata().elegir_siguiente(actual, [lejano, cercano])

    assert siguiente is cercano
