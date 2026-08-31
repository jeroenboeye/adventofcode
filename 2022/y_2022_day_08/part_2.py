"""Day 8 part 2 solution."""

import argparse
from pathlib import Path
from typing import Iterator

import pytest

INPUT_TXT = Path(__file__).parent / "input.txt"


def parse(text: str) -> Iterator[list[int]]:
    """Parse 2d array of integers."""
    for line in text.splitlines():
        yield [int(c) for c in line]


def view(treeline: list[int], index: int, delta: int) -> int:
    """Search for distance to non-lower tree along treeline."""
    max_index = len(treeline) - 1
    height = treeline[index]
    new_index = index + delta
    if new_index < 0 or max_index < new_index:
        return 0

    distance = 1
    while 0 < new_index < max_index and treeline[new_index] < height:
        distance += 1
        new_index += delta
    return distance


def solve(text: str) -> int:
    """Solve the puzzle."""
    forest = list(parse(text))
    columns = {x: [row[x] for row in forest] for x in range(len(forest[0]))}

    max_score = 0
    for y, row in enumerate(forest):
        for x, column in columns.items():
            score = view(row, x, -1) * view(row, x, 1) * view(column, y, -1) * view(column, y, 1)
            max_score = max(max_score, score)
    return max_score


INPUT_S = """\
30373
25512
65332
33549
35390
"""
EXPECTED = 8


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
