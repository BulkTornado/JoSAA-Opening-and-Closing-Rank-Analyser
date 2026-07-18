import csv
import sqlite3
import sys
from pathlib import Path


CSV_FILE_DIR = Path() / "data"

if not CSV_FILE_DIR.exists():
    print("Not running from root of project. Stopping the script.")
    sys.exit(1)

years = [2024, 2025, 2026]
rounds = [1, 2, 3, 4, 5, 6]

DB_FILE = Path() / "JoSAA_Seat_Allotment.db"
DB_SCHEMA = Path() / "schema.sql"

if not DB_FILE.exists():
    print("Database file not created. Creating it now.")
    DB_FILE.touch()

if not DB_SCHEMA.exists():
    print(
        "Could not find database schema. Ensure that git cloned perfectly, or that the archive was fully extracted "
        "or that the schema.sql file is in the root of the project."
    )
    print("Until then, stopping the script.")
    sys.exit(2)

