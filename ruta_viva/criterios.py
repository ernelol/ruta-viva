"""Cómo se decide, en cada paso, cuál es el próximo lugar a visitar. Separado del
Planificador a propósito: cambiar el criterio (por ejemplo, a "visitar primero el más
barato") no debería tocar el algoritmo que arma el recorrido."""

from abc import ABC, abstractmethod

from .lugares import Lugar


class CriterioDeCalidad(ABC):
    @abstractmethod
    def elegir_siguiente(self, actual: Lugar, disponibles: list[Lugar]) -> Lugar:
        """Cuál de los lugares disponibles conviene visitar después de `actual`."""


class MinimaCaminata(CriterioDeCalidad):
    def elegir_siguiente(self, actual: Lugar, disponibles: list[Lugar]) -> Lugar:
        return min(disponibles, key=lambda lugar: _distancia(actual, lugar))


def _distancia(a: Lugar, b: Lugar) -> float:
    return ((a.x - b.x) ** 2 + (a.y - b.y) ** 2) ** 0.5
