"""Day 9 part 1 solution."""
import argparse
from pathlib import Path
from typing import Iterator, List, Tuple

import pytest

from aoc.parsers import unspaced_text_to_2d_list

INPUT_TXT = Path(__file__).parent / "input.txt"


def get_value_and_neighbors(grid: List[List[int]]) -> Iterator[Tuple[int, int, int, int, int]]:
    """Iterate over all values in the grid and their neighbors.

    Parameters
    ----------
    grid : List[List[int]]
        2D list of ints

    Yields
    ------
    Iterator[Tuple[int, int, int, int, int]]
        value, up, down, right, left
    """
    for y, row in enumerate(grid):
        for x, value in enumerate(row):
            if y == 0:
                up = 10
                down = grid[y + 1][x]
            elif y == len(grid) - 1:
                up = grid[y - 1][x]
                down = 10
            else:
                up = grid[y - 1][x]
                down = grid[y + 1][x]

            if x == 0:
                left = 10
                right = row[x + 1]
            elif x == len(row) - 1:
                left = row[x - 1]
                right = 10
            else:
                left = row[x - 1]
                right = row[x + 1]

            yield value, up, down, right, left


def solve(text: str) -> int:
    """Solve the puzzle."""
    topography = unspaced_text_to_2d_list(text, int)
    total = 0
    for value, up, down, right, left in get_value_and_neighbors(topography):
        if value < min(up, down, left, right):
            total += value + 1
    return total


INPUT_S = """\
2199943210
3987894921
9856789892
8767896789
9899965678
"""


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((INPUT_S, 15),),
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
