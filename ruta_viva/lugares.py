"""Los lugares que puede visitar un recorrido. Lugar es abstracta: cada subtipo decide
distinto cuándo está disponible. Agregar un tipo de lugar nuevo no toca el resto del
programa — ese es el punto del polimorfismo acá."""

from abc import ABC, abstractmethod
from dataclasses import dataclass

from .momento import Clima, Franja, Momento


@dataclass(frozen=True)
class Lugar(ABC):
    nombre: str
    x: float  # posición en un plano inventado, en metros — no es GPS real
    y: float
    duracion_visita_min: int
    costo: float
    es_accesible: bool

    @abstractmethod
    def esta_disponible(self, momento: Momento) -> bool:
        """Si tiene sentido visitar este lugar en ese momento (horario, clima, etc.)."""


@dataclass(frozen=True)
class Museo(Lugar):
    horario_apertura: Franja
    horario_cierre: Franja

    def esta_disponible(self, momento: Momento) -> bool:
        return self.horario_apertura.value <= momento.franja.value <= self.horario_cierre.value


@dataclass(frozen=True)
class Plaza(Lugar):
    def esta_disponible(self, momento: Momento) -> bool:
        return True


@dataclass(frozen=True)
class Mirador(Lugar):
    def esta_disponible(self, momento: Momento) -> bool:
        return momento.clima != Clima.LLUVIA


@dataclass(frozen=True)
class Restaurante(Lugar):
    horario_apertura: Franja
    horario_cierre: Franja

    def esta_disponible(self, momento: Momento) -> bool:
        return self.horario_apertura.value <= momento.franja.value <= self.horario_cierre.value


@dataclass(frozen=True)
class ParadaDeDescanso(Lugar):
    """Un banco o baño accesible: no es un atractivo, pero hace falta en un recorrido
    largo para alguien con movilidad reducida. Siempre disponible, sin horario."""

    def esta_disponible(self, momento: Momento) -> bool:
        return True
