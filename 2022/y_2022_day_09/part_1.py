"""Day 9 part 1 solution."""
import argparse
from pathlib import Path
from typing import Iterator, TypeAlias

import pytest

INPUT_TXT = Path(__file__).parent / "input.txt"

coord: TypeAlias = tuple[int, int]  # x, y coord


def parse(text: str) -> Iterator[tuple[str, int]]:
    """Get direction and distance from text input."""
    for line in text.splitlines():
        direction, distance = line.split()
        yield direction, int(distance)


def move_head(head_coord: coord, direction: str) -> coord:
    """Move the head one step in the given direction."""
    match direction:
        case "R":
            return head_coord[0] + 1, head_coord[1]
        case "L":
            return head_coord[0] - 1, head_coord[1]
        case "U":
            return head_coord[0], head_coord[1] + 1
        case "D":
            return head_coord[0], head_coord[1] - 1
        case _:
            raise ValueError(f"Unknown direction: {direction}")


def move_tail(tail_coord: coord, deltas: coord) -> coord:
    """Move a tail according to elven rope physics."""

    def delta_to_distance(d: int) -> int:
        if d > 0:
            return 1
        elif d < 0:
            return -1
        else:
            return 0

    if max(deltas) < 2 and -2 < min(deltas):
        return tail_coord
    return tail_coord[0] + delta_to_distance(deltas[0]), tail_coord[1] + delta_to_distance(deltas[1])


def solve(text: str) -> int:
    """Solve the puzzle."""
    head_coord, tail_coord = (0, 0), (0, 0)
    tail_history = {tail_coord}
    for direction, distance in parse(text):
        for _ in range(distance):
            head_coord = move_head(head_coord, direction)
            deltas = head_coord[0] - tail_coord[0], head_coord[1] - tail_coord[1]
            tail_coord = move_tail(tail_coord, deltas)
            tail_history.add(tail_coord)
    return len(tail_history)


INPUT_S = """\
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
"""
EXPECTED = 13


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
