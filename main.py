import atexit
import sqlite3
from pathlib import Path

from rich.table import Table
import tabulate

from src.console import console, console_err

ROOT_DIR = Path().cwd()

DB_FILE         = ROOT_DIR / "JoSAA-OR-CR.db"

if not DB_FILE.exists():
    console_err.print("Could not find the database file. Ensure that the JoSAA-OR-CR.db file exists and is in the root of the project.")
    console_err.print("Stopping the script...")
    exit(2)

# Connecting to the database
cxn = sqlite3.connect(DB_FILE)
cur = cxn.cursor()

@atexit.register
def close_db_cxn():
    cxn.close()

def main():
    console.print("Hello from josaa-opening-and-closing-rank-analyser!", style="bold italic")

    cur.execute('''SELECT COUNT(*) FROM JoSAA_OR_CR''')
    _ = cur.fetchall()
    console.print(tabulate.tabulate(_, headers=["COUNT(*)"]), style="bold green")



if __name__ == "__main__":
    main()
