"""Day 11 part 1 solution."""
import argparse
from pathlib import Path
from typing import Iterator, Set, Tuple

import pytest

Coord = Tuple[int, int]
INPUT_TXT = Path(__file__).parent / "input.txt"


def parse(text: str) -> Iterator[Tuple[Coord, int]]:
    """Parse the input."""
    for y, line in enumerate(text.splitlines()):
        for x, value in enumerate(line):
            yield (x, y), int(value)


def neighbors(x: int, y: int, max_x: int, max_y: int, min_x: int = 0, min_y: int = 0) -> Iterator[Coord]:
    """Return the neighbors of a coordinate."""
    for x2 in range(x - 1, x + 2):
        for y2 in range(y - 1, y + 2):
            if (x2, y2) != (x, y) and min_x <= x2 <= max_x and min_y <= y2 <= max_y:
                yield x2, y2


def solve(text: str) -> int:
    """Solve the puzzle."""
    coord_to_energy = dict(parse(text))
    all_coords = set(coord_to_energy.keys())
    max_x = max(x for x, _ in all_coords)
    max_y = max(y for _, y in all_coords)
    total_flashed = 0
    for _ in range(100):
        coord_to_energy = {k: v + 1 for k, v in coord_to_energy.items()}
        flashed: Set[Coord] = set()
        while len(flashed) != len([energy for energy in coord_to_energy.values() if energy > 9]):
            for coord in all_coords - flashed:
                if coord_to_energy[coord] > 9:
                    flashed.add(coord)
                    for neighbor in list(neighbors(*coord, max_x, max_y)):
                        coord_to_energy[neighbor] += 1
        coord_to_energy = {k: (v if v <= 9 else 0) for k, v in coord_to_energy.items()}
        total_flashed += len(flashed)
    return total_flashed


INPUT_S = """\
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
"""


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((INPUT_S, 1656),),
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
