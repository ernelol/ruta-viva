"""El momento simulado de un recorrido. Nunca se lee del reloj del sistema real:
siempre se construye a mano y se inyecta, para que el cálculo sea reproducible."""

from dataclasses import dataclass
from enum import Enum, auto


class Franja(Enum):
    MANIANA = auto()
    TARDE = auto()
    NOCHE = auto()


class Clima(Enum):
    SOLEADO = auto()
    NUBLADO = auto()
    LLUVIA = auto()


@dataclass(frozen=True)
class Momento:
    franja: Franja
    clima: Clima
