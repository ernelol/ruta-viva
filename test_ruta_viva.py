"""Tests de Ruta viva. Se corren con: .venv/bin/pytest -v

Cada test arma lugares en una línea recta (x = 100, 200, ...) y un momento fijo, así el
resultado es siempre el mismo y no depende de la hora ni de dónde está la computadora.
"""

import dataclasses

import pytest

from ruta_viva import (
    LLUVIA, MANIANA, NOCHE, SOLEADO, TARDE,
    CriterioDeCalidad, Lugar, MinimaCaminata, Mirador, Momento, Museo, ParadaDeDescanso, Plaza,
    Recorrido, Restaurante, TramoAPie, TramoEnTransporte, TramoRuta,
    costo_de_ir, lugares_visitables, mejor_recorrido, planificar, tramo_entre,
)

# Un momento fijo para todos los tests: de tarde y con sol.
MOMENTO = Momento(TARDE, SOLEADO)


def plaza(nombre, x, visita=15, accesible=True, costo=0):
    """Atajo para crear una Plaza en la posición x (y siempre en 0)."""
    return Plaza(nombre=nombre, x=x, y=0, duracion_visita_min=visita, costo=costo, es_accesible=accesible)


# El punto de partida de casi todos los tests: en el 0.
PARTIDA = plaza("Partida", 0)


def nombres(recorrido):
    """Los nombres de las paradas en orden, para comparar fácil."""
    return [parada.lugar.nombre for parada in recorrido.paradas]


def planificar_simple(catalogo, minutos):
    """planificar con la partida, el momento y el criterio de siempre."""
    return planificar(PARTIDA, MOMENTO, minutos, catalogo, MinimaCaminata())


# ---------- Abstracción ----------

def test_las_clases_abstractas_no_se_pueden_crear():
    # pytest.raises comprueba que el código de adentro lance ese error.
    # Las clases abstractas (ABC) no se pueden crear directamente: lanzan TypeError.
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
    # El museo abre de mañana a tarde; el restaurante de tarde a noche.
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
    # Cada caso tiene que lanzar ValueError: los datos inválidos no llegan a crear el objeto.
    with pytest.raises(ValueError):
        plaza("x", 0, visita=-1)  # duración negativa
    with pytest.raises(ValueError):
        Momento("MEDIANOCHE", SOLEADO)  # franja que no existe
    with pytest.raises(ValueError):
        Momento(TARDE, "GRANIZO")  # clima que no existe
    with pytest.raises(ValueError):
        planificar_simple((), -1)  # tiempo negativo
    with pytest.raises(ValueError):
        Museo("M", 0, 0, 30, 0, True, horario_apertura="ALMUERZO", horario_cierre=TARDE)  # horario que no existe
    with pytest.raises(ValueError):
        Museo("M", 0, 0, 30, 0, True, horario_apertura=NOCHE, horario_cierre=MANIANA)  # cierra antes de abrir


def test_los_objetos_son_inmutables():
    # Con frozen=True, cambiar o agregar un atributo lanza FrozenInstanceError.
    with pytest.raises(dataclasses.FrozenInstanceError):
        plaza("P", 0).costo = 999
    with pytest.raises(dataclasses.FrozenInstanceError):
        plaza("P", 0).otro_atributo = 1
    with pytest.raises(dataclasses.FrozenInstanceError):
        MOMENTO.clima = LLUVIA
    with pytest.raises(dataclasses.FrozenInstanceError):
        Recorrido(PARTIDA, MOMENTO).paradas = ()


# ---------- Tramos y recorrido ----------

def test_tramos():
    # 700 m a pie: se caminan los 700 m y llevan 700 / 70 = 10 minutos.
    assert TramoAPie(700).metros_caminados() == 700
    assert TramoAPie(700).duracion_min() == 10
    # 2000 m en transporte: no se camina nada y llevan round(2000 / 300) = 7 minutos.
    assert TramoEnTransporte(2000).metros_caminados() == 0
    assert TramoEnTransporte(2000).duracion_min() == 7
    # El límite: 400 m todavía es a pie; 401 m ya va en transporte.
    assert isinstance(tramo_entre(plaza("a", 0), plaza("b", 400)), TramoAPie)
    assert isinstance(tramo_entre(plaza("a", 0), plaza("b", 401)), TramoEnTransporte)


def test_recorrido_suma_sus_paradas():
    # Una parada a pie (100 m) y otra en transporte (500 m) que cuesta 200.
    recorrido = (
        Recorrido(PARTIDA, MOMENTO)
        .agregar_parada(plaza("A", 0), TramoAPie(100))
        .agregar_parada(Plaza("B", 100, 0, 45, 200, True), TramoEnTransporte(500))
    )
    assert recorrido.metros_caminados_total() == 100  # el transporte no suma metros
    assert recorrido.duracion_total_min() == (1 + 15) + (2 + 45)  # viaje + visita de cada una
    assert recorrido.costo_total() == 200


def test_agregar_parada_no_modifica_el_original():
    # agregar_parada devuelve un recorrido nuevo; el original queda igual (inmutabilidad).
    original = Recorrido(PARTIDA, MOMENTO)
    nuevo = original.agregar_parada(plaza("A", 0), TramoAPie(100))
    assert original.paradas == ()
    assert nombres(nuevo) == ["A"]


def test_recorrido_conoce_su_partida_y_donde_esta():
    recorrido = Recorrido(PARTIDA, MOMENTO)
    # Sin paradas, está en la partida. "is" comprueba que sea el mismo objeto.
    assert recorrido.lugar_actual() is PARTIDA
    a = plaza("A", 100)
    # Con una parada, está en esa parada; la partida no cambia.
    assert recorrido.agregar_parada(a, TramoAPie(100)).lugar_actual() is a
    assert recorrido.agregar_parada(a, TramoAPie(100)).partida is PARTIDA


# ---------- Criterio ----------

def test_minima_caminata_cuesta_los_metros_caminados():
    # 300 m a pie + 600 m en transporte: el costo son solo los 300 m caminados.
    recorrido = (
        Recorrido(PARTIDA, MOMENTO)
        .agregar_parada(plaza("A", 300), TramoAPie(300))
        .agregar_parada(plaza("B", 900), TramoEnTransporte(600))
    )
    assert MinimaCaminata().costo(recorrido) == 300


def test_costo_de_ir_suma_el_tramo_y_desempata_por_distancia():
    # costo_de_ir devuelve (costo, distancia).
    recorrido = Recorrido(PARTIDA, MOMENTO)
    # A está a 300 m: se camina, cuesta 300.
    assert costo_de_ir(recorrido, plaza("A", 300), MinimaCaminata()) == (300, 300)
    # B está a 900 m: va en transporte, cuesta 0.
    assert costo_de_ir(recorrido, plaza("B", 900), MinimaCaminata()) == (0, 900)


def test_mejor_recorrido_es_el_que_menos_camina():
    camina_mucho = Recorrido(PARTIDA, MOMENTO).agregar_parada(plaza("P", 0), TramoAPie(300))
    camina_poco = Recorrido(PARTIDA, MOMENTO).agregar_parada(plaza("P", 0), TramoAPie(50))
    assert mejor_recorrido([camina_mucho, camina_poco], MinimaCaminata()) is camina_poco


# ---------- Planificar ----------

def test_descarta_lugares_no_accesibles():
    # Aunque el no accesible esté más cerca, nunca entra en el recorrido.
    recorrido = planificar_simple((plaza("Accesible", 50), plaza("No accesible", 10, accesible=False)), 120)
    assert nombres(recorrido) == ["Accesible"]


def test_respeta_el_tiempo_disponible():
    # 10 lugares cada 200 m y solo 60 minutos: no entran todos.
    catalogo = tuple(plaza(f"Lugar {i}", i * 200) for i in range(1, 11))
    recorrido = planificar_simple(catalogo, 60)
    assert recorrido.duracion_total_min() <= 60
    assert len(recorrido.paradas) < len(catalogo)


def test_minimiza_la_caminata_ejemplo_del_profesor():
    # A 390 m a pie y después B en transporte caminaría 390 m; al revés, 0 m
    recorrido = planificar_simple((plaza("A", 390), plaza("B", 800)), 300)
    assert nombres(recorrido) == ["B", "A"]
    assert recorrido.metros_caminados_total() == 0


def test_evita_caminar_cuando_hay_transporte():
    # antes daba A, B, C con 320 m caminados; ahora camina menos
    recorrido = planificar_simple((plaza("A", 300), plaza("B", 900), plaza("C", 920)), 300)
    assert nombres(recorrido) == ["B", "A", "C"]
    assert recorrido.metros_caminados_total() == 0


def test_empate_de_costo_no_depende_del_orden_del_catalogo():
    lejos, cerca = plaza("Lejos", 900), plaza("Cerca", 500)  # los dos en transporte: 0 m
    # Paso el catálogo en los dos órdenes: el resultado tiene que ser el mismo.
    assert nombres(planificar_simple((lejos, cerca), 300)) == nombres(planificar_simple((cerca, lejos), 300))
    # Y empatan en costo (0 m), así que gana el más cercano.
    assert nombres(planificar_simple((lejos, cerca), 300))[0] == "Cerca"


def test_la_partida_no_se_visita_aunque_este_en_el_catalogo():
    recorrido = planificar_simple((PARTIDA, plaza("A", 100)), 120)
    assert nombres(recorrido) == ["A"]


def test_un_criterio_nuevo_solo_implementa_costo():
    # Un criterio inventado para el test: gastar la menor plata posible.
    # Solo define costo, y planificar funciona igual sin tocarlo.
    class MenosPlata(CriterioDeCalidad):
        def costo(self, recorrido):
            return recorrido.costo_total()

    catalogo = (plaza("Cara", 100, costo=500), plaza("Barata", 900, costo=0))
    recorrido = planificar(PARTIDA, MOMENTO, 20, catalogo, MenosPlata())
    assert nombres(recorrido) == ["Barata"]


def test_si_el_elegido_no_entra_sigue_con_otro():
    # A cuesta 0 (transporte) y se elige primero, pero con 100 min de visita no entra en 30.
    # En vez de terminar, lo saltea y prueba B, que sí entra.
    recorrido = planificar_simple((plaza("A", 900, visita=100), plaza("B", 100, visita=10)), 30)
    assert nombres(recorrido) == ["B"]


def test_catalogo_vacio_da_recorrido_sin_paradas():
    assert planificar_simple((), 60).paradas == ()


def test_un_recorrido_no_afecta_a_otro_y_es_reproducible():
    catalogo = (plaza("A", 100), plaza("B", 200))
    primero = planificar_simple(catalogo, 120)
    segundo = planificar_simple(catalogo, 20)
    # Calcular el segundo no cambió el primero, y repetir el cálculo da lo mismo.
    assert planificar_simple(catalogo, 120) == primero
    assert len(segundo.paradas) < len(primero.paradas)


def test_un_tipo_de_lugar_nuevo_funciona_sin_tocar_el_codigo():
    # Un tipo de lugar que no existe en ruta_viva.py: lo defino acá mismo.
    class Feria(Lugar):
        def esta_disponible(self, momento):
            return momento.franja == TARDE

    feria = Feria(nombre="Feria", x=100, y=0, duracion_visita_min=30, costo=0, es_accesible=True)
    assert nombres(planificar_simple((feria,), 60)) == ["Feria"]


def test_lugares_visitables_es_perezosa():
    # Un lugar que explota si alguien le pregunta si está disponible.
    class Roto(Lugar):
        def esta_disponible(self, momento):
            raise RuntimeError("se evaluó")

    visitables = lugares_visitables((Roto("x", 0, 0, 0, 0, True),), MOMENTO)  # no falla todavía
    # Recién falla cuando se recorre el filter (list lo recorre).
    with pytest.raises(RuntimeError):
        list(visitables)
