# Implementación del Sankey de finanzas públicas

## Objetivo

Añadir una vista de finanzas públicas sin duplicar la lógica de KPIs ni escribir cifras en el frontend.

## Tablas

### `Datos_largos_Looker`

Se mantiene como tabla de KPIs del dashboard principal. No se cambia su granularidad para acomodar el Sankey.

### `Fact_finanzas_publicas`

Nueva tabla jerárquica. Las columnas iniciales conservan la convención del dataset ATENEA y se añaden dimensiones específicas:

- `lado`
- `sector_sec`
- `clasificacion`
- `codigo`
- `parent_codigo`
- `nivel`
- `vintage`
- `metodologia`
- `source_id`
- `es_ajuste_vintage`
- `es_corte_analitico`

La visualización se deriva de `codigo → parent_codigo`; no hay árboles codificados manualmente en la página.

### `Dim_fuentes`

Registro de procedencia del módulo. El libro actual ya tiene una hoja `Fuentes` para el inventario KPI, pero su esquema no contiene `source_id`, vintage ni carácter del dato. Para no romper la estructura existente, esta implementación añade `Dim_fuentes` y deja abierta una futura unificación de ambos catálogos.

### `Figuras_ingresos_no_sumables`

Tabla temporal. Permite mostrar IRPF, IVA, Sociedades, IBI, ITP/AJD y otras figuras explícitamente publicadas por IGAE en el informe 4T 2024, pero las marca como no exhaustivas y no sumables.

Debe desaparecer cuando el ETL ingiera el XLSX anual de IGAE de impuestos y cotizaciones con una vintage coherente y detalle exhaustivo.

## Data loaders

- `src/data/public-finance.csv.py`
- `src/data/public-finance-sources.csv.py`
- `src/data/public-finance-tax-figures.csv.py`
- `src/data/public-finance.xlsx.py`

Los loaders aceptan tres modos mediante `ATENEA_DATA_MODE`:

- `google`: Google Sheets obligatorio; falla si falta una hoja.
- `seed`: solo snapshots versionados.
- `auto`: Google primero y snapshot si no está disponible.

## Página

`src/finanzas-publicas.md` crea `/finanzas-publicas`.

La visualización está encapsulada en `src/components/public-finance-sankey.js` y ofrece:

- importe y porcentaje por rama;
- detalle jerárquico al pulsar;
- corte analítico de pensiones;
- figuras tributarias destacadas, señaladas como no sumables;
- enlace a fuente oficial;
- descarga de la rama en CSV;
- descarga del libro Excel generado a partir del mismo origen.

## Reglas contables bloqueantes

`scripts/validate_data.py` impide publicar si:

- hay códigos duplicados por ejercicio;
- una fuente no existe en el registro;
- `recursos + déficit != gasto`;
- las ramas de ingresos no suman recursos;
- COFOG nivel 1 no suma el gasto total;
- los hijos jerárquicos no reconcilian con su padre;
- los componentes de un corte analítico no suman el corte;
- una figura temporal no exhaustiva se marca como sumable.

## Incidencias heredadas detectadas

El validador no las corrige silenciosamente:

1. Los indicadores de alquiler contienen varias cifras diferentes para una misma clave nacional/año, probablemente por pérdida de dimensión territorial. `KpiCard` y las funciones auxiliares omiten esos años ambiguos en lugar de elegir una fila arbitraria.
2. `pib_nominal_eur` parece almacenar euros mientras la unidad declara millones de euros. El frontend actual sigue compensando esa convención para no alterar el resultado visual; la corrección definitiva debe hacerse en la hoja `Datos_largos_Looker`.

## Paso de seed a Google Sheets

1. Crear `Fact_finanzas_publicas`, `Dim_fuentes` y `Figuras_ingresos_no_sumables` en el mismo libro configurado por `GOOGLE_SHEET_ID`.
2. Importar los CSV de `src/data/seed/` sin cambiar cabeceras.
3. Ejecutar `ATENEA_DATA_MODE=google npm run validate:data`.
4. Ejecutar `ATENEA_DATA_MODE=google npm run build`.
5. Cuando el build sea estable, puede cambiarse el workflow a `ATENEA_DATA_MODE: google` para impedir cualquier fallback.
