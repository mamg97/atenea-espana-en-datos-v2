# Iteración UI v3 — 2 septiembre 2026

Esta iteración corrige exclusivamente presentación y comportamiento responsive de la página `finanzas-publicas` después de revisar la versión dev en Chrome.

## Cambios

- Fuerza `theme: light` en `finanzas-publicas.md`, igual que la página principal. Esto evita que Observable aplique el tema oscuro del sistema operativo a esta página.
- El Sankey deja de vivir dentro de una gran tarjeta blanca con una segunda columna reservada para el detalle.
- El gráfico ocupa el ancho completo disponible cuando no hay una selección activa.
- El panel de detalle se convierte en un drawer superpuesto desde la derecha. Abrirlo ya no comprime ni recoloca el Sankey.
- Se añade backdrop y cierre mediante clic fuera, botón `×` o tecla `Escape`.
- Se elimina la altura mínima fija del lienzo y se reduce el `viewBox` a la altura realmente utilizada por los nodos.
- La botonera se simplifica: ejercicio, metodología/fuentes, estado COFOG y descargas CSV/Excel.
- En móvil se conserva scroll horizontal controlado para mantener legibles las etiquetas.
- En impresión se ocultan controles y drawer para que el diagrama utilice todo el ancho.

## Datos

No se ha modificado el modelo de datos ni ninguna cifra. Los tests de reconciliación continúan superándose. Se mantienen los warnings ya conocidos de alquiler y unidad del PIB nominal.
