"""Day 4 part 1 solution."""
import argparse
from pathlib import Path

import pytest

INPUT_TXT = Path(__file__).parent / "input.txt"


def parse(elf_range: str) -> set[int]:
    """Parse elf string range into set of integers."""
    start, stop = (int(x) for x in elf_range.split("-"))
    return set(range(start, stop + 1))


def solve(text: str) -> int:
    """Solve the puzzle."""
    total = 0
    for elf_pair in text.splitlines():
        elf_1_range, elf_2_range = elf_pair.split(",")
        elf_1_set = parse(elf_1_range)
        elf_2_set = parse(elf_2_range)
        if elf_1_set.issubset(elf_2_set) or elf_2_set.issubset(elf_1_set):
            total += 1
    return total


INPUT_S = """\
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
"""
EXPECTED = 2


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
