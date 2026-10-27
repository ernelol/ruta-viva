"""Cómo se llega de un lugar al siguiente: a pie, o en un transporte accesible. Es su
propia jerarquía, separada de Lugar, porque la misma ruta puede alternar ambas — es la
pieza central de la variante (transporte combinado)."""

from abc import ABC, abstractmethod
from dataclasses import dataclass

RITMO_CAMINATA_M_POR_MIN = 70
RITMO_TRANSPORTE_M_POR_MIN = 300


class TramoRuta(ABC):
    @abstractmethod
    def metros_caminados(self) -> int:
        ...

    @abstractmethod
    def duracion_min(self) -> int:
        ...


@dataclass(frozen=True)
class TramoAPie(TramoRuta):
    distancia_m: int

    def metros_caminados(self) -> int:
        return self.distancia_m

    def duracion_min(self) -> int:
        return round(self.distancia_m / RITMO_CAMINATA_M_POR_MIN)


@dataclass(frozen=True)
class TramoEnTransporte(TramoRuta):
    distancia_m: int

    def metros_caminados(self) -> int:
        return 0

    def duracion_min(self) -> int:
        return round(self.distancia_m / RITMO_TRANSPORTE_M_POR_MIN)
