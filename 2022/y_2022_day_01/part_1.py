"""Day 1 part 1 solution."""
import argparse
from pathlib import Path
from typing import Iterator

import pytest

INPUT_TXT = Path(__file__).parent / "input.txt"


def sum_per_elf_calories(text: str) -> Iterator[int]:
    """Parse the input."""
    for elf_text in text.split("\n\n"):
        yield sum([int(calories) for calories in elf_text.splitlines()])


def solve(text: str) -> int:
    """Solve the puzzle."""
    return max(list(sum_per_elf_calories(text)))


INPUT_S = """\
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
"""


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((INPUT_S, 24000),),
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
