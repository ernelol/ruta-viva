"""Ruta viva: arma un recorrido para una persona con movilidad reducida.

Variante: movilidad reducida / transporte combinado / mínima caminata.
El diagrama UML y las decisiones de diseño están en DISENO.md.

Cómo está organizado este archivo (de arriba hacia abajo):
1. Momento: la franja del día y el clima.
2. Lugares: Lugar (abstracta) y sus tipos (Museo, Plaza, Mirador...).
3. Tramos: cómo se llega de un lugar a otro (a pie o en transporte).
4. Recorrido: la lista de paradas que se va armando.
5. Criterio: qué significa que un recorrido sea "mejor".
6. Planificar: la función que arma el recorrido usando todo lo anterior.
"""

# ABC y abstractmethod sirven para hacer clases abstractas (clases que no se pueden crear
# directamente y que obligan a sus hijas a definir ciertos métodos).
from abc import ABC, abstractmethod

# dataclass escribe solo el __init__ (y también __eq__ y __repr__) a partir de los atributos
# que declaro en la clase. Así no tengo que escribir "self.nombre = nombre" para cada uno.
from dataclasses import dataclass

# ---------- Momento: se arma a mano, nunca se lee el reloj ----------

# Las franjas del día y los climas son textos fijos (constantes). Uso constantes en vez de
# escribir "MANIANA" suelto por todo el código, así si me equivoco al escribir, Python avisa.
MANIANA, TARDE, NOCHE = "MANIANA", "TARDE", "NOCHE"
FRANJAS = (MANIANA, TARDE, NOCHE)  # en orden del día: así puedo comparar "abre antes de cerrar"
SOLEADO, NUBLADO, LLUVIA = "SOLEADO", "NUBLADO", "LLUVIA"
CLIMAS = (SOLEADO, NUBLADO, LLUVIA)


# frozen=True: una vez creado el objeto, no se puede cambiar ningún atributo (es inmutable).
# Si alguien intenta "momento.clima = LLUVIA", Python lanza FrozenInstanceError.
@dataclass(frozen=True)
class Momento:
    """El momento del recorrido: en qué franja del día y con qué clima.

    Se crea a mano y se le pasa al programa. El programa nunca mira la hora real de la
    computadora, por eso con los mismos datos siempre da el mismo resultado (y se puede testear).
    """

    franja: str
    clima: str

    # __post_init__ lo llama dataclass solo, justo después de crear el objeto.
    # Lo uso para validar: si los datos no tienen sentido, el objeto no llega a existir.
    def __post_init__(self):
        if self.franja not in FRANJAS:
            raise ValueError(f"franja inválida: {self.franja}")
        if self.clima not in CLIMAS:
            raise ValueError(f"clima inválido: {self.clima}")


# ---------- Lugares: lo común en Lugar, lo distinto en cada subtipo ----------

# Lugar hereda de ABC, entonces es abstracta: no se puede hacer Lugar(...) directamente
# (da TypeError). Hay que crear un tipo concreto: Museo, Plaza, Mirador, etc.
@dataclass(frozen=True)
class Lugar(ABC):
    """Lo que tienen en común todos los lugares que se pueden visitar."""

    nombre: str
    x: float  # posición en metros sobre un plano (la calcula armar_recorrido.py desde lat/lon)
    y: float
    duracion_visita_min: int  # cuántos minutos se queda la persona en el lugar
    costo: float  # cuánto sale la entrada
    es_accesible: bool  # si es False, el lugar nunca entra en un recorrido (filtro duro)

    # Invariantes: reglas que siempre tienen que cumplirse para que un Lugar sea válido.
    def __post_init__(self):
        if self.duracion_visita_min < 0:
            raise ValueError("la duración de la visita no puede ser negativa")
        if self.costo < 0:
            raise ValueError("el costo no puede ser negativo")

    # Método abstracto: Lugar no sabe responderlo, pero obliga a cada tipo a definirlo.
    # Acá está el polimorfismo: cada tipo de lugar responde distinto a la misma pregunta.
    @abstractmethod
    def esta_disponible(self, momento: Momento) -> bool:
        """Si se puede visitar en ese momento."""


@dataclass(frozen=True)
class LugarConHorario(Lugar):
    """Un lugar que abre en una franja y cierra en otra, dentro del mismo día.

    Existe para no repetir el mismo código en Museo y Restaurante: los dos tienen horario.
    """

    horario_apertura: str
    horario_cierre: str

    def __post_init__(self):
        # Primero corro las validaciones de Lugar (duración y costo), para no perderlas.
        super().__post_init__()
        # Después valido lo propio: que el horario exista...
        if self.horario_apertura not in FRANJAS or self.horario_cierre not in FRANJAS:
            raise ValueError("horario inválido")
        # ...y que no cierre antes de abrir. FRANJAS.index da la posición: MANIANA=0, TARDE=1, NOCHE=2.
        if FRANJAS.index(self.horario_apertura) > FRANJAS.index(self.horario_cierre):
            raise ValueError("no puede cerrar antes de abrir")

    def esta_disponible(self, momento):
        # Está abierto si la franja del momento cae entre la apertura y el cierre (inclusive).
        # Ejemplo: abre MANIANA (0), cierra TARDE (1); a la NOCHE (2) da False.
        return FRANJAS.index(self.horario_apertura) <= FRANJAS.index(momento.franja) <= FRANJAS.index(self.horario_cierre)


# Museo y Restaurante no agregan nada propio: heredan todo de LugarConHorario.
# Son clases separadas porque son tipos distintos del mundo real; si mañana un restaurante
# necesita una regla propia (por ejemplo, solo al mediodía), se cambia solo esta clase.
@dataclass(frozen=True)
class Museo(LugarConHorario):
    pass


@dataclass(frozen=True)
class Restaurante(LugarConHorario):
    pass


@dataclass(frozen=True)
class Plaza(Lugar):
    # Una plaza (o un parque, o una playa) siempre se puede visitar.
    def esta_disponible(self, momento):
        return True


@dataclass(frozen=True)
class Mirador(Lugar):
    # Con lluvia no tiene sentido ir a un mirador.
    def esta_disponible(self, momento):
        return momento.clima != LLUVIA


@dataclass(frozen=True)
class ParadaDeDescanso(Lugar):
    """Un banco o baño accesible: no es un atractivo, pero hace falta para esta persona."""

    def esta_disponible(self, momento):
        return True


# ---------- Tramos: cómo se llega de un lugar al siguiente ----------

# Valores supuestos (no medidos): son iguales para todos, y eso está anotado como sesgo en ETICA.md.
RITMO_CAMINATA_M_POR_MIN = 70  # metros por minuto caminando
RITMO_TRANSPORTE_M_POR_MIN = 300  # metros por minuto en transporte
UMBRAL_TRANSPORTE_M = 400  # más lejos que esto, se va en transporte accesible


# Clase abstracta: un tramo genérico no existe; hay tramo a pie o tramo en transporte.
class TramoRuta(ABC):
    # Cuántos metros hay que caminar en este tramo.
    @abstractmethod
    def metros_caminados(self) -> int: ...

    # Cuántos minutos lleva hacer este tramo.
    @abstractmethod
    def duracion_min(self) -> int: ...


@dataclass(frozen=True)
class TramoAPie(TramoRuta):
    distancia_m: int

    def metros_caminados(self):
        # A pie, todo lo que se recorre se camina.
        return self.distancia_m

    def duracion_min(self):
        # round redondea al minuto más cercano. Ejemplo: 700 m / 70 = 10 minutos.
        return round(self.distancia_m / RITMO_CAMINATA_M_POR_MIN)


@dataclass(frozen=True)
class TramoEnTransporte(TramoRuta):
    distancia_m: int

    def metros_caminados(self):
        # En transporte no se camina. Por eso el criterio MinimaCaminata prefiere el transporte.
        return 0

    def duracion_min(self):
        return round(self.distancia_m / RITMO_TRANSPORTE_M_POR_MIN)


# Función pura: con los mismos lugares siempre da el mismo número y no modifica nada.
def distancia(a: Lugar, b: Lugar) -> float:
    """Distancia en línea recta entre dos lugares, en metros (teorema de Pitágoras)."""
    return ((a.x - b.x) ** 2 + (a.y - b.y) ** 2) ** 0.5


def tramo_entre(origen: Lugar, destino: Lugar) -> TramoRuta:
    """Decide cómo se va de un lugar al otro: hasta 400 m a pie, más lejos en transporte."""
    metros = round(distancia(origen, destino))
    if metros <= UMBRAL_TRANSPORTE_M:
        return TramoAPie(metros)
    return TramoEnTransporte(metros)


# ---------- Recorrido: compone sus paradas ----------

@dataclass(frozen=True)
class Parada:
    """Una parada del recorrido: a qué lugar se va y cómo se llega (el tramo).

    La parada conoce el lugar y el tramo, pero no los crea: es asociación.
    """

    lugar: Lugar
    tramo: TramoRuta


@dataclass(frozen=True)
class Recorrido:
    """El recorrido que se va armando: desde dónde sale, en qué momento y sus paradas en orden."""

    partida: Lugar
    momento_inicio: Momento
    # Uso tupla y no lista: aunque la clase sea frozen, una lista igual aceptaría append
    # (se podría modificar por dentro). Una tupla no se puede modificar.
    paradas: tuple = ()

    def agregar_parada(self, lugar, tramo):
        """Crea la parada y devuelve un recorrido nuevo; este no cambia."""
        # No modifico este recorrido (es inmutable): armo uno NUEVO con una parada más.
        # (Parada(lugar, tramo),) es una tupla de un solo elemento; la coma es necesaria.
        # El Recorrido crea la Parada acá adentro: por eso la relación es de composición.
        return Recorrido(self.partida, self.momento_inicio, self.paradas + (Parada(lugar, tramo),))

    def lugar_actual(self):
        """Dónde está el recorrido: la última parada, o la partida si todavía no hay ninguna."""
        # paradas[-1] es la última parada de la tupla.
        return self.paradas[-1].lugar if self.paradas else self.partida

    # Los totales no se guardan: se calculan cada vez sumando las paradas, así nunca quedan
    # desactualizados. sum(... for ...) recorre las paradas sin armar una lista intermedia.
    def metros_caminados_total(self):
        return sum(parada.tramo.metros_caminados() for parada in self.paradas)

    def duracion_total_min(self):
        # Cada parada suma el tiempo del viaje hasta ahí más el tiempo de la visita.
        return sum(parada.tramo.duracion_min() + parada.lugar.duracion_visita_min for parada in self.paradas)

    def costo_total(self):
        return sum(parada.lugar.costo for parada in self.paradas)


# ---------- Criterio: qué le importa a la persona ----------

class CriterioDeCalidad(ABC):
    """Una sola pregunta: cuánto le cuesta un recorrido a la persona. Menos es mejor.

    Para crear un criterio nuevo alcanza con una clase hija que defina costo().
    planificar no se toca (patrón estrategia).
    """

    @abstractmethod
    def costo(self, recorrido: Recorrido) -> float: ...


class MinimaCaminata(CriterioDeCalidad):
    # El criterio del proyecto: un recorrido es mejor cuantos menos metros se caminen.
    def costo(self, recorrido):
        return recorrido.metros_caminados_total()


def mejor_recorrido(recorridos, criterio: CriterioDeCalidad) -> Recorrido:
    """Entre varios recorridos ya armados, devuelve el de menor costo según el criterio."""
    # key=criterio.costo: le paso a min una función (el método costo) para comparar.
    # Esto es una función de orden superior.
    return min(recorridos, key=criterio.costo)


def costo_de_ir(recorrido: Recorrido, lugar: Lugar, criterio: CriterioDeCalidad) -> tuple:
    """Cuánto costaría el recorrido si el próximo lugar fuera `lugar`. Si hay empate, gana el
    más cercano, así el resultado no depende del orden del catálogo."""
    actual = recorrido.lugar_actual()
    # Armo el recorrido "como quedaría" si fuera a ese lugar (no cambia el original).
    candidato = recorrido.agregar_parada(lugar, tramo_entre(actual, lugar))
    # Devuelvo un par (costo, distancia). Python compara pares por orden: primero el costo y,
    # si empatan, la distancia. Ejemplo: (0, 428) es menor que (0, 1097) y que (148, 148).
    return (criterio.costo(candidato), distancia(actual, lugar))


# ---------- Planificar: funciones puras ----------

def lugares_visitables(catalogo, momento):
    """Perezosa: filter no evalúa ningún lugar hasta que se lo recorre."""
    # Se queda solo con los lugares accesibles y abiertos en ese momento.
    # filter recibe una función (la lambda) y devuelve los lugares para los que da True.
    return filter(lambda lugar: lugar.es_accesible and lugar.esta_disponible(momento), catalogo)


def planificar(partida: Lugar, momento: Momento, tiempo_disponible_min: int,
               catalogo: tuple, criterio: CriterioDeCalidad) -> Recorrido:
    """En cada paso va al lugar que menos le suma al costo del recorrido. Si no entra en el
    tiempo que queda, se descarta y se sigue con los demás. La partida nunca se visita.
    No busca el óptimo."""
    # Invariante: el tiempo disponible no puede ser negativo.
    if tiempo_disponible_min < 0:
        raise ValueError("el tiempo disponible no puede ser negativo")

    # 1. Lugares que se pueden visitar: accesibles, abiertos y que no sean la partida.
    #    Es una lista local: la creo acá adentro, así que modificarla no afecta al catálogo.
    disponibles = [lugar for lugar in lugares_visitables(catalogo, momento) if lugar != partida]
    # 2. Arranco con un recorrido vacío que sale desde la partida.
    recorrido = Recorrido(partida, momento)

    # 3. Mientras queden lugares por probar.
    #    Uso un while porque cada paso depende de dónde quedó el recorrido en el paso anterior.
    while disponibles:
        # Elijo el lugar que menos le suma al costo. min compara usando costo_de_ir como key.
        siguiente = min(disponibles, key=lambda lugar: costo_de_ir(recorrido, lugar, criterio))
        # Lo saco de la lista para no volver a probarlo (entre o no entre).
        disponibles.remove(siguiente)
        # Cómo se llega hasta ahí y cuánto tiempo lleva: el viaje más la visita.
        tramo = tramo_entre(recorrido.lugar_actual(), siguiente)
        duracion = tramo.duracion_min() + siguiente.duracion_visita_min
        # Si entra en el tiempo que queda, lo agrego. Si no, lo salteo y sigo con los demás.
        if recorrido.duracion_total_min() + duracion <= tiempo_disponible_min:
            recorrido = recorrido.agregar_parada(siguiente, tramo)

    return recorrido
