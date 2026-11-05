"""Arma un recorrido: en cada paso, le pregunta al criterio cuál es el próximo lugar a
visitar, hasta que no entra más tiempo. No busca el recorrido óptimo (el enunciado no lo
pide) — es un criterio simple, explicable, y fácil de cambiar sin tocar este archivo."""

from dataclasses import dataclass

from .criterios import CriterioDeCalidad, _distancia
from .lugares import Lugar
from .momento import Momento
from .recorrido import Parada, Recorrido
from .tramos import TramoAPie, TramoEnTransporte, TramoRuta

UMBRAL_TRANSPORTE_M = 400  # a partir de esta distancia conviene el transporte accesible


def _tramo_hacia(origen: Lugar, destino: Lugar) -> TramoRuta:
    distancia = round(_distancia(origen, destino))
    if distancia <= UMBRAL_TRANSPORTE_M:
        return TramoAPie(distancia_m=distancia)
    return TramoEnTransporte(distancia_m=distancia)


@dataclass(frozen=True)
class Planificador:
    catalogo: tuple[Lugar, ...]
    criterio: CriterioDeCalidad

    def planificar(self, partida: Lugar, momento: Momento, tiempo_disponible_min: int) -> Recorrido:
        disponibles = [lugar for lugar in self.catalogo if lugar.es_accesible and lugar.esta_disponible(momento)]
        paradas: list[Parada] = []
        actual = partida
        tiempo_usado = 0

        while disponibles:
            siguiente = self.criterio.elegir_siguiente(actual, disponibles)
            tramo = _tramo_hacia(actual, siguiente)
            duracion = tramo.duracion_min() + siguiente.duracion_visita_min
            if tiempo_usado + duracion > tiempo_disponible_min:
                break
            paradas.append(Parada(lugar=siguiente, tramo=tramo))
            tiempo_usado += duracion
            disponibles.remove(siguiente)
            actual = siguiente

        return Recorrido(momento_inicio=momento, paradas=tuple(paradas))
