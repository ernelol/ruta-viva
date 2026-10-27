"""Arma un recorrido candidato a partir de un catálogo de lugares, y elige el mejor
candidato según un CriterioDeCalidad.

No busca el recorrido óptimo (el enunciado explícitamente no lo pide) — usa un criterio
simple y explicable: desde el punto de partida, visita siempre el lugar disponible y
accesible más cercano, mientras entre en el tiempo disponible."""

from dataclasses import dataclass

from .criterios import CriterioDeCalidad
from .lugares import Lugar
from .momento import Momento
from .recorrido import Parada, Recorrido
from .tramos import TramoAPie, TramoEnTransporte, TramoRuta

UMBRAL_TRANSPORTE_M = 400  # a partir de esta distancia conviene el transporte accesible


def _distancia_m(origen: Lugar, destino: Lugar) -> int:
    return round(((origen.x - destino.x) ** 2 + (origen.y - destino.y) ** 2) ** 0.5)


def _tramo_hacia(origen: Lugar, destino: Lugar) -> TramoRuta:
    distancia = _distancia_m(origen, destino)
    if distancia <= UMBRAL_TRANSPORTE_M:
        return TramoAPie(distancia_m=distancia)
    return TramoEnTransporte(distancia_m=distancia)


def _lugares_disponibles(catalogo: tuple[Lugar, ...], momento: Momento) -> list[Lugar]:
    return [lugar for lugar in catalogo if lugar.es_accesible and lugar.esta_disponible(momento)]


def armar_candidato(
    partida: Lugar, catalogo: tuple[Lugar, ...], momento: Momento, tiempo_disponible_min: int
) -> Recorrido:
    restantes = _lugares_disponibles(catalogo, momento)
    paradas: list[Parada] = []
    actual = partida
    tiempo_usado = 0

    while restantes:
        siguiente = min(restantes, key=lambda lugar: _distancia_m(actual, lugar))
        tramo = _tramo_hacia(actual, siguiente)
        duracion_parada = tramo.duracion_min() + siguiente.duracion_visita_min
        if tiempo_usado + duracion_parada > tiempo_disponible_min:
            break
        paradas.append(Parada(lugar=siguiente, tramo=tramo))
        tiempo_usado += duracion_parada
        restantes.remove(siguiente)
        actual = siguiente

    return Recorrido(momento_inicio=momento, paradas=tuple(paradas))


def elegir_mejor(candidatos: list[Recorrido], criterio: CriterioDeCalidad) -> Recorrido:
    return max(candidatos, key=criterio.puntuar)


@dataclass(frozen=True)
class Planificador:
    catalogo: tuple[Lugar, ...]
    criterio: CriterioDeCalidad

    def planificar(self, partida: Lugar, momento: Momento, tiempo_disponible_min: int) -> Recorrido:
        candidato = armar_candidato(partida, self.catalogo, momento, tiempo_disponible_min)
        return elegir_mejor([candidato], self.criterio)
