# Ruta viva

Planificador de recorridos a pie para una persona con movilidad reducida. Dado un punto
de partida, un momento del día y un tiempo disponible, arma un recorrido que minimiza la
caminata, combinando tramos a pie con transporte accesible y descartando lugares que no
son accesibles de verdad.

Ver `DISENO.md` para la variante elegida, el UML y las decisiones de diseño.

## Cómo correrlo

```bash
python3 -m venv .venv
.venv/bin/pip install pytest
.venv/bin/python3 ejemplo.py     # corrida de punta a punta
.venv/bin/pytest -v              # los tests
```

Solo usa la librería estándar de Python — `pytest` es la única dependencia, y es
exclusivamente para los tests (no lo importa el programa en sí).

## Estructura

```
ruta_viva/
  momento.py        Momento, Franja, Clima — nunca se lee el reloj del sistema
  lugares.py         Lugar (abstracta) y sus 5 subtipos
  tramos.py          TramoRuta (abstracta): a pie / en transporte
  recorrido.py       Parada, Recorrido
  criterios.py        CriterioDeCalidad (Estrategia): MinimaCaminata
  planificador.py     arma un recorrido candidato y elige el mejor
tests/                14 tests de pytest, uno por módulo
ejemplo.py             corrida completa con un catálogo de ejemplo
```

## Documentos del proyecto

- `DISENO.md` — variante, UML, decisiones y alternativas descartadas (Hito 1)
- `BITACORA_IA.md` — cada uso de IA, qué devolvió, qué se corrigió
- `PREDICCIONES.md` — predicciones antes de correr funciones clave, comparadas con el resultado real
- `ETICA.md` — datos que maneja la app, riesgo ético y mitigación, marco legal, uso de IA
