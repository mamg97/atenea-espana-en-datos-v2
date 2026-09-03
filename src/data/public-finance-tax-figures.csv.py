from pathlib import Path

from _google_sheets import read_sheet_or_seed, write_mapped_csv

SHEET_RANGE = "Figuras_ingresos_no_sumables!A:K"
SEED_PATH = Path(__file__).resolve().parent / "seed" / "figuras_ingresos_2024.csv"

COLUMN_MAP = {
    "año": "year",
    "grupo_sec": "sec_group",
    "subsector": "subsector",
    "figura": "tax_figure",
    "valor_mill_eur": "value_mill_eur",
    "es_exhaustivo": "is_exhaustive",
    "es_sumable_en_sankey": "is_summable_in_sankey",
    "fuente_oficial": "source",
    "url_verificable": "source_url",
    "vintage": "vintage",
    "notas": "notes",
}

rows, _origin = read_sheet_or_seed(SHEET_RANGE, SEED_PATH)
write_mapped_csv(rows, COLUMN_MAP)
