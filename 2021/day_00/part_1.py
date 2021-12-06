"""Day 0 part 1 solution."""
import argparse
from pathlib import Path

import pytest

INPUT_TXT = Path(__file__).parent / "input.txt"


def solve(text: str) -> int:
    """Solve the puzzle."""
    return 1


INPUT_S = """\
"""


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((INPUT_S, 1),),
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
        day = int(Path(__file__).parent.absolute().name.split("_")[1])
        submit(solution, year=2021, day=day)

    return 0


if __name__ == "__main__":
    exit(main())
