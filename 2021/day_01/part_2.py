"""Day 1 part 2 solcution."""
import argparse
from pathlib import Path

import numpy as np
import pytest

from aoc.parsers import text_to_integer_array

INPUT_TXT = Path(__file__).parent / "input.txt"


def solve(text: str) -> int:
    """Solves the puzzle."""
    data = text_to_integer_array(text)
    convolved_data = np.convolve(data, np.ones(3, dtype=int), "valid")
    return int(np.sum(np.diff(convolved_data) > 0))  # type: ignore


INPUT_S = """\
199
200
208
210
200
207
240
269
260
263
"""


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((INPUT_S, 5),),
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
