# TODO add docstring

import atexit
import sqlite3
from pathlib import Path

# TODO remove tabulate dependency by using the
#   Table class from the Rich package
import tabulate

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
    _ = cur.fetchall()
    # TODO implement rich.table and thus remove the tabulate dependency
    console.print(tabulate.tabulate(_, headers=["COUNT(*)"]), style="bold green")



if __name__ == "__main__":
    main()
