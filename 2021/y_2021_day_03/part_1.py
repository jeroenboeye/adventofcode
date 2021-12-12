"""Day 3 part 1 solution."""
import argparse
from pathlib import Path

import pytest

from aoc.parsers import unspaced_text_to_2d_list

INPUT_TXT = Path(__file__).parent / "input.txt"


def solve(text: str) -> int:
    """Solves the puzzle."""
    x = unspaced_text_to_2d_list(text, int)
    gamma_bit_list = [str(int(sum(column) > len(column) / 2)) for column in zip(*x)]
    gamma_bits = "".join(gamma_bit_list)
    epsilon_bits = "".join("1" if x == "0" else "0" for x in gamma_bits)
    return int(gamma_bits, 2) * int(epsilon_bits, 2)


INPUT_S = """\
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
"""


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((INPUT_S, 198),),
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
