import csv
from pathlib import Path

from josaa_or_cr_row import JoSAAORCRRow

ROOT_DIR        = Path().cwd()

CSV_DATA_DIR    = ROOT_DIR / "data"

if not CSV_DATA_DIR.exists():
    print("Not running from root of project.")
    print("Stopping the script.")
    exit(1)

CSV_FILES: list[Path] = list(CSV_DATA_DIR.glob("*.csv"))
CSV_FILES.sort()

if len(CSV_FILES) == 0:
    print("No CSV files found.")
    print("Stopping the script.")
    exit(2)

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

    print(f"Year: {year:04}, Round: {rnd:02} completed. Total count till now: {len(full_csv_data)}")

    # print(full_csv_data[-1])

    print()