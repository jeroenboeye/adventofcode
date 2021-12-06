"""Day 4 part 1 solution."""
import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import (
    Generator,
    List,
    Set,
)

import pytest

INPUT_TXT = Path(__file__).parent / "input.txt"
NumberLine = Set[int]


@dataclass
class NumberSheet:
    """Bingo numbersheet with rows and columns."""

    rows: List[NumberLine]
    columns: List[NumberLine]
    won: bool = False

    def total(self) -> int:
        """Return the total of all numbers in the sheet."""
        return sum(sum(row) for row in self.rows)

    def remove_number(self, number: int) -> None:
        """Remove a number from the sheet, when a row or column is empty the sheet has won."""
        for row in self.rows:
            row.discard(number)
            if len(row) == 0:
                self.won = True
        for column in self.columns:
            column.discard(number)
            if len(column) == 0:
                self.won = True


def numbersheet_parser(text: str) -> Generator:
    """Parse the input."""
    for sheet in text.split("\n\n")[1:]:
        rows: List[NumberLine] = []
        columns: List[NumberLine] = [set() for _ in range(5)]
        for text_row in sheet.splitlines():
            row = set()
            for i, value in enumerate(text_row.split()):
                row.add(int(value))
                columns[i].add(int(value))
            rows.append(row)
        yield NumberSheet(rows, columns)


def solve(text: str) -> int:
    """Solves the puzzle."""
    random_numbers = [int(x) for x in text.splitlines()[0].split(sep=",")]
    numbersheets: List[NumberSheet] = list(numbersheet_parser(text))
    for number in random_numbers:
        for sheet in numbersheets:
            sheet.remove_number(number)
            if sheet.won:
                break
        if sheet.won:
            break
    return sheet.total() * number


INPUT_S = """\
7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
"""


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((INPUT_S, 4512),),
)
def test(input_s: str, expected: int) -> None:
    """Check that the solution is correct."""
    assert solve(input_s) == expected


def main() -> int:
    """Run the solution."""
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", nargs="?", default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(solve(f.read()))

    return 0


if __name__ == "__main__":
    exit(main())
