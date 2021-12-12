"""Day 3 part 2 solution."""
import argparse
from pathlib import Path
from typing import (
    Any,
    List,
)

import pytest

from aoc.parsers import unspaced_text_to_2d_list

INPUT_TXT = Path(__file__).parent / "input.txt"


def filter(x: List[List[int]], criteria: str, bit_index: int = 0) -> List[Any]:
    """Apply the a bit criteria to filter list of bits."""
    if len(x) > 1:
        idx = bit_index % len(x[0])
        bits_at_idx = [bits[idx] for bits in x]
        if criteria == "oxygen":
            to_match = int(sum(bits_at_idx) >= len(x) / 2)
        elif criteria == "co2":
            to_match = int(sum(bits_at_idx) < len(x) / 2)
        else:
            raise ValueError(f"Invalid criteria: {criteria}")
        return filter([bits for bits in x if bits[idx] == to_match], criteria, bit_index + 1)
    else:
        return [str(bit) for bit in x[0]]


def solve(text: str) -> int:
    """Solves the puzzle."""
    x = unspaced_text_to_2d_list(text, int)
    oxygen_bit_list = filter(x, "oxygen")
    co2_bit_list = filter(x, "co2")

    oxygen_bits = "".join(oxygen_bit_list)
    co2_bits = "".join(co2_bit_list)

    return int(oxygen_bits, 2) * int(co2_bits, 2)


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
    ((INPUT_S, 230),),
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
