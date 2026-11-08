import atexit
import csv
import sqlite3
from pathlib import Path

from console import console
from josaa_or_cr_row import JoSAAORCRRow

ROOT_DIR        = Path().cwd()

CSV_DATA_DIR    = ROOT_DIR / "data"

if not CSV_DATA_DIR.exists():
    console.print(
        "Not running from root of project.\n"
        "Stopping the script.",
        style="danger"
    )
    exit(1)

CSV_FILES       = list(CSV_DATA_DIR.glob("*.csv"))
CSV_FILES.sort()

if len(CSV_FILES) == 0:
    console.print(
        "No CSV files found.\n"
        "Stopping the script.",
        style="danger"
    )
    exit(2)

DB_FILE         = ROOT_DIR / "JoSAA-OR-CR.db"
DB_SCHEMA_FILE  = ROOT_DIR / "schema.sql"

if not DB_FILE.exists():
    console.print(
        "Could not find database file. Creating JoSAA-OR-CR.db file in the root of the project.",
        style="warning"
    )
    DB_FILE.touch()
    console.print(
        "Database file created. Continuing...",
        style="info"
    )

if not DB_SCHEMA_FILE.exists():
    console.print(
        "Could not find database schema. Ensure that the schema.sql file exists and is in the root of the project.\n"
        "Stopping the script.",
        style="danger"
    )
    exit(2)

# Connecting to the database
cxn = sqlite3.connect(DB_FILE)
cur = cxn.cursor()

@atexit.register
def close_db_cxn():
    cxn.close()

DB_SCHEMA: str = DB_SCHEMA_FILE.read_text()

cur.execute(DB_SCHEMA)
cxn.commit()

full_csv_data: list[JoSAAORCRRow] = []

def extract_year_and_round(_file: Path) -> tuple[int, int]:
    file_name: str = _file.name.replace(".csv", "")
    _ = file_name.split("-")
    _year, _rnd = int(_[1]), int(_[-1])

    return _year, _rnd

console.print(
    "\nParsing through the CSV files...\n",
    style="info"
)

for file in CSV_FILES:
    file: Path = file.relative_to(ROOT_DIR)
    year, rnd = extract_year_and_round(file)

    with open(file, encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter="\t")

        for row in csv_reader:
            full_csv_data.append(JoSAAORCRRow.from_csv_row(year, rnd, row))

    console.print(
        f"\t./{file} -> {year:04}, {rnd:02} completed. Total: {len(full_csv_data):10}, Diff: +{"...":>10}",
        style="dim"
    )

console.print()

# Insert into DB
for row in full_csv_data:
    cur.execute(f"""
        INSERT INTO JoSAA_OR_CR
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, row.to_sql_parameters()
    )
cxn.commit()

row_count_in_list: int = len(full_csv_data)
row_count_in_db:   int = cur.execute('''SELECT COUNT(*) FROM JoSAA_OR_CR''').fetchone()[0]

if row_count_in_list != row_count_in_db:
    console.print(
        "Something went wrong.\n"
        f"Row count in list: {row_count_in_list}\n"
        f"Row count in db: {row_count_in_db}",
        style="danger"
    )
    exit(3)

console.print(
    f"OR-CR Result parser script finished successfully.\n"
    f"Total rows parsed: {row_count_in_list}\n"
    f"Total rows inserted: {row_count_in_db}\n",
    style="success"
)
