import atexit
import csv
import sqlite3
from pathlib import Path

import rich

from josaa_or_cr_row import JoSAAORCRRow

ROOT_DIR        = Path().cwd()

CSV_DATA_DIR    = ROOT_DIR / "data"

if not CSV_DATA_DIR.exists():
    print("Not running from root of project.")
    print("Stopping the script.")
    exit(1)

CSV_FILES       = list(CSV_DATA_DIR.glob("*.csv"))
CSV_FILES.sort()

if len(CSV_FILES) == 0:
    print("No CSV files found.")
    print("Stopping the script.")
    exit(2)

DB_FILE         = ROOT_DIR / "JoSAA-OR-CR.db"
DB_SCHEMA_FILE  = ROOT_DIR / "schema.sql"

if not DB_FILE.exists():
    print("Could not find database file. Creating JoSAA-OR-CR.db file in the root of the project.")
    DB_FILE.touch()
    print("Database file created. Continuing...")

if not DB_SCHEMA_FILE.exists():
    print(
        "Could not find database schema. Ensure that the schema.sql file exists and is in the root of the project."
    )
    print("Stopping the script.")
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


for file in CSV_FILES:
    file: Path = file.relative_to(ROOT_DIR)
    print(f"Processing file: ./{file}...")
    year, rnd = extract_year_and_round(file)

    with open(file, encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter="\t")

        for row in csv_reader:
            full_csv_data.append(JoSAAORCRRow.from_csv_row(year, rnd, row))

    print(f"Year: {year}, Round: {rnd} completed.")

    print()


# Insert into DB
for row in full_csv_data:
    cur.execute(f"""
        INSERT INTO JoSAA_OR_CR
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, row.to_sql_parameters()
    )
cxn.commit()

print(f"OR-CR Result parser script finished successfully. Total rows inserted: {len(full_csv_data)}")
