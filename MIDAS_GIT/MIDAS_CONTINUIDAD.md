# MIDAS — documento puente entre Codex y ChatGPT

Versión 1 · actualizado el 21 de septiembre de 2026 · idioma de trabajo: español.

## Cómo usar este documento

Este es el punto de continuidad autocontenido del proyecto. Adjuntar este archivo a la siguiente conversación: incluye contexto, auditoría y hoja de ruta, sin depender de abrir enlaces locales. No incluye el código ni los datasets. Las rutas son referencias al ordenador del usuario; disponer de este documento no implica acceso a esos archivos. Para analizar o modificar una implementación, solicitar únicamente los archivos relevantes que no estén disponibles. No afirmar haber inspeccionado o ejecutado lo que no se haya recibido.

## Objetivo y contexto histórico aportado por el usuario

MIDAS es un proyecto de algoritmo de inversión iniciado en el TFG de 2021. Evolucionó desde R, con MACD, RSI, Estocástico, Bollinger, AHP y evaluación de rentabilidad/riesgo, hacia experimentación de estrategias y un pipeline Python LightGBM: PREPROCESSING → TRAIN → INFERENCE → FUNDAMENTAL, coordinado por EJECUCIÓN. En 2026 aparece un agente genético con EMA, RSI, stop loss y take profit y separación IS/OOS. Markowitz se utiliza por separado para asignación de cartera.

Esta historia proviene del usuario: no se ha cotejado íntegramente con el TFG. La referencia inicial a personal_mamg/MIDAS y a un problema Git de unos 882,76 MiB no describe con precisión el estado local actual; prevalecen los hallazgos fechados más abajo.

El objetivo inmediato autorizado es reconstruir y consolidar el proyecto antes de añadir modelos: identificar código útil, variantes, duplicados, datos/modelos pesados, documentación y riesgos de reproducibilidad. No se ha acordado aún un objetivo de rentabilidad, horizonte definitivo, universo definitivo, broker o despliegue real.

## Reglas y separación de cuentas

- Cuenta personal GitHub: mamg97. MIDAS pertenece a este ámbito.
- Cuenta de marca: litosartesania. No mezclar MIDAS con LITOS ni usar sus repositorios o despliegues.
- No eliminar archivos ni reescribir historial Git sin aprobación explícita del usuario.
- Conservar originales y cambios de otros proyectos. Preparar propuestas revisables antes de migraciones.
- No se ha autorizado ejecutar operaciones de inversión, enviar mensajes o desplegar el sistema por el mero hecho de continuar el proyecto.

## Qué está hecho y qué no

**Hecho:** inspección local y Git, identificación de los tres componentes, inventarios y duplicados, revisión estática, documentación y estructura de carpetas de destino.

**No hecho:** migración del código, reparación de errores, instalación de entorno, pruebas funcionales, backtests, entrenamiento, validación de rentabilidades, backup completo, creación de repositorio independiente o publicación. No confundir las carpetas preparadas con una aplicación consolidada.

**Propuesta pendiente de confirmar:** usar el motor genético de cartera como principal candidato, mantener LightGBM y R como referencias comparables y Markowitz como asignación independiente. Es una recomendación de la auditoría, no una decisión definitiva del usuario.

## Ubicaciones para retomar en Codex

- Repositorio padre: `/Users/miguelangelmayordomogragera/Documents/TRABAJO/CODING_PERSONAL/personal_mamg`.
- Línea histórica: `MIDAS_GIT/` dentro de ese repositorio.
- Genético: `AGENTE/genetic_invest_agent/`.
- Markowitz: `AGENTE/markowitz_portfolio/`.
- Documentación y estructura preparada: `/Users/miguelangelmayordomogragera/Documents/Codex/2026-09-21/referenced-chatgpt-conversation-this-is-an/outputs/MIDAS`.
- Base de auditoría: HEAD `25d820ee`. Comprobar de nuevo el estado antes de modificar: puede haber cambiado desde esta fecha.

## Próximo paso recomendado en ChatGPT

Acordar el alcance de una primera versión reproducible y convertir P0–P3 en un plan de implementación pequeño y verificable. No repetir toda la reconstrucción ni proponer otro modelo antes de resolver los bloqueos.

Si se va a revisar código, empezar por `sp500_portfolio_agent.py`, `genetic_agent.py`, `test_agent.py`, su README y requirements. Pedirlos cuando no estén adjuntos. Para LightGBM, pedir MAIN/TRAIN/INFERENCE/EJECUCIÓN v2 y TRAIN v3; para asignación, markowitz_analysis.py. No hace falta subir inicialmente modelos pickle, cientos de gráficos o todos los datos. Para pruebas posteriores bastará una muestra anonimizada o sintética con el esquema necesario.

Preguntas de producto pendientes: ¿se prioriza investigación de estrategias, señales diarias o seguimiento de cartera simulada?, ¿qué universo/horizonte y moneda base se quieren?, ¿qué línea se desea consolidar primero? Resolverlas al abordar esa fase; no suponer que las elecciones de los scripts históricos son requisitos definitivos.

## Protocolo de actualización del puente

Al terminar cada sesión de ChatGPT o Codex, devolver una versión actualizada de este mismo documento, conservando los hallazgos aún válidos. Añadir fecha, decisiones confirmadas por el usuario, cambios realmente aplicados y archivos afectados, comprobaciones realizadas, pendientes y siguiente paso concreto. Separar siempre propuestas de implementaciones y resultados comprobados de hipótesis. Un código sugerido en el chat no cuenta como aplicado al repositorio.

Si una nueva observación contradice esta auditoría, registrar la corrección y su evidencia. No reemplazar el historial con una descripción que haga parecer completado trabajo pendiente. Al volver a Codex, adjuntar la versión más reciente junto con cualquier código modificado fuera del repositorio.

## Registro de continuidad

| Fecha | Entorno | Trabajo realizado | Próxima acción |
| --- | --- | --- | --- |
| 2026-09-21 | Codex local | Auditoría, inventarios, estructura vacía y documentos; sin modificar originales | Definir alcance de primera versión y preparar P0–P3 |
| 2026-09-21 | Codex local | Creado este documento puente autocontenido | Adjuntarlo a ChatGPT y mantenerlo actualizado |

---

# Estado real de MIDAS

## Alcance y método

Raíz inspeccionada: `/Users/miguelangelmayordomogragera/Documents/TRABAJO/CODING_PERSONAL/personal_mamg`. Se inspeccionaron el árbol local, estado Git, historial, archivos fuente locales disponibles y blobs de HEAD. Las lecturas locales demoradas terminaron: inventario.json cubre los 152 archivos locales de MIDAS_GIT con SHA-256; inventario_git.json cubre HEAD de los tres componentes. No se auditaron exhaustivamente todas las copias externas. No se cargaron pickle ni se ejecutaron imports del proyecto. La conversación anterior solo aportaba intención de continuidad, no evidencia técnica adicional.

El estado inicial muestra modificaciones ajenas en AGENTE/LIBROS_YOUTUBE y ATENEA. MIDAS_GIT no muestra cambios propios en `git status --short -- .`. Su último commit observado es `7b91019e` (2026-02-07, Organización). El contexto de 882,76 MiB es histórico y no puede atribuirse a MIDAS con la evidencia actual.

## Familias de código

| Ubicación relativa a personal_mamg | Clasificación y evidencia |
| --- | --- |
| MIDAS_GIT/SIMULACIONES INVERSIONES/MIDAS.R, MIDAS_crypto.R, SIMULACIONES PASADAS/CODIGO_TFG_simulacion.R | Línea R histórica; conservar como referencia del TFG, sin certificar equivalencia con el documento de 2021. |
| MIDAS_GIT/SIMULACIONES INVERSIONES/MIDAS/{MAIN,PREPROCESSING,TRAIN,INFERENCE}_MIDAS_v2.py y FUNDAMENTAL_MIDAS.py | Pipeline modular histórico, candidato a recuperación; el lanzador apunta expresamente a TRAIN v2. |
| MIDAS/.../TRAIN_MIDAS_v3.py | Experimento divergente; el número v3 no significa versión canónica. Tiene defectos concretos. |
| MIDAS/.../MIDAS_v2.py y BORRADORES/MIDAS_v2_1.py | Monolitos con funcionalidades solapadas con los módulos. No son duplicados exactos ni deben eliminarse automáticamente. |
| AGENTE/genetic_invest_agent/sp500_portfolio_agent.py | Candidato principal 2026: evolución IS, selección OOS, señales y diario persistente; necesita validación y separación de responsabilidades. |
| AGENTE/genetic_invest_agent/genetic_agent.py | Variante de estrategia individual; conservar como experimento separado. |
| AGENTE/genetic_invest_agent/test_agent.py | Script de experimentación con evolución, datos y cartera; el nombre no demuestra una suite de pruebas. No se ejecutó. |
| AGENTE/markowitz_portfolio/markowitz_analysis.py | Asignación mediante PyPortfolioOpt con posiciones incrustadas y precios descargados. Independiente de las señales. |
| MIDAS_GIT/TRADING, IA y SCRAPING YAHOO FINANCE | Utilidades y experimentos adyacentes; IA incluye juegos, no todo pertenece al núcleo financiero. |

Se localizaron además copias bajo `Documents/TRABAJO/MIDAS DOCUMENTOS/TFM IA COTIZACIONES`, algunas denominadas OBSOLETA/OBSOLETE CODES, y un archivo de respaldo de 2024 bajo ENDESA - CIBERNOS. No se auditó exhaustivamente su contenido ni se declara redundancia exacta con el código del repositorio.

## Duplicidades y volumen

El inventario de HEAD comprende:

| Componente | Archivos | Bytes sin comprimir |
| --- | ---: | ---: |
| MIDAS_GIT | 71 | 108.023.425 |
| AGENTE/genetic_invest_agent | 9.333 | 604.354.314 |
| AGENTE/markowitz_portfolio | 3 | 50.312 |

Duplicado exacto confirmado: `MIDAS_GIT/SIMULACIONES INVERSIONES/MIDAS_crypto.R` y `MIDAS_GIT/SIMULACIONES INVERSIONES/MIDAS/BORRADORES/MIDAS_crypto.R`. El inventario identifica una sola agrupación idéntica en el alcance seleccionado; las variantes funcionales requieren comparación semántica antes de archivar.

Cuatro modelos pickle versionados: modelo_dif_pre.pkl 24.919.531 bytes, modelo.pkl 24.607.459, modelo_bin.pkl 23.478.649 y modelo_pre.pkl 23.354.326. También están versionados .RData, __pycache__, hojas de resultados, PDF y ZIP.

El registro genético contiene 9.227 SVG (602.336.055 bytes), 99 CSV (1.798.407) y un JSON (41.476). El JSON de cartera es estado operativo: no tratarlo como basura ni regenerarlo sin reconciliación.

Los packs del repositorio padre ocupan 1,42 GiB; incluyen otros proyectos. Entre los mayores blobs históricos hay vídeos de YouTube ajenos a MIDAS, hasta 84.606.641 bytes. Los tamaños del árbol y los de packs no son sumables ni equivalentes. `.gitignore` no retira archivos ya versionados ni reduce el historial existente.

## Bloqueos concretos y reproducibilidad

1. **LightGBM no es portable.** MAIN_v2:29 y EJECUCIÓN:19–22 contienen rutas Windows. Importar MAIN accede a directorios/datos y calcula fechas, por lo que ni importar las funciones es independiente del entorno.
2. **Datos históricos ausentes del árbol versionado esperado.** En DATOS solo aparece etoro_list.csv. MAIN requiere index_data/stocks_data; TRAIN_v2:27 requiere datos_modelo.xlsx. Sí existen localmente datos_modelo.xlsx (123.902.709 bytes), stocks_data e index_data; están fuera del árbol versionado. Su contenido y procedencia aún no se han validado como dataset reproducible. Un clon por sí solo no basta.
3. **Validación temporal insuficiente.** TRAIN_v2:33–45 y v3:29–41 usan GroupShuffleSplit por semana: evita compartir una semana, pero mezcla pasado y futuro. No equivale a evaluación cronológica.
4. **TRAIN v3 presenta un fallo determinista de columnas.** Líneas 227–228 leen 'Sube real' y 'Sube pred', aunque ese DataFrame define nombres distintos en 223–224. Además exporta modelo_dif_pre y no modelo_pre (502–504), requerido por INFERENCE_v2:27. TRAIN_v2 sí exporta modelo_pre.
5. **Ejecución puede continuar tras un fallo.** EJECUCIÓN:35,40,48,54 usa subprocess.run sin check=True ni comprobación del resultado. Entrenamiento desactivado por defecto; TRAIN tiene exportacion=0, por lo que inferencia puede reutilizar modelos antiguos sin trazabilidad.
6. **OOS genético es validación de selección.** sp500_portfolio_agent:630–639 elige el mejor de diez candidatos usando OOS. Hace falta un tramo final intocable para evaluar al ganador; ese OOS no constituye un test final independiente.
7. **Control de aceptación inconsistente.** sp500_portfolio_agent:1088 informa de fitness no positivo, pero :1099 permite generar señales y actualizar el diario si hay cualquier best_genome. El rechazo y la actualización de cartera necesitan un único criterio.
8. **Semillas y datos variables.** No se encontraron random.seed/np.random.seed en los scripts genéticos revisados. Las ventanas dependen de la fecha actual y las descargas no fijan un snapshot. Los requirements genéticos usan mínimos y los de Markowitz no fijan versiones; no hay lock reproducible en estos componentes.
9. **Supuestos de ejecución.** genetic_agent:201–232 utiliza señal y ejecución en el cierre de la misma barra; revisar disponibilidad temporal y ejecutar al siguiente precio permitido. Incluye comisión; no se debe afirmar que ignora todos los costes. Validar por separado gaps, SL/TP intradía y slippage del motor de cartera.
10. **Markowitz mezcla activos de diferentes mercados.** Usa cantidades × precios sin conversión monetaria visible; validar divisas y unidades de cotización antes de comparar pesos. dropna sobre todas las series puede reducir mucho la muestra. Alinear tasa libre de riesgo en la comparación y registrar ventana/covarianza.
11. **Documentación desfasada.** README genético describe una ventana anual y configuración histórica; el código actual calcula 24 meses IS y 6 OOS. No debe presentarse su rentabilidad de ejemplo como resultado validado.
12. **Efectos secundarios y trazabilidad.** El agente incluye Telegram y persistencia del diario. Separar investigación, simulación y notificaciones, con ejecución externa optativa. Revisar secretos en código/notebooks antes de cualquier publicación sin reproducir sus valores. Los pickle existentes carecen de manifiesto verificado de datos, esquema y entorno.

## Verificación realizada y límites

Los 21 archivos Python versionados de los tres componentes pasan ast.parse. Esto demuestra sintaxis, no funcionamiento ni exactitud de resultados. No se ejecutaron los scripts ni test_agent.py: descargan datos, evolucionan estrategias y pueden escribir estado/notificar. No se han contrastado rentabilidades ni realizado una revisión financiera externa; este documento audita software y reproducibilidad. La búsqueda de objetos históricos cubre referencias locales alcanzables, no objetos perdidos ni el servidor remoto.

## Inventario local completado

MIDAS_GIT contiene 152 archivos y 1.009.765.634 bytes lógicos (incluye ignorados). El mayor es DATOS/RESULTADOS.pbix, 161.889.681 bytes. inventario.json incluye SHA-256; el indicador tracked normaliza Unicode NFC para comparar rutas macOS con Git. No se han abierto las hojas ni el PBIX para validar su contenido. Se confirma un grupo de duplicados exactos también en el inventario local.


---

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
