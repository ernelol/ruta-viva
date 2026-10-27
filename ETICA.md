# Ética — Ruta viva

## Datos que maneja la aplicación

- **Datos del catálogo:** nombre, ubicación (en un plano inventado, nunca coordenadas
  GPS reales), horarios, costo y accesibilidad de cada lugar. No identifican a ninguna
  persona.
- **Datos del visitante:** punto de partida, tiempo disponible, y si necesita transporte
  accesible. Son parámetros de una sola corrida — no se guardan en ningún archivo ni se
  asocian a una identidad. A diferencia de una app de turismo real, acá no hay cuenta de
  usuario, ni historial, ni ubicación real del dispositivo: eso fue una decisión de
  diseño, no una casualidad (ver restricción del enunciado de no depender de la
  ubicación real de la máquina).

## Riesgo ético concreto y cómo lo mitiga el diseño

**El riesgo:** que el sistema le diga a alguien con movilidad reducida que un lugar está
disponible cuando en realidad no es accesible de verdad (una rampa rota, una escalera no
declarada). Para esta variante eso no es un detalle — es el riesgo central: una
recomendación que falla justo en lo que el usuario más necesita que sea confiable.

**La mitigación de diseño:** `es_accesible` en `Lugar` es un **filtro duro**, no un
factor más que se pondera junto a otros. Un lugar marcado como no accesible queda
completamente afuera del recorrido — no se le resta puntaje y se lo deja competir
igual, se lo excluye antes de puntuar nada (`_lugares_disponibles()` en
`planificador.py`). La razón: para esta variante, "inaccesible" no es un defecto menor
compensable con otras cualidades (buena ubicación, bajo costo) — es una razón de
exclusión total.

Esto también marca el límite honesto del sistema: el programa es tan confiable como el
dato `es_accesible` que alguien cargó en el catálogo. Si ese dato está mal cargado (un
lugar que dice ser accesible y no lo es), el programa no tiene forma de detectarlo por
sí solo. Es una limitación real del diseño, no algo para esconder.

## Marco legal

Leídas para este proyecto (no citadas de memoria):

- **Ley Nº 18.651 (2010), Protección Integral de Personas con Discapacidad** —
  arts. 68 y 69 establecen como prioridad la supresión de barreras físicas aplicando
  normas técnicas UNIT de accesibilidad, y prohíben que centros recreativos, educativos
  o culturales discriminen el acceso a sus instalaciones. Es la razón de fondo por la
  que `es_accesible` se trata como un filtro excluyente y no como un detalle
  secundario del modelo: la ley ya lo trata como no negociable, el programa sigue esa
  misma lógica.
- **Ley Nº 18.331 (2008), Protección de Datos Personales** — regula la recolección,
  tratamiento y transferencia de datos personales en Uruguay, bajo principios de
  legalidad, finalidad y consentimiento informado, con la URCDP como órgano de
  control. Hoy esta aplicación no recolecta datos personales reales (ver sección
  anterior), así que no está sujeta a esta ley en su forma actual — pero si una
  versión futura guardara preferencias de un visitante identificado, aplicaría
  directo, y el diseño actual (nada persiste, nada identifica) ya deja el terreno
  preparado para eso.

## Uso de IA

Ver `BITACORA_IA.md` para el detalle de cada interacción. En resumen: se usó IA para
proponer la estructura de clases, el código del núcleo y los tests, y para investigar
el marco legal de esta sección — siempre revisando y corrigiendo lo que devolvió antes
de aceptarlo (incluye al menos un error real detectado y corregido, documentado en la
bitácora).
