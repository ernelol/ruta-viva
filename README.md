# Ruta viva

Planificador de recorridos para una persona con movilidad reducida. Dado un punto de partida,
un momento del día y un tiempo disponible, arma un recorrido que evita caminar cuando puede,
combinando tramos a pie con transporte accesible y descartando lugares no accesibles.

## Archivos

| Archivo | Qué tiene |
|---|---|
| `ruta_viva.py` | Todo el modelo: lugares, tramos, recorrido, criterio y `planificar` |
| `test_ruta_viva.py` | Los tests |
| `armar_recorrido.py` | Armás un recorrido por Montevideo desde la terminal |
| `DISENO.md` | Variante, UML, decisiones y alternativas descartadas |
| `ETICA.md` | Datos, riesgo y mitigación, marco legal y licencia, uso de IA |
| `BITACORA_IA.md` | Cada uso de IA, qué devolvió y qué se corrigió |
| `PREDICCIONES.md` | Predicciones anotadas antes de ejecutar, comparadas con el resultado |

## Cómo correrlo

```bash
python3 -m venv .venv
.venv/bin/pip install pytest
.venv/bin/python3 armar_recorrido.py
.venv/bin/pytest -v
```

El programa solo usa la librería estándar. `pytest` se usa únicamente para los tests.

Coordenadas de `armar_recorrido.py`: © OpenStreetMap contributors, licencia ODbL. La
accesibilidad, los horarios y los costos son datos de ejemplo, no información real.
