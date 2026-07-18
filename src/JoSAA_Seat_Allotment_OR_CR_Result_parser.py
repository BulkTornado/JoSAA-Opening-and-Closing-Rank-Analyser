import csv
import sqlite3
import sys
from pathlib import Path

ROOT_DIR        = Path().cwd()

CSV_DATA_DIR    = ROOT_DIR / "data"

if not CSV_DATA_DIR.exists():
    print("Not running from root of project. Stopping the script.")
    sys.exit(1)

CSV_FILES       = list(CSV_DATA_DIR.glob("*.csv"))

years = [2025, 2026]
rounds = [1, 2, 3, 4, 5, 6]

NO_OF_EXPECTED_CSV_FILES = len(years) * len(rounds)
NO_OF_CSV_FILES = len(CSV_FILES)

if NO_OF_CSV_FILES != NO_OF_EXPECTED_CSV_FILES:
    print("The number of csv files does not match the number of expected csv files.")
    print("Stopping the script.")
    sys.exit(2)

DB_FILE         = ROOT_DIR / "JoSAA-OR-CR.db"
DB_SCHEMA       = ROOT_DIR / "schema.sql"

if not DB_FILE.exists():
    print(
        "Could not find database file. Ensure that the JoSAA-OR-CR.db file exists and is in the root of the project."
    )
    print("Stopping the script.")
    sys.exit(2)

if not DB_SCHEMA.exists():
    print(
        "Could not find database schema. Ensure that the schema.sql file exists and is in the root of the project."
    )
    print("Stopping the script.")
    sys.exit(2)

for file in CSV_FILES:
    print(file)
