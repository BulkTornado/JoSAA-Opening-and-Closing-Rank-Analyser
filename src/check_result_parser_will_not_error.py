"""
This script is intended to be run before running the actual result parser.

Run this script from the project root. It reads every CSV in ``data/``,
extracts the year and round from each filename, converts each row to a
``JoSAAORCRRow``, and inserts the resulting values into an in-memory SQLite
database using the project's schema.

A successful run shows that the current files can be parsed and their rows
inserted into SQLite with the current schema, without modifying
``JoSAA-OR-CR.db``. It does not verify the persistent database's state or
guarantee that filesystem operations in the real parser will succeed.

Note that this script attempts to follow all the steps exactly as it would
occur in the result parser, except the database being a sqlite in-memory
database. However, it should not create any deviation from a real run of
the result parser script, except that it cannot replicate the duplicate
handling that will be implemented in the real parser in the future.

TODO clean up the last paragraph when I have implemented the duplicate
    handling in the parser script.
"""

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

CSV_FILES: list[Path] = list(CSV_DATA_DIR.glob("*.csv"))
CSV_FILES.sort()

if len(CSV_FILES) == 0:
    console.print(
        "No CSV files found.\n"
        "Stopping the script.",
        style="danger"
    )
    exit(2)

DB_CXN          = sqlite3.connect(":memory:")

@atexit.register
def close_db_cxn():
    DB_CXN.close()

DB_SCHEMA_FILE  = ROOT_DIR / "schema.sql"

if not DB_SCHEMA_FILE.exists():
    console.print(
        "Could not find database schema. Ensure that the schema.sql file exists and is in the root of the project.\n"
        "Stopping the script.",
        style="danger"
    )
    exit(2)

DB_SCHEMA: str = DB_SCHEMA_FILE.read_text()

DB_CXN.execute(DB_SCHEMA)
DB_CXN.commit()

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
            full_csv_data.append(
                JoSAAORCRRow.from_csv_row(year, rnd, row)
            )

    console.print(
        f"\t./{file} -> {year:04}, {rnd:02} completed. Total: {len(full_csv_data):10}, Diff: +{"...":>10}",
        style="dim"
    )

console.print()

# Attempting insert into DB
for row in full_csv_data:
    DB_CXN.execute(f"""
        INSERT INTO JoSAA_OR_CR
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, row.to_sql_parameters()
    )
DB_CXN.commit()

row_count_in_list: int = len(full_csv_data)
row_count_in_db:   int = DB_CXN.execute('''SELECT COUNT(*) FROM JoSAA_OR_CR''').fetchone()[0]

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
