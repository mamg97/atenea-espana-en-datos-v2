import csv
import json
import os
import sys
from pathlib import Path

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]


def _credentials_available():
    return bool(
        os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
        or os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    )


def _get_credentials():
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


def read_google_sheet(sheet_range):
    """Return a list of rows from Google Sheets or raise a descriptive error."""
    sheet_id = os.environ.get("GOOGLE_SHEET_ID")
    if not sheet_id:
        raise RuntimeError("GOOGLE_SHEET_ID no está configurado.")
    if not _credentials_available():
        raise RuntimeError("No hay credenciales de Google disponibles.")

    from googleapiclient.discovery import build

    service = build(
        "sheets",
        "v4",
        credentials=_get_credentials(),
        cache_discovery=False,
    )

    response = (
        service.spreadsheets()
        .values()
        .get(
            spreadsheetId=sheet_id,
            range=sheet_range,
            valueRenderOption="UNFORMATTED_VALUE",
            dateTimeRenderOption="FORMATTED_STRING",
        )
        .execute()
    )
    rows = response.get("values", [])
    if not rows:
        raise RuntimeError(f"No se encontraron datos en {sheet_range}.")
    return rows


def read_semicolon_seed(path):
    path = Path(path)
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.reader(handle, delimiter=";"))


def read_sheet_or_seed(sheet_range, seed_path):
    """
    Prefer Google Sheets; fall back to the versioned seed snapshot.

    The fallback intentionally emits a warning to stderr so build logs make the
    data origin explicit without corrupting loader stdout.
    """
    mode = os.environ.get("ATENEA_DATA_MODE", "auto").strip().lower()

    if mode not in {"auto", "google", "seed"}:
        raise RuntimeError(
            "ATENEA_DATA_MODE debe ser auto, google o seed."
        )

    if mode != "seed":
        try:
            return read_google_sheet(sheet_range), "google"
        except Exception as exc:
            if mode == "google":
                raise
            print(
                f"[ATENEA] Aviso: no se pudo leer {sheet_range} desde Google "
                f"Sheets ({exc}). Se usa el snapshot local versionado.",
                file=sys.stderr,
            )

    return read_semicolon_seed(seed_path), "seed"


def write_mapped_csv(rows, column_map):
    if not rows:
        raise RuntimeError("El origen de datos no contiene filas.")

    source_header = [str(value).strip() for value in rows[0]]
    output_header = [column_map.get(column, column) for column in source_header]

    writer = csv.DictWriter(
        sys.stdout,
        fieldnames=output_header,
        lineterminator="\n",
        extrasaction="ignore",
    )
    writer.writeheader()

    for raw_row in rows[1:]:
        raw_row = list(raw_row) + [""] * (len(source_header) - len(raw_row))
        source_record = dict(zip(source_header, raw_row))
        output_record = {
            column_map.get(key, key): value for key, value in source_record.items()
        }
        writer.writerow(output_record)
