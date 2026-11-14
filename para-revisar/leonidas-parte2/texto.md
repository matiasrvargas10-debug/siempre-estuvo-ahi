# Leónidas · parte 2

**Formato:** Reel 9:16 · 31,7 s · voz "Narrador siempre" + música propia al ~18 %, ya mezclado (en Instagram NO añadir música).

**Cuándo:** martes 17/11 por la tarde.

## Guion (voz)

Esta noche, la Tierra cruza el polvo del cometa. Desde Mataró, el máximo llega a la una menos cuarto. Mira al este, sobre el mar, hacia Leo. Sale bajo: cuanto más tarde, mejor. Hasta quince por hora, a setenta y un kilómetros por segundo: las más rápidas del año. Lejos de las luces, y deja que tus ojos se acostumbren. ¿Y si hay nubes? El veinticuatro llega la superluna. Síguenos para no perdértela.

## Texto (pie)

Esta noche llegan las Leónidas, las estrellas fugaces más rápidas del año.
Máximo a las 00:45: mira al este, sobre el mar. Leo sale bajo, así que de madrugada se ven más.
La luna se pone a las 00:36 y deja el cielo oscuro.
¿Vas a salir a verlas? SÍ o NO

#mataro #maresme #barcelona #leonidas #estrellasfugaces

📍 Mataró

## Hueco AEMET (el martes)

El vídeo lleva un recuadro "Previsión AEMET · martes 17" con un hueco. El martes se vuelve a generar con el dato:

```
cd scripts/leonidas_p2
python3 leonidas_p2.py --nubes "Despejado hasta las 3; nubes altas al amanecer"
```

## Datos calculados (ephem, Mataró 41.5381 N, 2.4447 E)

- Puesta de la luna: 00:36 del 18/11 (cuarto creciente el 17/11 a las 12:48).
- Radiante de Leo (AR 10h08, Dec +22°): 00:45 → 10° de altura, acimut 69° (este-noreste, sobre el mar). 03:00 → 34° (este), 05:00 → 56° (este-sureste).
- Amanecer 18/11: 07:42.
- Luna llena 24/11 a las 15:53, a 360.765 km.
- Ojo: con Leo a 10° se ven pocas (la tasa baja mucho con el radiante bajo). Por eso el guion dice "cuanto más tarde, mejor".

## Notas de montaje

- La parte 1 usaba lluvia desde un radiante a pantalla completa. Esta usa el cielo real desde Mataró mirando al este (estrellas y Leo calculados con ephem); los meteoros salen de Leo, pero es otro plano.
- Reloj 21:00 → 00:45, brújula al este, Leo subiendo hora a hora, barras 0,34 / 7,7 / 71 km/s, nubes, superluna.
