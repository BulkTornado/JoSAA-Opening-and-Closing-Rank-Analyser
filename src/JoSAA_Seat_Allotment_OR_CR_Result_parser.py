import csv
import sqlite3
import sys
from pathlib import Path

ROOT_DIR        = Path().cwd()

CSV_DATA_DIR    = ROOT_DIR / "data"

if not CSV_DATA_DIR.exists():
    print("Not running from root of project.")
    print("Stopping the script.")
    sys.exit(1)

CSV_FILES       = list(CSV_DATA_DIR.glob("*.csv"))
CSV_FILES.sort()

if len(CSV_FILES) == 0:
    print("No CSV files found.")
    print("Stopping the script.")
    sys.exit(2)

DB_FILE         = ROOT_DIR / "JoSAA-OR-CR.db"
DB_SCHEMA       = ROOT_DIR / "schema.sql"

if not DB_FILE.exists():
    print(
        "Could not find database file. Ensure that the JoSAA-OR-CR.db file exists and is in the root of the project."
    )
    print("Touch the database file.")
    DB_FILE.touch()
    print("Database file created. Continuing...")

if not DB_SCHEMA.exists():
    print(
        "Could not find database schema. Ensure that the schema.sql file exists and is in the root of the project."
    )
    print("Stopping the script.")
    sys.exit(2)

data_to_insert = []

for file in CSV_FILES:
    print(f"Processing file: {file.relative_to(ROOT_DIR)}")