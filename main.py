# TODO add docstring

import atexit
import sqlite3
from pathlib import Path

from rich.table import Table

from src.console import console

ROOT_DIR = Path().cwd()

DB_FILE         = ROOT_DIR / "JoSAA-OR-CR.db"

if not DB_FILE.exists():
    console.print(
        "Could not find the database file.\n"
        "Ensure that the JoSAA-OR-CR.db file exists and is in the root of the project.\n"
        "Stopping the script...",
        style="danger"
    )
    exit(2)

# Connecting to the database
cxn = sqlite3.connect(DB_FILE)
cur = cxn.cursor()

@atexit.register
def close_db_cxn():
    cxn.close()

def main():
    console.print("Hello from josaa-opening-and-closing-rank-analyser!", style="bold italic #ffa500")

    cur.execute('''SELECT COUNT(*) FROM JoSAA_OR_CR''')
    row_count = cur.fetchone()[0] # fetchone returns a tuple with one element, thus indexing the first element
    table = Table(show_header=True, header_style="bold green")
    table.add_column("COUNT(*)", style="info")
    table.add_row(str(row_count))
    console.print(table)



if __name__ == "__main__":
    main()
