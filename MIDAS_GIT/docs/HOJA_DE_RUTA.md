# Consolidación propuesta

## Decisiones iniciales

Mantener originales y usar una nueva estructura como destino. Adoptar provisionalmente el motor de cartera genético como línea principal; conservar LightGBM y R como líneas comparables hasta disponer de evaluaciones homogéneas. Mantener Markowitz en portfolio, separado de estrategias. No copiar los 600 MB de gráficos ni los modelos al nuevo núcleo.

| Destino | Responsabilidad / procedencia |
| --- | --- |
| src/midas/data | Descarga, calendario, divisas, snapshots y validación OHLCV |
| src/midas/features | Indicadores compartidos con contratos temporales |
| src/midas/strategies | Interfaces separadas genetic y lightgbm; sin persistencia ni notificaciones |
| src/midas/backtesting | Motor común, costes, fills, métricas, IS/validación/test |
| src/midas/portfolio | Asignación Markowitz y límites; diario simulado separado de posiciones reales |
| src/midas/reporting | Informes y notificación optativa |
| config | Fechas, semillas, universo, divisa base y rutas |
| tests | Casos deterministas pequeños sin red |
| research | Índice de experimentos y referencias a R/TFG/TFM, sin duplicar todos los originales |
| artifacts | Destino excluido de nuevos modelos/resultados, con manifiestos ligeros versionables |

## P0 — Identidad y conservación

Documentar el remoto deseado de un MIDAS independiente en la cuenta mamg97. Verificar referencias y estado antes de cualquier publicación. Preparar respaldo verificable del repositorio compartido y del diario de cartera antes de migrar; no se ha creado aún. La migración puede ser aditiva sin reescribir la historia compartida. Cualquier eliminación o reescritura exige aprobación explícita. Criterio de cierre: correspondencia verificable origen→destino y respaldo restaurable.

## P1 — Ejecución segura y portable

Extraer configuración, eliminar trabajo al importar, introducir modo offline/simulación y desactivar notificaciones por defecto. Centralizar aceptación del ganador para impedir que un resultado rechazado actualice el diario. Usar parada ante error en el pipeline. Reparar contrato train/inference, columnas de v3 y manifiestos antes de elegir una versión. No promover v3 por nombre. Criterio: ejecución con fixture pequeño sin red ni modificación de originales, y rechazo probado de modelos incompatibles.

## P2 — Reproducibilidad

Elegir y probar una versión Python y fijar dependencias completas; no inventar un lock sin resolverlo. Registrar hash de datos, intervalo, proveedor, zona horaria, ajustes, universo, moneda, commit, configuración y semillas. Validar los datos locales ya encontrados del pipeline histórico y documentar cómo restaurarlos; si no bastan, declarar los límites de reproducibilidad. Registrar procedencia del modelo sin cargar pickle desconocidos. Criterio: dos ejecuciones sobre el mismo snapshot reproducen señales y métricas dentro de tolerancias documentadas.

## P3 — Evaluación temporal común

Crear train→validación→test cronológicos y walk-forward; el OOS utilizado para elegir candidatos cuenta como validación. Introducir separación acorde al horizonte de etiquetas y reservar test final. Probar invariancia de señales pasadas frente a cambios en datos futuros; fills al momento ejecutable, gaps, comisiones y slippage; contabilidad y rechazo del ganador. Comparar con buy-and-hold y una regla sencilla bajo idénticos datos/costes. Revisar supervivencia del universo S&P500. Criterio: reporte fuera de muestra con retorno, drawdown, rotación, costes y supuestos, sin selección sobre el test.

## P4 — Asignación e integración

Conectar señales con asignación solo tras estabilizar contratos. Normalizar divisas/unidades, comparar covarianza muestral con estimación regularizada y limitar concentración. Separar diario simulado de cartera real y probar reconciliación. Criterio: pesos válidos, exposición y cash consistentes, benchmark homogéneo y un informe trazable.

## P5 — Artefactos y mantenimiento

Elegir almacén externo o LFS según acceso, coste y retención. Versionar manifiestos, no cada gráfico regenerable; conservar estado operativo y snapshots irremplazables con backup. El .gitignore preparado solo afecta al destino. No ejecutar git rm ni filtros históricos como parte de esta propuesta. Actualizar README con parámetros derivados de configuración y añadir CI offline en la raíz del futuro repositorio (un workflow anidado no basta). Criterio: clon ligero, restauración documentada de datos/modelos y CI sin credenciales ni red.
