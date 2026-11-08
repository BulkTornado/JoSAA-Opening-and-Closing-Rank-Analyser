from dataclasses import dataclass

# TODO come up with a better name for the data class.
# TODO look into dataclass, and think of how the AI
#   implemented it, and try to reason why this shouldn't
#   be refactored to smth written and understood by me.
@dataclass
class JoSAAORCRRow:
    year: int
    round: int
    institute_name: str
    academic_program: str
    quota: str
    seat_type: str
    gender: str
    opening_rank: int
    closing_rank: int

    @classmethod
    def from_csv_row(cls, year: int, round_number: int, row: list[str]) -> "JoSAAORCRRow":
        if len(row) != 7:
            raise ValueError(f"Expected 7 columns in a JoSAA row, got {len(row)}")

        return cls(
            year=year,
            round=round_number,
            institute_name=row[0],
            academic_program=row[1],
            quota=row[2],
            seat_type=row[3],
            gender=row[4],
            opening_rank=int(row[5]),
            closing_rank=int(row[6]),
        )

    def to_sql_parameters(self) -> tuple[int, int, str, str, str, str, str, int, int]:
        return (
            self.year,
            self.round,
            self.institute_name,
            self.academic_program,
            self.quota,
            self.seat_type,
            self.gender,
            self.opening_rank,
            self.closing_rank,
        )
