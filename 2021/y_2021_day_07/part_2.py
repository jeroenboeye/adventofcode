"""Day 7 part 2 solution."""
import argparse
from pathlib import Path
from typing import List

import pytest

INPUT_TXT = Path(__file__).parent / "input.txt"


def sum_of_absolute_differences(numbers: List[int], value: int) -> int:
    """Sum of absolute differences."""
    return sum([abs(x - value) for x in numbers])


def sum_of_absolute_triangular_differences(numbers: List[int], value: int) -> int:
    """Sum of absolute triangular differences.

    https://en.wikipedia.org/wiki/Triangular_number
    """
    return sum([int(abs(x - value) * (abs(x - value) + 1) / 2) for x in numbers])


def solve(text: str) -> int:
    """Solve the puzzle."""
    locations = [int(x) for x in text.split(",")]
    midpoint = int(round(sum(locations) / len(locations)))
    delta = sum_of_absolute_triangular_differences(locations, midpoint)
    if delta > sum_of_absolute_triangular_differences(locations, midpoint + 1):
        direction = 1
        midpoint += 1
    else:
        direction = -1
        midpoint -= 1

    new_delta = sum_of_absolute_triangular_differences(locations, midpoint)
    while new_delta < delta:
        delta = new_delta
        midpoint += direction
        new_delta = sum_of_absolute_triangular_differences(locations, midpoint)

    return delta


INPUT_S = """\
16,1,2,0,4,2,7,1,2,14
"""


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((INPUT_S, 168),),
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
