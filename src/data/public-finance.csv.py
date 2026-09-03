from pathlib import Path

from _google_sheets import read_sheet_or_seed, write_mapped_csv

SHEET_RANGE = "Fact_finanzas_publicas!A:AC"
SEED_PATH = Path(__file__).resolve().parent / "seed" / "fact_finanzas_publicas_2024.csv"

COLUMN_MAP = {
    "año": "year",
    "categoria": "category",
    "subcategoria": "subcategory",
    "indicador_id": "indicator_id",
    "indicador": "indicator_name",
    "fuente_oficial": "source",
    "valor": "value",
    "url_verificable": "source_url",
    "unidad": "unit",
    "periodo_referencia": "reference_period",
    "frecuencia": "frequency",
    "tipo_periodo": "period_type",
    "estado_dato": "status",
    "geo_nivel": "geo_level",
    "geo_nombre": "geo_name",
    "definicion": "definition",
    "fecha_revision_fuente": "source_revision_date",
    "notas": "notes",
    "lado": "side",
    "sector_sec": "sector_sec",
    "clasificacion": "classification",
    "codigo": "code",
    "parent_codigo": "parent_code",
    "nivel": "level",
    "vintage": "vintage",
    "metodologia": "methodology",
    "source_id": "source_id",
    "es_ajuste_vintage": "is_vintage_adjustment",
    "es_corte_analitico": "is_analytic_cut",
}

rows, _origin = read_sheet_or_seed(SHEET_RANGE, SEED_PATH)
write_mapped_csv(rows, COLUMN_MAP)
