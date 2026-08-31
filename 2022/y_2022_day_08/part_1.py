"""Day 8 part 1 solution."""

import argparse
from pathlib import Path
from typing import Iterator

import pytest

INPUT_TXT = Path(__file__).parent / "input.txt"


def parse(text: str) -> Iterator[list[int]]:
    """Parse 2d array of integers."""
    for line in text.splitlines():
        yield [int(c) for c in line]


def is_visible(x: int, y: int, row: list[int], column: list[int]) -> bool:
    """Check if a tree is visible from any direction."""
    if not (0 < x < len(row) and 0 < y < len(column)):
        return True
    height = row[x]

    if (
        max(row[:x], default=-1) >= height  # Look left
        and max(row[x + 1 :], default=-1) >= height  # Look right
        and max(column[:y], default=-1) >= height  # Look uo
        and max(column[y + 1 :], default=-1) >= height  # Look down
    ):
        return False
    else:
        return True


def solve(text: str) -> int:
    """Solve the puzzle."""
    forest = list(parse(text))
    n_visible = 0
    columns = {x: [row[x] for row in forest] for x in range(len(forest[0]))}

    for y, row in enumerate(forest):
        for x, column in columns.items():
            n_visible += is_visible(x, y, row, column)
    return n_visible


INPUT_S = """\
30373
25512
65332
33549
35390
"""
EXPECTED = 21


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((INPUT_S, EXPECTED),),
)
def test(input_s: str, expected: int) -> None:
    """Check that the solution is correct."""
    assert solve(input_s) == expected


def main() -> int:
    """Run the solution."""
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", nargs="?", default=INPUT_TXT)
    parser.add_argument(
        "-s",
        "--submit",
        action="store_const",
        dest="submit_solution",
        const=True,
        default=False,
    )
    args = parser.parse_args()

    with open(args.data_file) as f:
        solution = solve(f.read())

    print(solution)

    if args.submit_solution:
        from aocd import submit

        print("Submitting solution.")
        # Derive year and day from parent directory name, dirname should end in e.g. /2021/y_2021_day_01
        full_path = Path(__file__).parent.absolute()
        submit(solution, year=int(full_path.parent.name), day=int(full_path.name.split("_")[-1]))

    return 0


if __name__ == "__main__":
    exit(main())
