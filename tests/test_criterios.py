from ruta_viva import Clima, Franja, MinimaCaminata, Momento, Parada, Plaza, Recorrido, TramoAPie


def _recorrido_con(metros: int) -> Recorrido:
    plaza = Plaza(nombre="Plaza", x=0, y=0, duracion_visita_min=15, costo=0, es_accesible=True)
    paradas = (Parada(lugar=plaza, tramo=TramoAPie(distancia_m=metros)),)
    return Recorrido(momento_inicio=Momento(Franja.MANIANA, Clima.SOLEADO), paradas=paradas)


def test_minima_caminata_prefiere_menos_metros():
    criterio = MinimaCaminata()
    corto = _recorrido_con(100)
    largo = _recorrido_con(900)

    assert criterio.puntuar(corto) > criterio.puntuar(largo)
