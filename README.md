# ATENEA · España en Datos

Dashboard de datos públicos de España construido con [Observable Framework](https://observablehq.com/framework/).

## Arquitectura de datos

La aplicación usa Google Sheets como data lake ligero de producción y loaders de Observable para convertir cada tabla al formato que consume el frontend.

```text
Google Sheets
├─ Datos_largos_Looker
│  └─ src/data/observations.csv.py
├─ Fact_finanzas_publicas
│  └─ src/data/public-finance.csv.py
├─ Dim_fuentes
│  └─ src/data/public-finance-sources.csv.py
└─ Figuras_ingresos_no_sumables   # puente temporal hasta ingesta anual IGAE
   └─ src/data/public-finance-tax-figures.csv.py

Observable Framework
├─ src/index.md                    # dashboard KPI
└─ src/finanzas-publicas.md        # Sankey / mapa del dinero público
```

`Datos_largos_Looker` sigue siendo la tabla de KPIs del dashboard. El Sankey **no** fuerza datos jerárquicos dentro de esa tabla: usa `Fact_finanzas_publicas`, donde cada fila conserva código, padre, nivel, metodología, vintage y `source_id`.

## Fuentes del Sankey

La primera versión implementada usa exclusivamente datos oficiales de IGAE para 2024:

- Operaciones no financieras / NEDD-SDDS para recursos, gasto y déficit vigentes.
- Informe trimestral de las AAPP 4T 2024 para el detalle económico de ingresos disponible.
- Clasificación funcional COFOG para el gasto por finalidad y el corte analítico de pensiones.

La tabla `Dim_fuentes` evita repetir metadatos y permite enlazar cada registro con su publicación oficial.

## Desarrollo local

Instala dependencias:

```bash
npm install
pip install -r requirements.txt
```

Para trabajar sin credenciales de Google, usa los snapshots versionados:

```bash
ATENEA_DATA_MODE=seed npm run dev
```

Para usar Google Sheets:

```bash
export GOOGLE_SHEET_ID="..."
export GOOGLE_APPLICATION_CREDENTIALS="/ruta/credencial.json"
ATENEA_DATA_MODE=google npm run dev
```

`ATENEA_DATA_MODE=auto` (valor por defecto) intenta Google Sheets y, si no está disponible la hoja nueva o las credenciales, utiliza el snapshot local y deja un aviso visible en los logs del build.

## Validación

Antes de construir o desplegar:

```bash
npm run validate:data
```

Los controles **bloqueantes** del módulo de finanzas públicas comprueban, entre otros:

- clave `año + código` única;
- todos los `source_id` existentes en `Dim_fuentes`;
- recursos + déficit = gasto;
- suma de ramas de ingresos = recursos;
- suma COFOG nivel 1 = gasto total;
- reconciliación de hijos con su padre;
- reconciliación de cortes analíticos como pensiones;
- figuras tributarias temporales marcadas como no sumables.

El validador también informa de anomalías heredadas de `Datos_largos_Looker` sin ocultarlas. La interfaz KPI omite los años con varias cifras nacionales diferentes para una misma clave en lugar de escoger una fila arbitrariamente.

## Nuevas hojas a crear en Google Sheets

Antes de retirar el fallback local, crear en el mismo libro de ATENEA:

1. `Fact_finanzas_publicas`
2. `Dim_fuentes`
3. `Figuras_ingresos_no_sumables` (temporal)

Los CSV semilla están en `src/data/seed/` y tienen exactamente las columnas esperadas por los loaders.

Cuando la ingesta anual de IGAE permita un detalle exhaustivo por figura tributaria, `Figuras_ingresos_no_sumables` debe desaparecer y ese detalle pasará a la jerarquía normal de `Fact_finanzas_publicas`.

## Despliegue

GitHub Actions:

1. instala Python y Node;
2. valida los datos;
3. construye Observable;
4. publica en GitHub Pages.

Además del despliegue por `push` a `main`, el workflow incluye una ejecución diaria para recoger cambios del Google Sheet sin necesidad de hacer un commit manual.

## Seguridad

No versionar credenciales. El repositorio ignora explícitamente `credentials/`, `.env` y `.env.*`. Las credenciales de producción deben seguir viviendo en GitHub Secrets.

## Iteración UI/UX de septiembre de 2026

La revisión posterior a las primeras pruebas locales elimina el sidebar automático de Observable, hace el Sankey principal responsive en tres columnas, mueve el detalle analítico al panel interactivo, mejora la exportación a PDF y evita mostrar como disponibles las series nacionales de alquiler mientras su dimensión territorial siga siendo ambigua. Véase `docs/ITERACION_UI_2026-09-02.md`.

## UI v3 — ajuste visual de Dinero público

Tras la revisión en navegador de la UI v2, `finanzas-publicas` se ha alineado con el tema claro del dashboard principal. El Sankey utiliza ahora todo el ancho de la página y el detalle se abre como drawer superpuesto, por lo que la visualización no se comprime al interactuar. Véase `docs/ITERACION_UI_V3_2026-09-02.md`.
