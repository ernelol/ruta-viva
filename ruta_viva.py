"""Ruta viva: arma un recorrido para una persona con movilidad reducida.

Variante: movilidad reducida / transporte combinado / mínima caminata.
El diagrama UML y las decisiones de diseño están en DISENO.md.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass

# ---------- Momento: se arma a mano, nunca se lee el reloj ----------

MANIANA, TARDE, NOCHE = "MANIANA", "TARDE", "NOCHE"
FRANJAS = (MANIANA, TARDE, NOCHE)  # en orden del día
SOLEADO, NUBLADO, LLUVIA = "SOLEADO", "NUBLADO", "LLUVIA"
CLIMAS = (SOLEADO, NUBLADO, LLUVIA)


@dataclass(frozen=True)
class Momento:
    franja: str
    clima: str

    def __post_init__(self):
        if self.franja not in FRANJAS:
            raise ValueError(f"franja inválida: {self.franja}")
        if self.clima not in CLIMAS:
            raise ValueError(f"clima inválido: {self.clima}")


# ---------- Lugares: lo común en Lugar, lo distinto en cada subtipo ----------

@dataclass(frozen=True)
class Lugar(ABC):
    nombre: str
    x: float  # metros sobre un plano
    y: float
    duracion_visita_min: int
    costo: float
    es_accesible: bool

    def __post_init__(self):
        if self.duracion_visita_min < 0:
            raise ValueError("la duración de la visita no puede ser negativa")
        if self.costo < 0:
            raise ValueError("el costo no puede ser negativo")

    @abstractmethod
    def esta_disponible(self, momento: Momento) -> bool:
        """Si se puede visitar en ese momento."""


@dataclass(frozen=True)
class LugarConHorario(Lugar):
    """Abre en una franja y cierra en otra, dentro del mismo día."""
    horario_apertura: str
    horario_cierre: str

    def __post_init__(self):
        super().__post_init__()
        if self.horario_apertura not in FRANJAS or self.horario_cierre not in FRANJAS:
            raise ValueError("horario inválido")
        if FRANJAS.index(self.horario_apertura) > FRANJAS.index(self.horario_cierre):
            raise ValueError("no puede cerrar antes de abrir")

    def esta_disponible(self, momento):
        return FRANJAS.index(self.horario_apertura) <= FRANJAS.index(momento.franja) <= FRANJAS.index(self.horario_cierre)


@dataclass(frozen=True)
class Museo(LugarConHorario):
    pass


@dataclass(frozen=True)
class Restaurante(LugarConHorario):
    pass


@dataclass(frozen=True)
class Plaza(Lugar):
    def esta_disponible(self, momento):
        return True


@dataclass(frozen=True)
class Mirador(Lugar):
    def esta_disponible(self, momento):
        return momento.clima != LLUVIA


@dataclass(frozen=True)
class ParadaDeDescanso(Lugar):
    """Un banco o baño accesible: no es un atractivo, pero hace falta para esta persona."""

    def esta_disponible(self, momento):
        return True


# ---------- Tramos: cómo se llega de un lugar al siguiente ----------

RITMO_CAMINATA_M_POR_MIN = 70
RITMO_TRANSPORTE_M_POR_MIN = 300
UMBRAL_TRANSPORTE_M = 400  # más lejos que esto, se va en transporte accesible


class TramoRuta(ABC):
    @abstractmethod
    def metros_caminados(self) -> int: ...

    @abstractmethod
    def duracion_min(self) -> int: ...


@dataclass(frozen=True)
class TramoAPie(TramoRuta):
    distancia_m: int

    def metros_caminados(self):
        return self.distancia_m

    def duracion_min(self):
        return round(self.distancia_m / RITMO_CAMINATA_M_POR_MIN)


@dataclass(frozen=True)
class TramoEnTransporte(TramoRuta):
    distancia_m: int

    def metros_caminados(self):
        return 0

    def duracion_min(self):
        return round(self.distancia_m / RITMO_TRANSPORTE_M_POR_MIN)


def distancia(a: Lugar, b: Lugar) -> float:
    return ((a.x - b.x) ** 2 + (a.y - b.y) ** 2) ** 0.5


def tramo_entre(origen: Lugar, destino: Lugar) -> TramoRuta:
    metros = round(distancia(origen, destino))
    if metros <= UMBRAL_TRANSPORTE_M:
        return TramoAPie(metros)
    return TramoEnTransporte(metros)


# ---------- Recorrido: compone sus paradas ----------

@dataclass(frozen=True)
class Parada:
    lugar: Lugar
    tramo: TramoRuta


@dataclass(frozen=True)
class Recorrido:
    partida: Lugar
    momento_inicio: Momento
    paradas: tuple = ()  # tupla: con frozen, una lista igual aceptaría append

    def agregar_parada(self, lugar, tramo):
        """Crea la parada y devuelve un recorrido nuevo; este no cambia."""
        return Recorrido(self.partida, self.momento_inicio, self.paradas + (Parada(lugar, tramo),))

    def lugar_actual(self):
        """Dónde está el recorrido: la última parada, o la partida si todavía no hay ninguna."""
        return self.paradas[-1].lugar if self.paradas else self.partida

    def metros_caminados_total(self):
        return sum(parada.tramo.metros_caminados() for parada in self.paradas)

    def duracion_total_min(self):
        return sum(parada.tramo.duracion_min() + parada.lugar.duracion_visita_min for parada in self.paradas)

    def costo_total(self):
        return sum(parada.lugar.costo for parada in self.paradas)


# ---------- Criterio: qué le importa a la persona ----------

class CriterioDeCalidad(ABC):
    """Una sola pregunta: cuánto le cuesta un recorrido a la persona. Menos es mejor."""

    @abstractmethod
    def costo(self, recorrido: Recorrido) -> float: ...


class MinimaCaminata(CriterioDeCalidad):
    def costo(self, recorrido):
        return recorrido.metros_caminados_total()


def mejor_recorrido(recorridos, criterio: CriterioDeCalidad) -> Recorrido:
    return min(recorridos, key=criterio.costo)


def costo_de_ir(recorrido: Recorrido, lugar: Lugar, criterio: CriterioDeCalidad) -> tuple:
    """Cuánto costaría el recorrido si el próximo lugar fuera `lugar`. Si hay empate, gana el
    más cercano, así el resultado no depende del orden del catálogo."""
    actual = recorrido.lugar_actual()
    candidato = recorrido.agregar_parada(lugar, tramo_entre(actual, lugar))
    return (criterio.costo(candidato), distancia(actual, lugar))


# ---------- Planificar: funciones puras ----------

def lugares_visitables(catalogo, momento):
    """Perezosa: filter no evalúa ningún lugar hasta que se lo recorre."""
    return filter(lambda lugar: lugar.es_accesible and lugar.esta_disponible(momento), catalogo)


def planificar(partida: Lugar, momento: Momento, tiempo_disponible_min: int,
               catalogo: tuple, criterio: CriterioDeCalidad) -> Recorrido:
    """En cada paso va al lugar que menos le suma al costo del recorrido. Si no entra en el
    tiempo que queda, se descarta y se sigue con los demás. La partida nunca se visita.
    No busca el óptimo."""
    if tiempo_disponible_min < 0:
        raise ValueError("el tiempo disponible no puede ser negativo")

    disponibles = [lugar for lugar in lugares_visitables(catalogo, momento) if lugar != partida]
    recorrido = Recorrido(partida, momento)

    while disponibles:
        siguiente = min(disponibles, key=lambda lugar: costo_de_ir(recorrido, lugar, criterio))
        disponibles.remove(siguiente)
        tramo = tramo_entre(recorrido.lugar_actual(), siguiente)
        duracion = tramo.duracion_min() + siguiente.duracion_visita_min
        if recorrido.duracion_total_min() + duracion <= tiempo_disponible_min:
            recorrido = recorrido.agregar_parada(siguiente, tramo)

    return recorrido
