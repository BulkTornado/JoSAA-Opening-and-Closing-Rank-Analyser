import atexit
import sqlite3
from pathlib import Path

import tabulate

ROOT_DIR = Path().cwd()

DB_FILE         = ROOT_DIR / "JoSAA-OR-CR.db"

if not DB_FILE.exists():
    print("Could not find the database file. Ensure that the JoSAA-OR-CR.db file exists and is in the root of the project.")
    print("Stopping the script...")
    exit(2)

# Connecting to the database
cxn = sqlite3.connect(DB_FILE)
cur = cxn.cursor()

@atexit.register
def close_db_cxn():
    cxn.close()

def main():
    print("Hello from josaa-opening-and-closing-rank-analyser!")

    cur.execute('''SELECT COUNT(*) FROM JoSAA_OR_CR''')
    _ = cur.fetchall()
    print(tabulate.tabulate(_, headers=["COUNT(*)"]))




if __name__ == "__main__":
    main()
