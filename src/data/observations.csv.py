import csv
import json
import os
import sys
from pathlib import Path

SHEET_ID = os.environ.get("GOOGLE_SHEET_ID")
SHEET_RANGE = "Datos_largos_Looker!A:R"
SEED_PATH = Path(__file__).resolve().parent / "seed" / "observations.csv"

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

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
}


def get_credentials():
    from google.oauth2 import service_account

    credentials_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    if credentials_json:
        return service_account.Credentials.from_service_account_info(
            json.loads(credentials_json), scopes=SCOPES
        )

    credentials_file = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if credentials_file:
        return service_account.Credentials.from_service_account_file(
            credentials_file, scopes=SCOPES
        )

    raise RuntimeError("No se han encontrado credenciales de Google.")


def read_google_rows():
    from googleapiclient.discovery import build

    if not SHEET_ID:
        raise RuntimeError("GOOGLE_SHEET_ID no está configurado.")

    service = build(
        "sheets",
        "v4",
        credentials=get_credentials(),
        cache_discovery=False,
    )

    response = (
        service.spreadsheets()
        .values()
        .get(
            spreadsheetId=SHEET_ID,
            range=SHEET_RANGE,
            valueRenderOption="UNFORMATTED_VALUE",
            dateTimeRenderOption="FORMATTED_STRING",
        )
        .execute()
    )
    rows = response.get("values", [])
    if not rows:
        raise RuntimeError("No se encontraron datos en Datos_largos_Looker.")
    return rows


def emit_google_rows(rows):
    source_header = rows[0]
    output_header = [COLUMN_MAP.get(column, column) for column in source_header]
    writer = csv.DictWriter(sys.stdout, fieldnames=output_header, lineterminator="\n")
    writer.writeheader()

    for raw_row in rows[1:]:
        raw_row = raw_row + [""] * (len(source_header) - len(raw_row))
        source_record = dict(zip(source_header, raw_row))
        output_record = {
            COLUMN_MAP.get(key, key): value for key, value in source_record.items()
        }
        writer.writerow(output_record)


def emit_seed():
    with SEED_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        sys.stdout.write(handle.read())


mode = os.environ.get("ATENEA_DATA_MODE", "auto").strip().lower()
if mode not in {"auto", "google", "seed"}:
    raise RuntimeError("ATENEA_DATA_MODE debe ser auto, google o seed.")

if mode == "seed":
    emit_seed()
else:
    try:
        emit_google_rows(read_google_rows())
    except Exception as exc:
        if mode == "google":
            raise
        print(
            f"[ATENEA] Aviso: no se pudo leer {SHEET_RANGE} desde Google Sheets "
            f"({exc}). Se usa el snapshot local versionado.",
            file=sys.stderr,
        )
        emit_seed()
