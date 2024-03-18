"""Day 12 part 2 solution."""

import argparse
from collections import defaultdict
from pathlib import Path
from string import ascii_lowercase
from typing import Iterator, TypeAlias

import pytest

INPUT_TXT = Path(__file__).parent / "input.txt"

coord: TypeAlias = tuple[int, int]  # x, y coord


def get_start_and_end_coords(text: str) -> tuple[coord, coord]:
    """Get start and end coords."""
    x_start, y_start = -1, -1
    x_end, y_end = -1, -1
    for y, line in enumerate(text.splitlines()):
        if "S" in line:
            x_start = line.find("S")
            y_start = y
        if "E" in line:
            x_end = line.find("E")
            y_end = y
    return (x_start, y_start), (x_end, y_end)


def parse(text: str) -> Iterator[list[int]]:
    """Parse letter map to int height."""
    text = text.replace("S", "a").replace("E", "z")
    for line in text.splitlines():
        yield [ascii_lowercase.index(c) for c in line]


def build_graph(height_map: list[list[int]]) -> dict[coord, set[coord]]:
    """Create graph of possible next positions to visit from each coord."""
    graph: dict[coord, set[coord]] = defaultdict(set)
    for y, line in enumerate(height_map):
        for x, height in enumerate(line):
            for delta in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                if 0 <= y + delta[1] < len(height_map) and 0 <= x + delta[0] < len(line):
                    if height - height_map[y + delta[1]][x + delta[0]] <= 1:
                        graph[(x, y)].add((x + delta[0], y + delta[1]))
    return graph


def shortest_path(graph: dict[coord, set[coord]], start_coord: coord, end_coords: set[coord]) -> list[coord]:
    """Find shortest path using breadth first search (BFS)."""
    path_list = [[start_coord]]
    path_index = 0
    visited = {start_coord}

    while path_index < len(path_list):
        current_path = path_list[path_index]
        last_node = current_path[-1]
        neighbors = graph[last_node]
        # Check if end reached
        if not end_coords.isdisjoint(neighbors):
            current_path.append((end_coords & neighbors).pop())
            return current_path
        # Add new paths
        for next_node in neighbors:
            if next_node not in visited:
                new_path = current_path[:]  # copy
                new_path.append(next_node)
                path_list.append(new_path)
                # To avoid backtracking
                visited.add(next_node)
        # Continue to next path in list
        path_index += 1
    return []


def get_low_points(height_map: list[list[int]]) -> set[coord]:
    """Get the coordinates of all the lowest points."""
    low_points: set[coord] = set()
    for y, line in enumerate(height_map):
        for x, height in enumerate(line):
            if height == 0:
                low_points.add((x, y))
    return low_points


def solve(text: str) -> int:
    """Solve the puzzle."""
    _, end_coord = get_start_and_end_coords(text)
    height_map = list(parse(text))
    graph = build_graph(height_map)

    low_points = get_low_points(height_map)
    path = shortest_path(graph, end_coord, low_points)
    # print(path)
    return len(path) - 1


INPUT_S = """\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
"""
EXPECTED = 29


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
