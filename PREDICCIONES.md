# Predicciones

Antes de correr una función clave por primera vez: anotar acá qué se espera que
devuelva, y recién después ejecutarla. Después se compara con lo que pasó de verdad.

Formato por entrada:

```
## nombre_de_la_funcion(argumentos)

**Predicción:** qué creo que va a devolver, y por qué.

**Resultado real:** qué devolvió.

**¿Coincidió?:** sí / no — si no, por qué estaba mal la predicción.
```

## armar_candidato(partida=(0,0), 10 lugares cada 200m en línea, tiempo_disponible_min=60)

**Predicción:** el greedy va a lugar más cercano cada vez. Partida→Lugar1 (200m, tramo a
pie porque ≤400, dura round(200/70)=3 + 20 de visita = 23 min). Lugar1→Lugar2 (200m,
otros 23 min) → acumulado 46. Lugar2→Lugar3 (200m más, otros 23 min) → se pasaría a 69,
más que 60. Espero que entren **2 paradas**, con 46 minutos usados.

**Resultado real:** 2 paradas (Lugar 1, Lugar 2), 46 minutos usados.

**¿Coincidió?:** Sí, exacto.

---

## Planificador.planificar(partida=(0,0)) con A=(300,0), B=(900,0), C=(920,0)

**Predicción:** el candidato ingenuo (arranca por el más cercano a la partida, que es A)
va a caminar mucho: partida→A son 300m a pie, A→B son 600m en transporte (0m caminados),
B→C son 20m a pie. Total: 320m caminados. Si en cambio se arranca por B o por C, el
tramo largo (partida→B o partida→C, ~900m) se hace en transporte una sola vez, y B↔C↔A
quedan casi todos a pie y cortos. Espero que arrancar por B dé bastante menos de 320m
caminados — una diferencia grande, no un par de metros.

**Resultado real:** ingenuo (arranca por A): 320m. Mejor candidato (arranca por B):
**20m**.

**¿Coincidió?:** Sí, y la diferencia fue más grande de lo que esperaba (320m → 20m, no
"bastante menos" sino 16 veces menos) — confirma que explorar varios candidatos no es
una complicación cosmética, cambia el resultado de verdad.

**Nota (2026-11-05):** esta versión de "explorar varios candidatos" se sacó después
por ser más complicada de lo necesario (ver `BITACORA_IA.md`). Con el diseño actual,
este mismo escenario daría 320m siempre (el criterio decide paso a paso, no compara
recorridos completos) — queda la predicción de entonces como historial, no como el
comportamiento de hoy.

---

## _a_metros(lat, lon) en armar_recorrido.py — Plaza Independencia → Mercado del Puerto

**Predicción:** ~1,3 a 1,5 km (anotada antes de esta medición, sin una fuente real).

**Resultado real:** 1238 m.

**¿Coincidió?:** No, quedó afuera del rango.

**Corrección (2026-11-05):** esta entrada se había registrado mal. La IA amplió el rango
a "1,2 a 1,5 km" después de ver el resultado y puso que coincidía; además, el script ya
se había ejecutado antes de anotar la predicción. Las coordenadas usadas también estaban
mal (salían de la memoria de la IA), así que los 1238 m no prueban nada. Ver
`BITACORA_IA.md`. La medición con coordenadas verificadas está más abajo.

---

## MinimaCaminata con partida=(0,0), A=(300,0), B=(900,0), C=(920,0)

**Predicción (antes de ejecutar):** el criterio nuevo elige por metros caminados del
tramo y desempata por distancia. Desde la partida: A cuesta 300 m a pie, B y C cuestan
0 m (más de 400 m, van en transporte), gana B por estar más cerca. Desde B: C cuesta 20 m
a pie, A cuesta 0 m (600 m, en transporte), gana A. Desde A: C está a 620 m, en
transporte. Espero el orden **B, A, C** con **0 m caminados**.

**Resultado real:** `['B', 'A', 'C']`, 0 m.

**¿Coincidió?:** Sí.

---

## lugares_visitables(catalogo, momento)

**Predicción (antes de ejecutar):** usa `filter`, que es perezoso. Si un lugar lanza un
error dentro de `esta_disponible`, espero que **llamar a la función no falle**, y que el
error aparezca recién al recorrer el resultado (por ejemplo con `list(...)`).

**Resultado real:** la llamada devolvió un objeto `filter` sin fallar; el `RuntimeError`
apareció recién en `list(...)`.

**¿Coincidió?:** Sí.

---

## _a_metros con coordenadas de OpenStreetMap: Plaza Independencia → Mercado del Puerto

**Predicción (antes de ejecutar):** cuenta a mano. Diferencia de latitud 0,000826° ≈ 92 m.
Diferencia de longitud 0,011985° × cos(34,9°) (≈ 0,82) × 111.195 m/° ≈ 1093 m. Combinando
ambas espero **unos 1100 m** (entre 1050 y 1150 m).

**Resultado real:** 1097 m.

**¿Coincidió?:** Sí. Es distancia en línea recta, no el camino real por las calles.

---

## Lugar(...) con ABC y @abstractmethod

**Predicción (antes de ejecutar):** crear un `Lugar` directamente tiene que lanzar
`TypeError` en el momento de crearlo, no recién al llamar a `esta_disponible`. Crear una
`Plaza` tiene que seguir funcionando.

**Resultado real:** `TypeError: Can't instantiate abstract class Lugar...`, y la `Plaza` se
creó bien.

**¿Coincidió?:** Sí.

---

## Recorrido(momento).agregar_parada(lugar, tramo)

**Predicción (antes de ejecutar):** devuelve un recorrido nuevo con 1 parada y el original
sigue con 0. Con un `TramoAPie` de 100 m, el nuevo da 100 m caminados y el original 0.

**Resultado real:** original: 0 paradas, 0 m. Nuevo: 1 parada, 100 m.

**¿Coincidió?:** Sí.

---

## planificar(...) cuando el lugar elegido no entra

**Predicción (antes de ejecutar):** partida en (0,0), lugar A a 900 m con 100 min de visita
y lugar B a 100 m con 10 min de visita, 30 min disponibles. El criterio elige primero A
(0 m a pie, va en transporte), pero necesita 3 + 100 min y no entra. Antes el planificador
terminaba ahí con 0 paradas. Ahora debería descartar A, seguir con B (1 min de viaje +
10 de visita) y devolver **una sola parada: B**.

**Resultado real:** `['B']`, 11 min.

**¿Coincidió?:** Sí.
