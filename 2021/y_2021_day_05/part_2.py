"""Day 5 part 2 solution."""

import argparse
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import pytest

INPUT_TXT = Path(__file__).parent / "input.txt"
Coord = Tuple[int, int]


def coord_parser(text: str) -> Coord:
    """Parse the input to coord."""
    x, y = [int(x) for x in text.split(",")]
    return (x, y)


def line_parser(text: str) -> Iterable[Tuple[Coord, Coord]]:
    """Parse the input."""
    for line in text.splitlines():
        start_coord, end_coord = [coord_parser(x) for x in line.split(" -> ")]
        yield (start_coord, end_coord)


def end_coords_to_line(coord_pair: Tuple[Coord, Coord]) -> List[Coord]:
    """Parse the input."""
    x_delta = coord_pair[1][0] - coord_pair[0][0]
    y_delta = coord_pair[1][1] - coord_pair[0][1]
    line_length = max(abs(x_delta), abs(y_delta))
    line = []
    for i in range(line_length + 1):
        x = coord_pair[0][0] + i * (x_delta // line_length)
        y = coord_pair[0][1] + i * (y_delta // line_length)
        line.append((x, y))
    return line


def solve(text: str) -> int:
    """Solve the puzzle."""
    coord_pairs: List[Tuple[Coord, Coord]] = list(line_parser(text))
    vent_dict: Dict[Coord, int] = {}
    for cp in coord_pairs:
        line = end_coords_to_line(cp)
        for coord in line:
            vent_dict[coord] = vent_dict.get(coord, 0) + 1
    return len([v for v in vent_dict.values() if v > 1])


INPUT_S = """\
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
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
