"""Day 2 part 2 solution."""
import argparse
from pathlib import Path

import pytest

INPUT_TXT = Path(__file__).parent / "input.txt"


def solve(text: str) -> int:
    """Solves the puzzle."""
    aim = 0
    pos_x = 0
    depth = 0
    for line in text.splitlines():
        k, v = line.split()
        if k == "forward":
            pos_x += int(v)
            depth += int(v) * aim
        elif k == "up":
            aim -= int(v)
        elif k == "down":
            aim += int(v)

    return pos_x * depth


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
    ((INPUT_S, 900),),
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
