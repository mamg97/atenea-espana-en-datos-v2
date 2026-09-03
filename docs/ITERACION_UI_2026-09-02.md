# Iteración UI/UX - 2 septiembre 2026

Cambios aplicados después de revisar las exportaciones PDF de `España en Datos` y `Dinero público`.

## Navegación

- Desactivado globalmente el sidebar automático de Observable Framework.
- ATENEA utiliza una única navegación horizontal propia.
- La marca de la navegación pasa a ser `ATENEA · España en datos`.
- La página de Dinero público comparte la misma navegación que el dashboard.

## Mapa del dinero público

- El Sankey principal pasa de cuatro a tres columnas: `De dónde sale -> Fondo común -> En qué se gasta`.
- Los cortes analíticos, como Pensiones, ya no ocupan una cuarta columna; aparecen al pulsar la rama correspondiente en el panel de detalle.
- El SVG pasa de 1760 a 1320 unidades de ancho y se adapta al ancho disponible en escritorio.
- En pantallas estrechas se conserva scroll horizontal controlado para no hacer ilegibles las etiquetas.
- Se reduce el contenido introductorio antes del gráfico: título, explicación breve, cuatro cifras resumen y mapa.
- La explicación metodológica extensa queda debajo del gráfico en desplegables.
- Se añaden reglas de impresión para evitar recortes del Sankey en PDF.

## Dashboard principal

- Las dos tarjetas de alquiler con dimensión territorial ambigua se ocultan temporalmente; el dato no se inventa ni se elige arbitrariamente.
- Se mantienen las advertencias del validador para corregir la dimensión territorial en el data lake.
- Los rankings usan una comparación por puestos. Por ejemplo, `#15 -> #12` se muestra como `▲ 3 puestos`, no como una variación porcentual.
- Se añaden reglas de impresión para evitar tarjetas KPI partidas entre páginas.

## Validación

Ejecutado con `ATENEA_DATA_MODE=seed`:

- 99 filas en `fact_finanzas_publicas`.
- 8 fuentes.
- 24 figuras tributarias temporales.
- 603 observaciones KPI.
- Reconciliaciones financieras bloqueantes: OK.
- Se mantienen como warnings conocidos la dimensión territorial del alquiler y la unidad del PIB nominal.
