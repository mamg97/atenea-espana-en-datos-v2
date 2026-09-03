# Iteración UI v4 — Sankey full-width

## Problema
El componente se insertaba como expresión Markdown (`${explorer}`), por lo que Observable podía mantenerlo dentro del ancho de lectura de un bloque de prosa. El SVG tenía `width:100%`, pero ese 100% correspondía al contenedor estrecho, no a la página.

## Corrección
- host HTML explícito `.pf-explorer-host` a ancho completo;
- página de finanzas con ancho fluido hasta 1680 px;
- componente, layout, chart y SVG sin `max-width`;
- tablet escala el Sankey al ancho disponible;
- móvil conserva el gráfico completo con desplazamiento horizontal solo cuando la anchura no permite etiquetas legibles.

No se modifican datos ni reconciliaciones.
