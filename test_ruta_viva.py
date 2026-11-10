import dataclasses

import pytest

from ruta_viva import (
    LLUVIA, MANIANA, NOCHE, SOLEADO, TARDE,
    CriterioDeCalidad, Lugar, MinimaCaminata, Mirador, Momento, Museo, ParadaDeDescanso, Plaza,
    Recorrido, Restaurante, TramoAPie, TramoEnTransporte, TramoRuta,
    lugares_visitables, mejor_recorrido, planificar, tramo_entre,
)

MOMENTO = Momento(TARDE, SOLEADO)


def plaza(nombre, x, visita=15, accesible=True):
    return Plaza(nombre=nombre, x=x, y=0, duracion_visita_min=visita, costo=0, es_accesible=accesible)


def nombres(recorrido):
    return [parada.lugar.nombre for parada in recorrido.paradas]


def planificar_simple(catalogo, minutos):
    return planificar(plaza("Partida", 0), MOMENTO, minutos, catalogo, MinimaCaminata())


# ---------- Abstracción ----------

def test_las_clases_abstractas_no_se_pueden_crear():
    with pytest.raises(TypeError):
        Lugar(nombre="x", x=0, y=0, duracion_visita_min=0, costo=0, es_accesible=True)
    with pytest.raises(TypeError):
        TramoRuta()
    with pytest.raises(TypeError):
        CriterioDeCalidad()


# ---------- Cada tipo de lugar decide su disponibilidad ----------

def test_mirador_no_disponible_con_lluvia():
    mirador = Mirador(nombre="Cerro", x=0, y=0, duracion_visita_min=30, costo=0, es_accesible=True)
    assert mirador.esta_disponible(Momento(TARDE, LLUVIA)) is False
    assert mirador.esta_disponible(Momento(TARDE, SOLEADO)) is True


def test_museo_y_restaurante_respetan_su_horario():
    museo = Museo(nombre="M", x=0, y=0, duracion_visita_min=60, costo=100, es_accesible=True,
                  horario_apertura=MANIANA, horario_cierre=TARDE)
    restaurante = Restaurante(nombre="R", x=0, y=0, duracion_visita_min=60, costo=400, es_accesible=True,
                              horario_apertura=TARDE, horario_cierre=NOCHE)
    assert museo.esta_disponible(Momento(TARDE, SOLEADO)) is True
    assert museo.esta_disponible(Momento(NOCHE, SOLEADO)) is False
    assert restaurante.esta_disponible(Momento(NOCHE, SOLEADO)) is True
    assert restaurante.esta_disponible(Momento(MANIANA, SOLEADO)) is False


def test_plaza_y_parada_de_descanso_siempre_disponibles():
    descanso = ParadaDeDescanso(nombre="Banco", x=0, y=0, duracion_visita_min=5, costo=0, es_accesible=True)
    for momento in (Momento(MANIANA, LLUVIA), Momento(NOCHE, SOLEADO)):
        assert plaza("P", 0).esta_disponible(momento) is True
        assert descanso.esta_disponible(momento) is True


# ---------- Invariantes e inmutabilidad ----------

def test_rechaza_datos_invalidos():
    with pytest.raises(ValueError):
        plaza("x", 0, visita=-1)
    with pytest.raises(ValueError):
        Momento("MEDIANOCHE", SOLEADO)
    with pytest.raises(ValueError):
        Momento(TARDE, "GRANIZO")
    with pytest.raises(ValueError):
        planificar_simple((), -1)
    with pytest.raises(ValueError):
        Museo("M", 0, 0, 30, 0, True, horario_apertura="ALMUERZO", horario_cierre=TARDE)
    with pytest.raises(ValueError):
        Museo("M", 0, 0, 30, 0, True, horario_apertura=NOCHE, horario_cierre=MANIANA)


def test_los_objetos_son_inmutables():
    with pytest.raises(dataclasses.FrozenInstanceError):
        plaza("P", 0).costo = 999
    with pytest.raises(dataclasses.FrozenInstanceError):
        plaza("P", 0).otro_atributo = 1
    with pytest.raises(dataclasses.FrozenInstanceError):
        MOMENTO.clima = LLUVIA
    with pytest.raises(dataclasses.FrozenInstanceError):
        Recorrido(MOMENTO).paradas = ()


# ---------- Tramos y recorrido ----------

def test_tramos():
    assert TramoAPie(700).metros_caminados() == 700
    assert TramoAPie(700).duracion_min() == 10
    assert TramoEnTransporte(2000).metros_caminados() == 0
    assert TramoEnTransporte(2000).duracion_min() == 7
    assert isinstance(tramo_entre(plaza("a", 0), plaza("b", 400)), TramoAPie)
    assert isinstance(tramo_entre(plaza("a", 0), plaza("b", 401)), TramoEnTransporte)


def test_recorrido_suma_sus_paradas():
    recorrido = (
        Recorrido(MOMENTO)
        .agregar_parada(plaza("A", 0), TramoAPie(100))
        .agregar_parada(Plaza("B", 100, 0, 45, 200, True), TramoEnTransporte(500))
    )
    assert recorrido.metros_caminados_total() == 100
    assert recorrido.duracion_total_min() == (1 + 15) + (2 + 45)
    assert recorrido.costo_total() == 200


def test_agregar_parada_no_modifica_el_original():
    original = Recorrido(MOMENTO)
    nuevo = original.agregar_parada(plaza("A", 0), TramoAPie(100))
    assert original.paradas == ()
    assert nombres(nuevo) == ["A"]


# ---------- Criterio ----------

def test_minima_caminata_prefiere_no_caminar_y_desempata_por_cercania():
    actual = plaza("Actual", 0)
    a_pie, cerca, lejos = plaza("A pie", 300), plaza("Cerca", 500), plaza("Lejos", 900)
    assert MinimaCaminata().elegir_siguiente(actual, [a_pie, lejos]) is lejos
    assert MinimaCaminata().elegir_siguiente(actual, [lejos, cerca]) is cerca


def test_mejor_recorrido_es_el_que_menos_camina():
    camina_mucho = Recorrido(MOMENTO).agregar_parada(plaza("P", 0), TramoAPie(300))
    camina_poco = Recorrido(MOMENTO).agregar_parada(plaza("P", 0), TramoAPie(50))
    assert mejor_recorrido([camina_mucho, camina_poco], MinimaCaminata()) is camina_poco


# ---------- Planificar ----------

def test_descarta_lugares_no_accesibles():
    recorrido = planificar_simple((plaza("Accesible", 50), plaza("No accesible", 10, accesible=False)), 120)
    assert nombres(recorrido) == ["Accesible"]


def test_respeta_el_tiempo_disponible():
    catalogo = tuple(plaza(f"Lugar {i}", i * 200) for i in range(1, 11))
    recorrido = planificar_simple(catalogo, 60)
    assert recorrido.duracion_total_min() <= 60
    assert len(recorrido.paradas) < len(catalogo)


def test_evita_caminar_si_hay_transporte():
    recorrido = planificar_simple((plaza("A", 300), plaza("B", 900), plaza("C", 920)), 300)
    assert nombres(recorrido) == ["B", "A", "C"]
    assert recorrido.metros_caminados_total() == 0


def test_si_el_elegido_no_entra_sigue_con_otro():
    recorrido = planificar_simple((plaza("A", 900, visita=100), plaza("B", 100, visita=10)), 30)
    assert nombres(recorrido) == ["B"]


def test_catalogo_vacio_da_recorrido_sin_paradas():
    assert planificar_simple((), 60).paradas == ()


def test_un_recorrido_no_afecta_a_otro_y_es_reproducible():
    catalogo = (plaza("A", 100), plaza("B", 200))
    primero = planificar_simple(catalogo, 120)
    segundo = planificar_simple(catalogo, 20)
    assert planificar_simple(catalogo, 120) == primero
    assert len(segundo.paradas) < len(primero.paradas)


def test_un_tipo_de_lugar_nuevo_funciona_sin_tocar_el_codigo():
    class Feria(Lugar):
        def esta_disponible(self, momento):
            return momento.franja == TARDE

    feria = Feria(nombre="Feria", x=100, y=0, duracion_visita_min=30, costo=0, es_accesible=True)
    assert nombres(planificar_simple((feria,), 60)) == ["Feria"]


def test_lugares_visitables_es_perezosa():
    class Roto(Lugar):
        def esta_disponible(self, momento):
            raise RuntimeError("se evaluó")

    visitables = lugares_visitables((Roto("x", 0, 0, 0, 0, True),), MOMENTO)  # no falla todavía
    with pytest.raises(RuntimeError):
        list(visitables)
