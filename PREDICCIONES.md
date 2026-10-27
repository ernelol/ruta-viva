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
