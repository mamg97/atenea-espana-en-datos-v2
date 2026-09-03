from pathlib import Path

from _google_sheets import read_sheet_or_seed, write_mapped_csv

SHEET_RANGE = "Dim_fuentes!A:H"
SEED_PATH = Path(__file__).resolve().parent / "seed" / "dim_fuentes_finanzas_publicas.csv"

COLUMN_MAP = {
    "source_id": "source_id",
    "organismo": "organization",
    "titulo": "title",
    "url": "url",
    "uso_en_atenea": "use_in_atenea",
    "vintage_o_fecha": "vintage_or_date",
    "caracter": "character",
    "notas": "notes",
}

rows, _origin = read_sheet_or_seed(SHEET_RANGE, SEED_PATH)
write_mapped_csv(rows, COLUMN_MAP)
