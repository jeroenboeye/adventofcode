"""Day 9 part 2 solution."""
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


def move_knot(tail_coord: coord, deltas: coord) -> coord:
    """Move a knot according to elven rope physics."""

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


def move_rope(rope: list[coord], direction: str) -> Iterator[coord]:
    """Iterate over the rope and move the knots."""
    previous_knot = rope[0]
    for i, knot in enumerate(rope):
        if i == 0:
            previous_knot = move_head(knot, direction)
            yield previous_knot
        else:
            deltas = previous_knot[0] - knot[0], previous_knot[1] - knot[1]
            previous_knot = move_knot(knot, deltas)
            yield previous_knot


def solve(text: str) -> int:
    """Solve the puzzle."""
    rope: list[coord] = [(0, 0) for _ in range(10)]
    tail_history = {rope[-1]}
    for direction, distance in parse(text):
        for _ in range(distance):
            rope = list(move_rope(rope, direction))
            tail_history.add(rope[-1])
    return len(tail_history)


INPUT_S_1 = """\
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
"""
EXPECTED_1 = 1

INPUT_S_2 = """\
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
"""
EXPECTED_2 = 36


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((INPUT_S_1, EXPECTED_1), (INPUT_S_2, EXPECTED_2)),
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
