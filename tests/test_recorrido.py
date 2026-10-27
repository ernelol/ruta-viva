import dataclasses

import pytest

from ruta_viva import Clima, Franja, Momento, Parada, Plaza, Recorrido, TramoAPie, TramoEnTransporte


def _recorrido_de_prueba() -> Recorrido:
    plaza = Plaza(nombre="Plaza", x=0, y=0, duracion_visita_min=15, costo=0, es_accesible=True)
    museo = Plaza(nombre="Museo (de prueba)", x=100, y=0, duracion_visita_min=45, costo=200, es_accesible=True)
    paradas = (
        Parada(lugar=plaza, tramo=TramoAPie(distancia_m=100)),
        Parada(lugar=museo, tramo=TramoEnTransporte(distancia_m=500)),
    )
    return Recorrido(momento_inicio=Momento(Franja.MANIANA, Clima.SOLEADO), paradas=paradas)


def test_metros_caminados_total_suma_solo_los_tramos_a_pie():
    recorrido = _recorrido_de_prueba()
    assert recorrido.metros_caminados_total() == 100  # el tramo en transporte no suma


def test_duracion_total_suma_tramos_y_visitas():
    recorrido = _recorrido_de_prueba()
    duracion_esperada = (round(100 / 70) + 15) + (round(500 / 300) + 45)
    assert recorrido.duracion_total_min() == duracion_esperada


def test_costo_total_suma_el_costo_de_cada_lugar():
    recorrido = _recorrido_de_prueba()
    assert recorrido.costo_total() == 200


def test_recorrido_es_inmutable():
    recorrido = _recorrido_de_prueba()
    with pytest.raises(dataclasses.FrozenInstanceError):
        recorrido.paradas = ()
