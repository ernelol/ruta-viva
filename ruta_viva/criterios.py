"""Cómo se decide que un recorrido es mejor que otro. Separado de Recorrido y de
Planificador a propósito (patrón Estrategia): agregar un criterio nuevo no toca el
algoritmo que arma recorridos, solo agrega una clase más acá."""

from abc import ABC, abstractmethod

from .recorrido import Recorrido


class CriterioDeCalidad(ABC):
    @abstractmethod
    def puntuar(self, recorrido: Recorrido) -> float:
        """Más alto es mejor."""


class MinimaCaminata(CriterioDeCalidad):
    def puntuar(self, recorrido: Recorrido) -> float:
        return -recorrido.metros_caminados_total()
