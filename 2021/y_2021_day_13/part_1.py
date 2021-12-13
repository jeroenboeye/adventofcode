"""Day 13 part 1 solution."""
import argparse
from pathlib import Path
from typing import (
    Iterator,
    List,
    Set,
    Tuple,
)

import pytest

Coord = Tuple[int, int]
INPUT_TXT = Path(__file__).parent / "input.txt"


def parse_coords(text: str) -> Iterator[Coord]:
    """Parse the input."""
    for coord in text.splitlines():
        x, y = coord.split(",")
        yield int(x), int(y)


def parse_instructions(text: str) -> Iterator[Tuple[str, int]]:
    """Parse the input."""
    for line in text.splitlines():
        direction, position = line.lstrip("fold along ").split("=")
        yield direction, int(position)


def parse_input(text: str) -> Tuple[Set[Coord], List[Tuple[str, int]]]:
    """Parse the input."""
    coords_raw, instructions_raw = text.split("\n\n")
    coords = set(parse_coords(coords_raw))
    instructions = list(parse_instructions(instructions_raw))
    return coords, instructions


def fold(coords: Set[Coord], direction: str, position: int) -> Set[Coord]:
    """Fold the coordinates along the given direction."""
    new_coords = set()
    if direction == "x":
        for x, y in coords:
            if x > position:
                new_coords.add((2 * position - x, y))
            elif x < position:
                new_coords.add((x, y))
    elif direction == "y":
        for x, y in coords:
            if y > position:
                new_coords.add((x, 2 * position - y))
            elif y < position:
                new_coords.add((x, y))
    return new_coords


def solve(text: str) -> int:
    """Solve the puzzle."""
    coords, instructions = parse_input(text)
    direction, position = instructions[0]
    coords = fold(coords, direction, position)
    return len(coords)


INPUT_S = """\
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
"""


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((INPUT_S, 17),),
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
