"""Day 13 part 2 solution."""
import argparse
from pathlib import Path
from typing import (
    Iterator,
    List,
    Set,
    Tuple,
)

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


def print_solution(coords: Set[Coord]) -> None:
    """Print the solution."""
    max_x = max(x for x, _ in coords)
    max_y = max(y for _, y in coords)

    # Empty printlines
    print_line = ["." for _ in range(max_x + 1)]
    printout = [print_line.copy() for _ in range(max_y + 1)]

    # Fill in the coordinates
    for x, y in coords:
        printout[y][x] = "#"

    # Print
    for line in printout:
        print("".join(line))


def solve(text: str) -> None:
    """Solve the puzzle."""
    coords, instructions = parse_input(text)
    for direction, position in instructions:
        coords = fold(coords, direction, position)
    print_solution(coords)


def main() -> int:
    """Run the solution."""
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", nargs="?", default=INPUT_TXT)

    args = parser.parse_args()

    with open(args.data_file) as f:
        solve(f.read())
    return 0


if __name__ == "__main__":
    exit(main())
