"""Day 2 part 1 solution."""

import argparse
from pathlib import Path

import pytest

INPUT_TXT = Path(__file__).parent / "input.txt"


def solve(text: str) -> int:
    """Solves the puzzle."""
    direction_totals = {
        "forward": 0,
        "up": 0,
        "down": 0,
    }
    for line in text.splitlines():
        k, v = line.split()
        direction_totals[k] += int(v)

    return direction_totals["forward"] * (direction_totals["down"] - direction_totals["up"])


INPUT_S = """\
forward 5
down 5
forward 8
up 3
down 8
forward 2
"""


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((INPUT_S, 150),),
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
