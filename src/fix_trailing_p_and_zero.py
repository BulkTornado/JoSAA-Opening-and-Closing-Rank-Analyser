"""
This Python script is intended to be run only once. It will fix all the trailing
P's and zeroes in the CSV data for any input year.
"""

import csv
import re
from pathlib import Path

from console import console

ROOT_DIR = Path().cwd()

CSV_DATA_DIR = ROOT_DIR / "data"

if not CSV_DATA_DIR.exists():
    console.print(
        "Not running from root of project.\n"
        "Stopping the script.",
        style="danger"
    )
    exit(1) # TODO document exit code

# TODO implement proper YEAR input validation
YEAR = int(input("Year: "))

# TODO cleanup
# CSV_FILES       = list(CSV_DATA_DIR.glob(f"*{YEAR}*.csv"))
# CSV_FILES.sort()
CSV_FILES       = sorted(
    CSV_DATA_DIR.glob(f"JoSAA-{YEAR}-Round-[1-6].csv")
)

if len(CSV_FILES) == 0:
    console.print(
        "No CSV files found.\n"
        "Stopping the script.",
        style="danger"
    )
    exit(2) # TODO document exit code

# matches digits followed by P at end
pattern_trailing_p = re.compile(r'^(\d+)P$')

# matches integer with .0
pattern_trailing_zero = re.compile(r'^(\d+)\.0$')

for file in CSV_FILES:
    fp = file.relative_to(ROOT_DIR)
    tmp_fp = fp.with_suffix(".tmp")

    with open(fp, 'r', newline='') as infile, open(tmp_fp, 'w', newline='') as outfile:
        reader = csv.reader(infile, delimiter='\t')
        writer = csv.writer(outfile, delimiter='\t')

        for row in reader:
            row = [col.strip() for col in row]

            # fix last two columns only
            for idx in [-2, -1]:
                match_trailing_p = pattern_trailing_p.match(row[idx])
                if match_trailing_p:
                    row[idx] = match_trailing_p.group(1)

                match_trailing_zero = pattern_trailing_zero.match(row[idx])
                if match_trailing_zero:
                    row[idx] = match_trailing_zero.group(1)

            writer.writerow(row)

    # TODO cleanup
    # overwrite original file
    # os.replace(tmp_fp, fp)
    tmp_fp.replace(fp)

console.print(
    "Script finished running. Please use git status or directly run the python script"
    "JoSAA_Seat_Allotment_OR_CR_Result_parser.py in src to check if the script worked or not.",
    style="success"
)