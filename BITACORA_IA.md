# Bitácora de IA

Cada entrada: qué se pidió, qué devolvió, qué se corrigió o rechazó y por qué. Tiene que
quedar al menos un error real de la IA, no inventado para cumplir el requisito.

---

### 2026-10-27 — Elegir proyecto y variante

**Se pidió:** comparar los 3 proyectos (Ruta viva, Mercado de cartas, Radio infinita) y
recomendar uno, sabiendo que el trabajo lo hace una sola persona.

**Devolvió:** recomendación de Ruta viva, razonando que Mercado de cartas tiene más
partes moviéndose a la vez (pensado para repartir en equipo) y que Radio infinita exige
dominar generadores/evaluación perezosa a fondo para poder defenderlo en vivo sin ayuda.
También propuso la variante (persona con movilidad reducida / transporte combinado /
mínima caminata), conectándola con el riesgo ético que ya sugiere el propio enunciado.

**Se aceptó / corrigió:** se aceptó tal cual — todavía no hay código para encontrar un
error real; se va a completar esta bitácora a medida que avance el proyecto.

---

### 2026-10-27 — Primera propuesta de clases (Hito 1)

**Se pidió:** después de leer el práctico de UML del curso (notación y los dos
ejercicios resueltos), proponer las clases de Ruta viva con la variante ya elegida.

**Devolvió:** `Lugar` (abstracta, 4 subtipos), `Momento` inmutable inyectado,
`TramoRuta` (a pie / en transporte, jerarquía separada de `Lugar`), `Parada` (asociación
con Lugar, composición con TramoRuta), `Recorrido` (compone Paradas), `CriterioDeCalidad`
como Estrategia, y `Planificador`. Decidió por su cuenta no modelar `Visitante` como
clase (sino como parámetros de `Planificador`), razonando que la variante es fija.

**Se aceptó / corrigió:** pendiente de revisar en conjunto — queda abierto si
`Visitante` como clase aparte conviene más de cara al cambio de requisito del Hito 2
(todavía no asignado).

---

### 2026-10-27 — Quinto tipo de lugar, a pedido de "hacelo diferente"

**Se pidió:** confirmados los 4 tipos de lugar, pero con la consigna de pensar qué
haría el diseño distinto al de otros grupos, no solo técnicamente correcto.

**Devolvió:** agregar `ParadaDeDescanso` como quinto subtipo de `Lugar` — sin atractivo
turístico, siempre disponible, pensado explícitamente para la variante de movilidad
reducida. Razonó que un tipo de lugar ligado directamente a la variante pesa más que
variar nombres de categorías genéricas (museo/plaza/mirador/restaurante, que cualquier
grupo pondría igual).

**Se aceptó / corrigió:** aceptado.

---

### 2026-10-27 — Hito 2: código del núcleo + primeros tests

**Se pidió:** implementar las clases del diseño (`Lugar` y sus 5 subtipos, `Momento`,
`TramoRuta`, `Recorrido`, `CriterioDeCalidad`, `Planificador`) solo con librería estándar,
más tests de pytest para cada módulo.

**Devolvió:** el paquete `ruta_viva/` completo y 14 tests, todos verdes.

**Error real encontrado:** al escribir `Planificador`, la IA declaró
`catalogo: list[Lugar]` dentro de un `@dataclass(frozen=True)`. Esto es inconsistente
con el propio argumento de inmutabilidad que la IA había escrito para `Recorrido.paradas`
(ahí sí usó `tuple`, explicando que una lista en un dataclass frozen igual se puede mutar
con `.append()` por dentro). Se dio cuenta ella misma al releer el archivo, sin que se le
señalara, y lo corrigió a `tuple[Lugar, ...]` antes de correr los tests. Queda como
ejemplo real de que hay que revisar la consistencia de lo que la IA genera, no solo que
compile.

**Se aceptó / corrigió:** aceptado el código final (ya con la corrección), tests
corridos y en verde (`.venv/bin/pytest`, 14 passed).

---

### 2026-10-27 — ETICA.md: buscar el marco legal real

**Se pidió:** buscar y leer la Ley 18.331 (datos personales) y una ley de
accesibilidad de Uruguay antes de citarlas en `ETICA.md`, en vez de citarlas de
memoria.

**Devolvió:** resumen de la Ley 18.331 (principios, URCDP como órgano de control) y de
la Ley 18.651 de protección integral de personas con discapacidad (arts. 68-69,
normas UNIT de accesibilidad) — ambas con fuentes. Con eso escribió `ETICA.md`
completo, conectando el art. 68-69 de la 18.651 con la decisión de diseño de que
`es_accesible` sea un filtro duro.

**Se aceptó / corrigió:** aceptado el contenido; falta que alguien del equipo (en este
caso, vos) lea el texto de las leyes citadas, no solo los resúmenes de la IA, antes de
dar esto por cerrado para la entrega final.

---

### 2026-10-27 — Planificador: de un candidato a varios, con evaluación perezosa

**Se pidió (trabajando de forma autónoma, sin frenar a preguntar salvo algo
importante):** revisar si faltaba algo del enunciado en el núcleo ya escrito.

**Devolvió:** notó que `Planificador` solo armaba un único candidato y que
`elegir_mejor()` nunca comparaba nada de verdad — y que no había ningún uso real de
evaluación perezosa, pese a que el enunciado la pide. Refactorizó a
`candidatos_posibles()` (un generador: un candidato por cada posible primer lugar) +
`elegir_mejor()` consumiéndolo con `max()`. Verificó con un catálogo de prueba que
explorar varios candidatos realmente encuentra menos caminata (320m → 20m) antes de
dar el cambio por bueno, y lo dejó como test (`test_explorar_varios_candidatos...`).

**Se aceptó / corrigió:** aceptado, con los 16 tests corridos y en verde después del
cambio (antes eran 14).

---

### 2026-10-29 — Simplificar: sacar código redundante

**Se pidió:** que todo el código (y el proyecto en general) sea lo más simple posible.

**Devolvió:** encontró que `armar_candidato()` había quedado sin uso real después del
cambio anterior (candidatos múltiples con `candidatos_posibles()`) — `Planificador.
planificar()` ya no la llamaba, solo dos tests. Dos funciones casi iguales conviviendo
no es simple, es confuso. La borró y reescribió esos tests contra `candidatos_posibles()`
directo, más uno nuevo que prueba la afirmación real ("empezar por un lugar u otro da
resultados distintos") sin depender del orden interno de iteración.

**Se aceptó / corrigió:** aceptado, 20 tests siguen en verde y `ejemplo.py` sigue dando
el mismo tipo de resultado.
