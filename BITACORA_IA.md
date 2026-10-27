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
