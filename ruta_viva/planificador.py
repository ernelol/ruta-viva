"""Arma recorridos candidatos a partir de un catálogo de lugares, y elige el mejor según
un CriterioDeCalidad.

No busca el recorrido óptimo (el enunciado explícitamente no lo pide): arma un candidato
por cada lugar disponible que se podría visitar primero (desde ahí, siempre sigue al más
cercano), y deja que el criterio elija entre esos candidatos — simple, explicable, y
fácil de cambiar sin tocar el resto."""

from collections.abc import Iterator
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


def _armar_desde(
    partida: Lugar, primer_lugar: Lugar, catalogo: tuple[Lugar, ...], momento: Momento,
    tiempo_disponible_min: int,
) -> Recorrido:
    """Arma un recorrido que visita primero `primer_lugar`, y desde ahí sigue siempre
    al lugar disponible más cercano, mientras entre en el tiempo disponible."""
    tramo_inicial = _tramo_hacia(partida, primer_lugar)
    duracion_inicial = tramo_inicial.duracion_min() + primer_lugar.duracion_visita_min
    if duracion_inicial > tiempo_disponible_min:
        return Recorrido(momento_inicio=momento, paradas=())

    paradas: list[Parada] = [Parada(lugar=primer_lugar, tramo=tramo_inicial)]
    tiempo_usado = duracion_inicial
    actual = primer_lugar
    restantes = [lugar for lugar in _lugares_disponibles(catalogo, momento) if lugar != primer_lugar]

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


def candidatos_posibles(
    partida: Lugar, catalogo: tuple[Lugar, ...], momento: Momento, tiempo_disponible_min: int
) -> Iterator[Recorrido]:
    """Un candidato por cada lugar disponible que se podría visitar primero — evaluación
    perezosa: cada candidato se arma recién cuando algo lo pide (por ejemplo,
    elegir_mejor los va consumiendo de a uno con max()), no todos de antemano."""
    for primer_lugar in _lugares_disponibles(catalogo, momento):
        yield _armar_desde(partida, primer_lugar, catalogo, momento, tiempo_disponible_min)


def elegir_mejor(candidatos: Iterator[Recorrido], criterio: CriterioDeCalidad) -> Recorrido:
    return max(candidatos, key=criterio.puntuar)


@dataclass(frozen=True)
class Planificador:
    catalogo: tuple[Lugar, ...]
    criterio: CriterioDeCalidad

    def planificar(self, partida: Lugar, momento: Momento, tiempo_disponible_min: int) -> Recorrido:
        candidatos = candidatos_posibles(partida, self.catalogo, momento, tiempo_disponible_min)
        return elegir_mejor(candidatos, self.criterio)
