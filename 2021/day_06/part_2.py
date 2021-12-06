"""Day 0 part 1 solution."""
import argparse
from pathlib import Path
from typing import Dict

import pytest

INPUT_TXT = Path(__file__).parent / "input.txt"


def parse_fish_age(text: str) -> Dict[int, int]:
    """Parse the input."""
    fish_age_count: Dict[int, int] = {}
    for age in text.split(","):
        fish_age_count[int(age)] = fish_age_count.get(int(age), 0) + 1
    return fish_age_count


def solve(text: str) -> int:
    """Solve the puzzle."""
    fish_age_count = parse_fish_age(text)
    for _ in range(256):
        fish_age_count = {(k - 1): v for k, v in fish_age_count.items()}
        fish_age_count[6] = fish_age_count.get(6, 0) + fish_age_count.get(-1, 0)
        fish_age_count[8] = fish_age_count.get(-1, 0)
        if -1 in fish_age_count:
            del fish_age_count[-1]
    return sum(fish_age_count.values())


INPUT_S = """\
3,4,3,1,2
"""


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((INPUT_S, 26984457539),),
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
