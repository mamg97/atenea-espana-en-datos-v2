# MIDAS — estado y consolidación preparada

Auditoría local: 21 de septiembre de 2026. Base Git: `25d820ee`.

MIDAS reúne investigación de señales técnicas iniciada en R, un pipeline LightGBM y una línea genética posterior. Markowitz es un módulo independiente de asignación. Este directorio es una **estructura de destino preparada**, con documentación e inventarios; todavía no es una aplicación ejecutable ni una migración del código.

## Resultado principal

La carpeta local `MIDAS_GIT` pertenece al repositorio padre `personal_mamg`. No tiene repositorio Git independiente. El remoto observado es `https://github.com/mamg97/atenea-espana-en-datos-v2.git`, no un remoto MIDAS. La cuenta personal es mamg97; LITOS/litosartesania queda fuera de este trabajo. No se ha verificado el estado remoto ni cambiado su configuración.

El código más reciente de la línea genética está en `AGENTE/genetic_invest_agent/sp500_portfolio_agent.py`, fuera de MIDAS_GIT. Es candidato principal para consolidación, no código validado para producción. LightGBM v2 queda como línea histórica recuperable. Markowitz debe mantenerse separado de la generación de señales.

## Continuidad entre conversaciones

Para continuar en ChatGPT o volver a Codex, adjuntar [MIDAS_CONTINUIDAD.md](MIDAS_CONTINUIDAD.md). Es el documento puente autocontenido: reúne contexto, límites, estado, hoja de ruta y protocolo de actualización. Este README funciona como índice del directorio.

## Documentos

- [Estado y evidencias](docs/ESTADO.md).
- [Hoja de ruta y estructura](docs/HOJA_DE_RUTA.md).
- `inventario.json`: 152 archivos locales de MIDAS_GIT con tamaños y SHA-256, incluidos datos no versionados.
- `duplicados.json`: duplicados exactos locales.
- `inventario_git.json`: rutas, tamaños y objetos Git de los tres componentes en HEAD.
- `duplicados_git.json`: duplicados exactos por identidad de blob, dentro de ese alcance.
- `objetos_grandes_historial.json`: blobs de al menos 10 MiB alcanzables desde todas las referencias locales del repositorio padre; no es una medición de espacio comprimido.
- `verificacion_sintaxis.json`: análisis sintáctico estático de 21 archivos Python en HEAD.

## Estructura preparada

`src/midas/data`, `features`, `strategies`, `backtesting`, `portfolio`, `reporting`; `config`, `tests`, `research`, `artifacts` y `docs`. Son destinos reservados, sin código antiguo copiado ni imports con efectos secundarios. `config/example.toml` expresa el contrato inicial propuesto; aún no existe un programa que lo consuma.

No se han ejecutado estrategias, entrenamientos, notificaciones ni operaciones; tampoco se han movido/eliminado archivos, modificado remotos, creado commits o reescrito historial. Los originales permanecen en sus ubicaciones.
