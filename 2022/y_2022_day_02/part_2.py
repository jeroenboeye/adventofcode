"""Day 2 part 1 solution."""
import argparse
from pathlib import Path
from typing import Iterator

import pytest

INPUT_TXT = Path(__file__).parent / "input.txt"


def rock_paper_scissors(text: str) -> Iterator[int]:
    """Parse text and resolve rock-paper-scissors games."""
    shape_points = {"rock": 1, "paper": 2, "scissors": 3}
    game_points = {"X": 0, "Y": 3, "Z": 6}
    shape_to_play = {
        "A X": "scissors",
        "A Y": "rock",
        "A Z": "paper",
        "B X": "rock",
        "B Y": "paper",
        "B Z": "scissors",
        "C X": "paper",
        "C Y": "scissors",
        "C Z": "rock",
    }
    for game_line in text.splitlines():
        _, your_strategy = game_line.split(" ")
        your_shape = shape_to_play[game_line]
        yield game_points[your_strategy] + shape_points[your_shape]


def solve(text: str) -> int:
    """Solve the puzzle."""
    return sum(list(rock_paper_scissors(text)))


INPUT_S = """\
A Y
B X
C Z
"""


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((INPUT_S, 12),),
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
