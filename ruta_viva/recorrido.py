"""Parada: un lugar y cómo se llega a él. Recorrido: una secuencia ordenada de paradas.

Recorrido.paradas es una tupla, no una lista — con frozen=True una lista todavía se
podría mutar en el lugar (append, etc.); una tupla no."""

from dataclasses import dataclass

from .lugares import Lugar
from .momento import Momento
from .tramos import TramoRuta


@dataclass(frozen=True)
class Parada:
    lugar: Lugar
    tramo: TramoRuta


@dataclass(frozen=True)
class Recorrido:
    momento_inicio: Momento
    paradas: tuple[Parada, ...]

    def metros_caminados_total(self) -> int:
        return sum(parada.tramo.metros_caminados() for parada in self.paradas)

    def duracion_total_min(self) -> int:
        return sum(
            parada.tramo.duracion_min() + parada.lugar.duracion_visita_min
            for parada in self.paradas
        )

    def costo_total(self) -> float:
        return sum(parada.lugar.costo for parada in self.paradas)
