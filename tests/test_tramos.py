from ruta_viva import TramoAPie, TramoEnTransporte


def test_tramo_a_pie_cuenta_los_metros():
    tramo = TramoAPie(distancia_m=700)
    assert tramo.metros_caminados() == 700
    assert tramo.duracion_min() == round(700 / 70)


def test_tramo_en_transporte_no_suma_metros_caminados():
    tramo = TramoEnTransporte(distancia_m=2000)
    assert tramo.metros_caminados() == 0
    assert tramo.duracion_min() == round(2000 / 300)
