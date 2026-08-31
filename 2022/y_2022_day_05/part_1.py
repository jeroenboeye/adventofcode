"""Day 5 part 1 solution."""

import argparse
import re
from collections import defaultdict
from pathlib import Path
from typing import Iterator

import pytest

INPUT_TXT = Path(__file__).parent / "input.txt"


def parse_stack(text: str) -> dict[int, list[str]]:
    """Parse stack text."""
    stack_dict: dict[int, list[str]] = defaultdict(list)
    for line in text.splitlines():
        for i, char in enumerate(line):
            if char.isalpha():
                stack_dict[i // 4 + 1].insert(0, char)
    return stack_dict


def parse_instructions(text: str) -> Iterator[tuple[int, int, int]]:
    """Generate instructions from text."""
    for instruction_str in text.splitlines():
        yield (int(x) for x in re.findall(r"\d+", instruction_str))  # type: ignore


def solve(text: str) -> str:
    """Solve the puzzle."""
    stack_str, instruction_str = text.split("\n\n")
    stack_dict = parse_stack(stack_str)
    for n, source, target in parse_instructions(instruction_str):
        for _ in range(n):
            stack_dict[target].append(stack_dict[source].pop())
    stack_tops = "".join([stack_dict[i][-1] for i in range(1, len(stack_dict) + 1)])
    return stack_tops


INPUT_S = """\
    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""
EXPECTED = "CMZ"


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((INPUT_S, EXPECTED),),
)
def test(input_s: str, expected: str) -> None:
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
