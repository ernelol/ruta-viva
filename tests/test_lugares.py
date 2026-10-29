import dataclasses

import pytest

from ruta_viva import Clima, Franja, Lugar, Mirador, Momento, Museo, ParadaDeDescanso, Plaza, Restaurante


def test_lugar_no_se_puede_instanciar_directo():
    with pytest.raises(TypeError):
        Lugar(nombre="x", x=0, y=0, duracion_visita_min=0, costo=0, es_accesible=True)


def test_mirador_no_disponible_con_lluvia():
    mirador = Mirador(nombre="Cerro", x=0, y=0, duracion_visita_min=30, costo=0, es_accesible=True)
    con_lluvia = Momento(franja=Franja.TARDE, clima=Clima.LLUVIA)
    sin_lluvia = Momento(franja=Franja.TARDE, clima=Clima.SOLEADO)

    assert mirador.esta_disponible(con_lluvia) is False
    assert mirador.esta_disponible(sin_lluvia) is True


def test_museo_disponible_solo_en_su_horario():
    museo = Museo(
        nombre="Museo X", x=0, y=0, duracion_visita_min=60, costo=100, es_accesible=True,
        horario_apertura=Franja.MANIANA, horario_cierre=Franja.TARDE,
    )
    assert museo.esta_disponible(Momento(Franja.TARDE, Clima.SOLEADO)) is True
    assert museo.esta_disponible(Momento(Franja.NOCHE, Clima.SOLEADO)) is False


def test_plaza_y_parada_de_descanso_siempre_disponibles():
    plaza = Plaza(nombre="Plaza", x=0, y=0, duracion_visita_min=15, costo=0, es_accesible=True)
    descanso = ParadaDeDescanso(nombre="Banco", x=0, y=0, duracion_visita_min=5, costo=0, es_accesible=True)
    for momento in (
        Momento(Franja.MANIANA, Clima.LLUVIA),
        Momento(Franja.NOCHE, Clima.SOLEADO),
    ):
        assert plaza.esta_disponible(momento) is True
        assert descanso.esta_disponible(momento) is True


def test_restaurante_disponible_solo_en_su_horario():
    restaurante = Restaurante(
        nombre="Mercado del Puerto", x=0, y=0, duracion_visita_min=60, costo=400, es_accesible=True,
        horario_apertura=Franja.MANIANA, horario_cierre=Franja.NOCHE,
    )
    assert restaurante.esta_disponible(Momento(Franja.NOCHE, Clima.SOLEADO)) is True


def test_lugar_es_inmutable():
    plaza = Plaza(nombre="Plaza", x=0, y=0, duracion_visita_min=15, costo=0, es_accesible=True)
    with pytest.raises(dataclasses.FrozenInstanceError):
        plaza.costo = 999


def test_momento_es_inmutable():
    momento = Momento(franja=Franja.MANIANA, clima=Clima.SOLEADO)
    with pytest.raises(dataclasses.FrozenInstanceError):
        momento.clima = Clima.LLUVIA
