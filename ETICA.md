# Ética — Ruta viva

## 1. Datos que maneja la aplicación

- **Catálogo:** nombre, posición, horarios, costo y accesibilidad de cada lugar. No
  identifica a nadie. Las coordenadas de `armar_recorrido.py` son de OpenStreetMap; la
  accesibilidad, los horarios y los costos son datos de ejemplo, no información real.
- **Ubicación del visitante:** el punto de partida se elige de una lista. El programa no
  lee la ubicación de la computadora, no la guarda en ningún archivo y no la asocia con
  ninguna persona. No hay cuentas ni historial.

## 2. Riesgo ético y cambio de diseño que lo mitiga

**Riesgo principal: mandar a una persona con movilidad reducida a un lugar al que no puede
entrar.** Es la falla más grave para este visitante.

**Cambio de diseño:** `es_accesible` es un filtro duro. `lugares_visitables` saca esos
lugares antes de que el criterio elija, así que ningún otro atributo puede compensarlo.
**Límite:** el programa confía en el dato cargado y no puede detectar si está mal.

**Sesgos del recorrido:**

- **Personas que no pueden caminar mucho:** el criterio minimiza la caminata, pero el umbral
  de 400 m y el ritmo de 70 m/min son iguales para todos y son supuestos míos, no medidos.
  Para algunas personas 400 m ya es demasiado. Además, `es_accesible` es sí o no: no
  distingue, por ejemplo, entre una silla de ruedas y un bastón.
- **Comercios que pagan:** hoy ningún lugar tiene un dato de patrocinio y el criterio solo
  usa metros y distancia, así que nadie puede pagar para subir en el recorrido. El riesgo
  aparecería si se agregara. Como el criterio es explícito y está en un solo lugar, ese
  cambio se vería en el código. Sí hay un sesgo sin pago: el catálogo lo elige quien lo arma,
  y lo que no está cargado no se recomienda.

## 3. Marco legal y licencia

**Ley 18.331, Protección de Datos Personales.** Define dato personal como información
"referida a personas físicas o jurídicas determinadas o determinables" (art. 4 D) e
incluye como dato sensible la información "referente a la salud" (art. 4 E). Una ubicación
asociada a una persona sería dato personal, y saber que esa persona tiene movilidad reducida
podría revelar información de salud. Los datos sensibles requieren consentimiento expreso y
escrito (art. 18), y los datos no pueden usarse para otra finalidad (art. 8). Esta versión
no recolecta ni guarda esos datos. Una versión con usuarios reales tendría que cumplir con
estos artículos.

**Ley 18.651, Protección Integral de Personas con Discapacidad.** Los edificios con
concurrencia de público, las vías públicas, los parques y los jardines deben permitir que
todas las personas puedan "acceder, ingresar, usar y egresar" (art. 68), y las Intendencias
deben aplicar las normas técnicas de UNIT (art. 69). El art. 82 define las barreras en el
transporte, relevante para la regla de transporte combinado. Por eso la accesibilidad se
trata como requisito y no como preferencia.

**Licencia de los datos de mapas.** Las coordenadas de `armar_recorrido.py` se consultaron en
OpenStreetMap y se copiaron al código: © OpenStreetMap contributors. Los datos están bajo la
licencia Open Database License (ODbL), que permite copiarlos y adaptarlos si se da crédito a
OpenStreetMap y sus colaboradores y se aclara la licencia. Si se distribuye una base derivada,
debe ser bajo la misma licencia. El crédito aparece en el script y al ejecutarlo. No se usa
ningún mapa ni se descarga nada al ejecutar: solo esas coordenadas, copiadas.

Fuentes: textos de ambas leyes en impo.com.uy y openstreetmap.org/copyright.

## 4. Uso de IA

Se usó IA para proponer el diseño, escribir código y tests, y buscar el marco legal. El detalle
y los errores reales que se le corrigieron están en `BITACORA_IA.md`.
