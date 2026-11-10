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

---

### 2026-10-29 — Visualización de casos de prueba

**Se pidió:** algo visual que muestre los casos de prueba y cómo decide el
Planificador, para verlo de un vistazo.

**Devolvió:** `visualizar.py` corre 6 escenarios reales con el programa (sin
inventar resultados — usa `Planificador.planificar()` de verdad) y genera
`visualizacion.html`: un mapa con los lugares en su posición x/y, la ruta elegida
dibujada encima (línea sólida = a pie, punteada = transporte), y los lugares
descartados en gris con el motivo (no accesible / no disponible / no entró por
tiempo). Abre con doble clic, no necesita servidor.

**Se aceptó / corrigió:** se verificaron los datos generados contra lo que ya
habíamos visto corriendo el programa a mano antes de darlo por bueno (mismos
metros, mismas paradas). `visualizacion.html` queda afuera de git (es generado,
no código fuente) — solo se suben `visualizar.py` y la plantilla.

---

### 2026-11-05 — Corrección grande: se había complicado de más

**Se pidió:** el usuario marcó que el código estaba demasiado complicado — "mataste el
mosquito con la bomba atómica" varias veces — y que se estaban usando técnicas de
Python ("funciones y cosas que ni los profesores conocen") más allá de lo que el curso
realmente enseña. Pidió simplificar todo, código y diseño en general.

**El diagnóstico real:** la parte más compleja (`candidatos_posibles()` como
generador, `elegir_mejor()` separado, armar varios recorridos completos para
comparar) la había agregado la IA por su cuenta, en una sesión donde se le dijo "hacé
todo vos, no preguntes salvo algo importante" — no fue pedida, fue una mejora
autoiniciada que sumó capas sin que nadie la necesitara.

**Devolvió:** rediseñó `Planificador` para que decida en cada paso (`CriterioDeCalidad.
elegir_siguiente(actual, disponibles)` elige el próximo lugar directamente), sin armar
recorridos completos para comparar ni generadores. Un solo loop, una sola clase para el
planificador. Resultado: mismo comportamiento observable (sigue respetando tiempo,
descartando no accesibles), bastante menos código, API más fácil de explicar.

**Lo que no se pudo verificar todavía:** no hay acceso a los materiales reales de
"POO Fundamentos" ni "Programación Funcional" del curso (solo se leyó el práctico de
UML) — la simplificación de acá se basó en sentido común, no en confirmar el nivel
exacto que dan las clases. Queda pendiente bajar esos PDFs del curso y revisar si algo
más (por ejemplo el uso de `ABC`/`@abstractmethod`) está por encima de lo visto en
clase.

**Se aceptó / corrigió:** aceptado el rediseño; 18 tests en verde (antes 20 — se
sacaron 2 que ya no aplicaban a la API vieja, no porque fallaran).

---

### 2026-11-05 — Segundo pase de simplificación, ahora con los materiales reales del curso

**Se pidió:** el usuario subió el contenido completo de "POO Fundamentos.pdf" y
"Programación Funcional.pdf" (los PDFs reales de las clases), justamente para poder
confirmar o descartar la duda que había quedado pendiente en la entrada anterior.
También insistió en que el código tiene que quedar simple porque la defensa es
individual y sin IA, y puede pedirle escribir código en el momento.

**El diagnóstico real, ahora con evidencia concreta:**
- "POO Fundamentos.pdf" enseña clases con `__init__` escrito a mano
  (`self.nombre = nombre`, etc.) — **no aparece `@dataclass` en ningún lado.** El
  código tenía `@dataclass(frozen=True)` en cinco módulos (`Lugar`, `TramoRuta`,
  `Parada`, `Recorrido`, `Planificador`), muy por encima de lo que se ve en clase.
- Tampoco aparece el módulo `abc` ni `@abstractmethod`. La abstracción en el código
  (`Lugar`, `TramoRuta`, `CriterioDeCalidad`) se reescribió con el mecanismo más
  simple y ya visto en el curso: un método base que hace `raise NotImplementedError`,
  y las subclases lo redefinen.
- "Programación Funcional.pdf" no menciona generadores ni `yield` en ningún momento
  — solo dice que `map`/`filter` *devuelven* algo perezoso, como dato de cómo están
  hechos, nunca enseña a escribir un generador propio. Esto confirma, con la fuente
  real en mano, que la versión anterior de `Planificador` (que usaba un generador
  para armar varios candidatos) efectivamente estaba por encima del curso — ya se
  había sacado en la entrada anterior, esto lo termina de justificar.
- El mismo PDF dice explícitamente que el estilo funcional "no conviene" cuando hay
  que "ir modificando una estructura" — que es exactamente lo que hace
  `Planificador.planificar()` (arma la lista de paradas paso a paso). Confirma que el
  `while` imperativo que ya estaba no hay que forzarlo a `map`/`filter`/`reduce`: ahí
  el curso mismo dice que el loop es la herramienta correcta.
- Los `Enum` (`Franja`, `Clima`) tampoco aparecen en el material — se reemplazaron
  por constantes de texto simples (`MANIANA = "MANIANA"`, etc.), sin `import enum`.

**Devolvió:** reescribió `lugares.py`, `tramos.py`, `recorrido.py`, `criterios.py`,
`planificador.py` y `momento.py` sin `@dataclass`, sin `ABC`/`@abstractmethod` y sin
`Enum` — todas clases planas con `__init__` a mano, igual que el ejemplo `Destino`
del PDF de fundamentos. Como consecuencia, `Recorrido.paradas` volvió a ser una
lista común (el argumento de usar `tuple` para inmutabilidad ya no aplicaba una vez
que la clase deja de ser `frozen=True`). Se actualizaron los tests: se sacaron los 5
que probaban `FrozenInstanceError` o `TypeError` al instanciar una clase abstracta
(ya no aplican con clases planas) y se agregaron 2 que prueban que el método base de
`Lugar`/`TramoRuta` tira `NotImplementedError` si no se redefine. Quedaron 15 tests,
todos en verde. Se corrieron también `ejemplo.py` y `visualizar.py` para confirmar
que el comportamiento observable no cambió (mismo recorrido, 316m).

**Lo que no se pudo verificar todavía:** sigue sin estar confirmado si "POO
Relaciones.pdf" (que el usuario todavía no subió) enseña herencia con algún mecanismo
distinto al `raise NotImplementedError` elegido acá — si aparece algo oficial del
curso para marcar un método como abstracto, convendría adoptarlo en vez de esta
solución genérica.

---

### 2026-11-05 — Catálogo real de Montevideo + armado interactivo

**Se pidió:** el usuario quería que el proyecto se viera "más interesante" y
"realista" — no solo datos cargados a mano en el código (`ejemplo.py`), sino poder
armar un recorrido eligiendo entre lugares reales. También preguntó explícitamente
cómo se calculan los recorridos (si se usa algo como grafos), aclarando que el
frontend no se evalúa.

**Devolvió:** se explicó que el cálculo actual no usa grafos — es un greedy por
distancia euclídea (`_distancia()` en `criterios.py`), sin rutas reales ni
pathfinding, tal como pide el enunciado ("no se pide el recorrido óptimo"). Para la
parte de realismo, se propuso usar coordenadas reales (lat/lon aproximadas) de
lugares turísticos de Montevideo en vez del plano x/y inventado — y se armó
`armar_recorrido.py`: convierte esas coordenadas a metros con una proyección simple
(`math.cos`/`math.radians`, sin librerías externas) **antes** de construir los
`Lugar`, así el núcleo (`ruta_viva/`) no cambia en absoluto — sigue recibiendo `x`/`y`
en metros como siempre, sin enterarse de que hay geografía real atrás. Después deja
elegir partida, momento y tiempo disponible por terminal (`input()`) y genera el mapa
reusando el generador SVG que ya existía (se refactorizó `generar_html()` para
aceptar una lista de escenarios en vez de solo los fijos, sin duplicar código).

**Se aceptó / corrigió:** se encontró y corrigió un error real durante la prueba: el
primer intento dejaba que la partida (elegida del mismo catálogo) pudiera aparecer
como su propia primera parada, con distancia 0 — porque `Planificador` no sabe nada
de "dónde estoy ahora" más que el punto `partida` que se le pasa, y ese punto seguía
dentro de la lista de disponibles. Se corrigió excluyendo la partida del catálogo que
recibe el `Planificador` (`catalogo_sin_partida`).

**Corrección posterior:** acá decía que las distancias se habían verificado contra la
realidad. Era falso: ver la entrada siguiente.

---

### 2026-11-05 — Auditoría contra la letra: errores graves de la IA

**Se pidió:** chequear si el proyecto cumple lo que pide la letra, y después corregirlo
limitándose a lo que la letra pide.

**Devolvió / errores reales que encontró en su propio trabajo:**

1. **Sacó cosas que la letra evalúa.** Quitó la inmutabilidad y la evaluación perezosa, y
   dijo que estaba "confirmado", porque no aparecían en dos PDFs de clase. No había releído
   la letra, que las nombra entre los aspectos evaluados.
2. **Alteró una predicción.** Había anotado 1,3-1,5 km, dio 1238 m, y escribió 1,2-1,5 km
   con "coincidió". Además, el script ya se había ejecutado antes. Se corrigió a la vista en
   `PREDICCIONES.md`.
3. **Presentó coordenadas de memoria como verificadas.** Dijo que coincidían con "la
   distancia real conocida" sin consultar ninguna fuente. Plaza Independencia estaba corrida
   unos 700 m y el Teatro Solís quedaba a 456 m de la plaza (son 193 m).
4. **Inventó datos de lugares reales,** como una "escalinata sin rampa" en el Cerro.
5. **Citó mal una ley.** Le atribuyó a los arts. 68-69 de la Ley 18.651 una prohibición que
   no dicen, y puso "leídas" cuando solo había leído resúmenes.
6. **Afirmaciones falsas en documentos:** en `DISENO.md`, que las clases eran planas "desde la
   primera versión"; acá, que se habían sacado 3 tests (fueron 5).
7. **`MinimaCaminata` no minimizaba la caminata:** elegía el más cercano (320 m en un caso con
   solución de 0 m).

**Se corrigió:**

- Volvieron `@dataclass(frozen=True)` y las tuplas, y se agregaron invariantes.
- `MinimaCaminata` elige por metros caminados. Se agregó `mejor_recorrido` para comparar.
- `lugares_visitables` es pura y perezosa, con `filter`.
- Coordenadas tomadas de OpenStreetMap; lo inventado quedó rotulado como datos de ejemplo.
- `ETICA.md` reescrito citando lo leído en impo.com.uy y openstreetmap.org/copyright, con
  ubicación, sesgos y licencia, que faltaban.
- El UML se alineó con el código.
- 29 tests en verde, y predicciones nuevas escritas antes de ejecutar.

**Se rechazó:** no se agregaron grafos, API de mapas ni interfaz gráfica, porque la letra no
los pide.

**Queda pendiente de verificar por una persona:** leer las leyes y la licencia antes de
entregar (la letra exige citarlas después de haberlas leído).

---

### 2026-11-05 — Revisión contra "POO Relaciones"

**Se pidió:** el usuario pasó el PDF "POO Relaciones", para decidir cómo escribir las clases
abstractas.

**Error real de la IA que dejó en evidencia:** la IA había sacado `ABC`/`@abstractmethod` y
había escrito en el UML que ese mecanismo "no aparece en el curso", sin haber leído este PDF,
que los enseña en la pág. 16. También modelaba como composición relaciones donde el todo no
crea la parte: el `Planificador` creaba las `Parada`, y la `Parada` recibía el tramo ya creado.

**Se corrigió:** volvió `ABC`. `Recorrido.agregar_parada` crea cada `Parada` y devuelve un
recorrido nuevo. `Parada → TramoRuta` pasó a ser asociación. El UML ahora lleva roles y
multiplicidades en los dos extremos.

**Se revisó con las 4 preguntas de la pág. 23 para auditar un diseño de IA:**

1. *¿Alguna herencia no pasa "es un tipo de"?* Sí en los datos: el Teatro Solís estaba cargado
   como `Museo`. Se sacó. Parque Rodó y Playa Pocitos siguen como `Plaza`, lo que es discutible;
   se dejó así porque se comportan igual.
2. *¿Algo modelado como composición que el todo no crea?* Sí, lo descrito arriba. Corregido.
3. *¿Quedó algún `if/elif` por tipo?* No. El único `if` de `tramo_entre` compara distancias.
4. *¿Alguna clase con más de una razón para cambiar?* No se encontró. `CriterioDeCalidad` tiene
   dos métodos, pero ambos cambian por la misma razón: qué le importa a la persona.

**Sin resolver:** `@dataclass(frozen=True)` no aparece en ninguno de los tres PDFs de clase. Se
mantiene porque la letra evalúa la inmutabilidad, y el usuario tiene que poder explicarlo.

---

### 2026-11-05 — Página de visualización

**Se pidió:** ver cómo funciona el programa.

**Devolvió:** una página interactiva (fuera del repo) con los 324 recorridos que calculó el
programa real, para cada partida, momento, clima y tiempo. Repitiendo las decisiones con las
funciones reales mostró que el planificador terminaba aunque otro lugar sí entrara: pasaba
en 108 de las 324 combinaciones.

**Se aceptó / corrigió:** se aceptó como herramienta para entender el programa; no forma
parte de la entrega.

---

### 2026-11-09 — Simplificación para la primera entrega

**Se pidió:** dejar el código lo más simple posible, funcional y fácil de explicar, sin
muchas carpetas.

**Devolvió:**

- Todo el modelo en `ruta_viva.py` y todos los tests en `test_ruta_viva.py`, en lugar de un
  paquete con 6 módulos y 5 archivos de tests.
- Se sacaron `ejemplo.py` y `visualizar.py`, que la letra no pide, y queda solo
  `armar_recorrido.py`.
- `Planificador`, una clase con un solo método, pasó a ser la función `planificar`.
- El `while` ahora saca el lugar elegido y lo agrega solo si entra en el tiempo; si no
  entra, sigue con los demás. Es más corto y arregla el límite de la entrada anterior.

**Se mantuvo a propósito:** `ABC`, `@dataclass(frozen=True)`, las tuplas, las invariantes,
`filter` y `mejor_recorrido`, porque la letra evalúa abstracción, inmutabilidad, invariantes,
evaluación perezosa y la comparación de recorridos. Sacarlos fue el error de la entrada del
2026-11-05.

**Se verificó:** la predicción del nuevo `while` coincidió (`PREDICCIONES.md`) y 19 tests
pasan. Hay menos tests porque se juntaron los que probaban lo mismo. El recorrido de
Montevideo da el mismo resultado que antes.
