#!/usr/bin/env python3
import csv
import io
import os
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_loader(relative_path):
    result = subprocess.run(
        [sys.executable, str(ROOT / relative_path)],
        cwd=ROOT,
        env=os.environ.copy(),
        check=False,
        capture_output=True,
        text=True,
    )
    if result.stderr:
        print(result.stderr.rstrip(), file=sys.stderr)
    if result.returncode != 0:
        raise RuntimeError(
            f"Falló el loader {relative_path}:\n{result.stdout}\n{result.stderr}"
        )
    return list(csv.DictReader(io.StringIO(result.stdout)))


def num(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def yes(value):
    return str(value or "").strip().lower() in {"sí", "si", "yes", "true", "1"}


errors = []
warnings = []

fact = run_loader("src/data/public-finance.csv.py")
sources = run_loader("src/data/public-finance-sources.csv.py")
tax_figures = run_loader("src/data/public-finance-tax-figures.csv.py")
observations = run_loader("src/data/observations.csv.py")

source_ids = {row.get("source_id", "") for row in sources if row.get("source_id")}

# ---- Finanzas públicas: integridad de clave y fuentes ----
key_counts = Counter((row.get("year"), row.get("code")) for row in fact)
duplicate_fact = [key for key, count in key_counts.items() if count > 1]
if duplicate_fact:
    errors.append(f"Fact_finanzas_publicas tiene claves año+código duplicadas: {duplicate_fact[:10]}")

missing_sources = sorted({
    row.get("source_id", "")
    for row in fact
    if row.get("source_id") and row.get("source_id") not in source_ids
})
if missing_sources:
    errors.append(f"source_id sin entrada en Dim_fuentes: {missing_sources}")

by_year = defaultdict(list)
for row in fact:
    by_year[int(num(row.get("year")))].append(row)

for year, rows in sorted(by_year.items()):
    by_code = {row.get("code"): row for row in rows}
    gasto = by_code.get("S13.GASTO")
    recursos = by_code.get("S13.RECURSOS")
    deficit = by_code.get("S13.DEFICIT")

    if gasto and recursos and deficit:
        lhs = num(recursos.get("value")) + num(deficit.get("value"))
        rhs = num(gasto.get("value"))
        if abs(lhs - rhs) > 0.5:
            errors.append(
                f"{year}: recursos + déficit != gasto ({lhs:.0f} vs {rhs:.0f} M€)"
            )

        incomes = [
            row for row in rows
            if row.get("parent_code") == "S13.RECURSOS" and row.get("side") == "ingreso"
        ]
        income_sum = sum(num(row.get("value")) for row in incomes)
        if abs(income_sum - num(recursos.get("value"))) > 0.5:
            errors.append(
                f"{year}: suma de ramas de ingreso != recursos ({income_sum:.0f} vs {num(recursos.get('value')):.0f} M€)"
            )

        cofog = [
            row for row in rows
            if row.get("parent_code") == "S13.GASTO"
            and row.get("side") == "gasto"
            and str(row.get("level")) == "1"
        ]
        if cofog:
            cofog_sum = sum(num(row.get("value")) for row in cofog)
            if abs(cofog_sum - rhs) > 0.5:
                errors.append(
                    f"{year}: suma COFOG nivel 1 != gasto ({cofog_sum:.0f} vs {rhs:.0f} M€)"
                )

    # Reconciliar jerarquías que no son cortes analíticos ni el nodo central.
    children = defaultdict(list)
    for row in rows:
        if row.get("parent_code") and not yes(row.get("is_analytic_cut")):
            children[row.get("parent_code")].append(row)

    for parent_code, child_rows in children.items():
        if parent_code in {"S13.GASTO", "S13.RECURSOS"}:
            continue
        parent = by_code.get(parent_code)
        if not parent:
            errors.append(f"{year}: parent_code {parent_code} no existe para {len(child_rows)} filas")
            continue
        child_sum = sum(num(row.get("value")) for row in child_rows)
        parent_value = num(parent.get("value"))
        if abs(child_sum - parent_value) > 0.5:
            errors.append(
                f"{year}: hijos de {parent_code} no reconcilian ({child_sum:.0f} vs {parent_value:.0f} M€)"
            )

    # Cortes analíticos: los hijos del corte sí deben sumar el corte.
    for row in rows:
        if not yes(row.get("is_analytic_cut")):
            continue
        analytic_children = [r for r in rows if r.get("parent_code") == row.get("code")]
        if analytic_children:
            child_sum = sum(num(r.get("value")) for r in analytic_children)
            if abs(child_sum - num(row.get("value"))) > 0.5:
                errors.append(
                    f"{year}: corte analítico {row.get('code')} no reconcilia ({child_sum:.0f} vs {num(row.get('value')):.0f} M€)"
                )

# ---- Figuras tributarias temporales ----
wrong_tax_flags = [
    row for row in tax_figures
    if str(row.get("is_summable_in_sankey", "")).strip().lower() not in {"no", "false", "0"}
]
if wrong_tax_flags:
    errors.append("Hay figuras tributarias temporales marcadas como sumables en el Sankey.")

# ---- Dataset KPI heredado: detectar problemas sin bloquear el despliegue ----
obs_groups = defaultdict(list)
for row in observations:
    key = (
        row.get("year"),
        row.get("indicator_id"),
        row.get("geo_level"),
        row.get("geo_name"),
    )
    obs_groups[key].append(row)

ambiguous = []
for key, rows in obs_groups.items():
    values = {row.get("value") for row in rows}
    if len(rows) > 1 and len(values) > 1:
        ambiguous.append((key, len(rows)))
if ambiguous:
    affected_rows = sum(count for _key, count in ambiguous)
    warnings.append(
        f"Datos KPI: {len(ambiguous)} claves año+indicador+geografía tienen varios valores "
        f"({affected_rows} filas). La interfaz omite esos años ambiguos en vez de escoger una fila arbitraria."
    )

for row in observations:
    if row.get("indicator_id") == "pib_nominal_eur":
        unit = str(row.get("unit", "")).lower()
        value = num(row.get("value"))
        if "millones" in unit and abs(value) > 100_000_000:
            warnings.append(
                "pib_nominal_eur: el valor parece estar expresado en euros mientras la unidad declara millones de euros. "
                "La corrección definitiva debe hacerse en Datos_largos_Looker."
            )
            break

print("ATENEA · validación de datos")
print(f"- fact_finanzas_publicas: {len(fact)} filas")
print(f"- dim_fuentes: {len(sources)} filas")
print(f"- figuras tributarias temporales: {len(tax_figures)} filas")
print(f"- Datos_largos_Looker: {len(observations)} filas")

for warning in warnings:
    print(f"WARNING: {warning}")

if errors:
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    raise SystemExit(1)

print("OK: controles bloqueantes superados.")
