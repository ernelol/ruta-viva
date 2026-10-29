"""Corre varios casos de prueba con el programa real y genera visualizacion.html —
un mapa de los lugares con el recorrido elegido dibujado encima, para ver de un
vistazo qué hace el Planificador. Solo para mostrar/entender; no es parte del núcleo
(no se usa librería externa igual, pero no tiene tests ni forma parte de la entrega).

Correr con: .venv/bin/python3 visualizar.py
"""

import json
from pathlib import Path

from ruta_viva import (
    Clima,
    Franja,
    MinimaCaminata,
    Mirador,
    Momento,
    Museo,
    ParadaDeDescanso,
    Plaza,
    Planificador,
    Restaurante,
)

CATALOGO_PRINCIPAL = (
    Museo(
        nombre="Museo del Carnaval", x=100, y=50, duracion_visita_min=45, costo=150,
        es_accesible=True, horario_apertura=Franja.MANIANA, horario_cierre=Franja.TARDE,
    ),
    Plaza(nombre="Plaza Independencia", x=300, y=80, duracion_visita_min=20, costo=0, es_accesible=True),
    Restaurante(
        nombre="Mercado del Puerto", x=150, y=600, duracion_visita_min=60, costo=400,
        es_accesible=True, horario_apertura=Franja.MANIANA, horario_cierre=Franja.NOCHE,
    ),
    Mirador(nombre="Mirador del Cerro", x=400, y=350, duracion_visita_min=25, costo=0, es_accesible=False),
    ParadaDeDescanso(nombre="Banco accesible, Sarandí", x=250, y=60, duracion_visita_min=10, costo=0, es_accesible=True),
)

CATALOGO_MIRADOR_ACCESIBLE = (
    Mirador(nombre="Mirador accesible", x=120, y=40, duracion_visita_min=20, costo=0, es_accesible=True),
    Plaza(nombre="Plaza", x=300, y=0, duracion_visita_min=15, costo=0, es_accesible=True),
)

PARTIDA = Plaza(nombre="Punto de partida", x=0, y=0, duracion_visita_min=0, costo=0, es_accesible=True)
PARTIDA_B = Plaza(nombre="Partida B (cerca del Mercado)", x=200, y=500, duracion_visita_min=0, costo=0, es_accesible=True)

ESCENARIOS = [
    {
        "nombre": "Mañana soleada, 3 horas",
        "catalogo": CATALOGO_PRINCIPAL,
        "partida": PARTIDA,
        "momento": Momento(Franja.MANIANA, Clima.SOLEADO),
        "tiempo_disponible_min": 180,
    },
    {
        "nombre": "De noche (el Museo cierra)",
        "catalogo": CATALOGO_PRINCIPAL,
        "partida": PARTIDA,
        "momento": Momento(Franja.NOCHE, Clima.SOLEADO),
        "tiempo_disponible_min": 180,
    },
    {
        "nombre": "Partida distinta (cerca del Mercado)",
        "catalogo": CATALOGO_PRINCIPAL,
        "partida": PARTIDA_B,
        "momento": Momento(Franja.TARDE, Clima.SOLEADO),
        "tiempo_disponible_min": 180,
    },
    {
        "nombre": "Poco tiempo (20 min) — no entra nada",
        "catalogo": CATALOGO_PRINCIPAL,
        "partida": PARTIDA,
        "momento": Momento(Franja.MANIANA, Clima.SOLEADO),
        "tiempo_disponible_min": 20,
    },
    {
        "nombre": "Mirador accesible, sol",
        "catalogo": CATALOGO_MIRADOR_ACCESIBLE,
        "partida": PARTIDA,
        "momento": Momento(Franja.TARDE, Clima.SOLEADO),
        "tiempo_disponible_min": 120,
    },
    {
        "nombre": "Mismo Mirador accesible, pero llueve",
        "catalogo": CATALOGO_MIRADOR_ACCESIBLE,
        "partida": PARTIDA,
        "momento": Momento(Franja.TARDE, Clima.LLUVIA),
        "tiempo_disponible_min": 120,
    },
]


def _lugar_a_json(lugar, visitado: bool, motivo_exclusion: str | None) -> dict:
    return {
        "nombre": lugar.nombre,
        "x": lugar.x,
        "y": lugar.y,
        "tipo": type(lugar).__name__,
        "es_accesible": lugar.es_accesible,
        "visitado": visitado,
        "motivo_exclusion": motivo_exclusion,
    }


def _motivo_exclusion(lugar, momento) -> str:
    if not lugar.es_accesible:
        return "no accesible"
    if not lugar.esta_disponible(momento):
        return "no disponible a esta hora/clima"
    return "no entró por tiempo"


def _escenario_a_json(escenario: dict) -> dict:
    planificador = Planificador(catalogo=escenario["catalogo"], criterio=MinimaCaminata())
    recorrido = planificador.planificar(escenario["partida"], escenario["momento"], escenario["tiempo_disponible_min"])
    visitados = {parada.lugar.nombre for parada in recorrido.paradas}

    lugares_json = [
        _lugar_a_json(lugar, lugar.nombre in visitados, None if lugar.nombre in visitados else _motivo_exclusion(lugar, escenario["momento"]))
        for lugar in escenario["catalogo"]
    ]

    paradas_json = [
        {
            "nombre": parada.lugar.nombre,
            "x": parada.lugar.x,
            "y": parada.lugar.y,
            "tramo": type(parada.tramo).__name__,
            "metros_caminados": parada.tramo.metros_caminados(),
        }
        for parada in recorrido.paradas
    ]

    return {
        "nombre": escenario["nombre"],
        "partida": {"nombre": escenario["partida"].nombre, "x": escenario["partida"].x, "y": escenario["partida"].y},
        "momento": f"{escenario['momento'].franja.name} / {escenario['momento'].clima.name}",
        "tiempo_disponible_min": escenario["tiempo_disponible_min"],
        "lugares": lugares_json,
        "paradas": paradas_json,
        "metros_caminados_total": recorrido.metros_caminados_total(),
        "duracion_total_min": recorrido.duracion_total_min(),
        "costo_total": recorrido.costo_total(),
    }


def generar_html() -> None:
    datos = [_escenario_a_json(escenario) for escenario in ESCENARIOS]
    plantilla = (Path(__file__).parent / "visualizacion_plantilla.html").read_text()
    html = plantilla.replace("/*__DATOS__*/", json.dumps(datos, ensure_ascii=False))
    Path("visualizacion.html").write_text(html)
    print(f"Generado visualizacion.html con {len(datos)} escenarios.")


if __name__ == "__main__":
    generar_html()
