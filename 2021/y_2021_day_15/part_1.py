"""Day 15 part 1 solution."""

import argparse
from pathlib import Path
from typing import Dict, List, Tuple

import pytest

from aoc.compute import dijkstra
from aoc.parsers import unspaced_text_to_2d_list

INPUT_TXT = Path(__file__).parent / "input.txt"
Coord = Tuple[int, int]


def build_graph(list_2d: List[List[int]]) -> Dict[Coord, Dict[Coord, int]]:
    """Build a graph from the input text."""
    graph: Dict[Coord, Dict[Coord, int]] = {}
    for y, row in enumerate(list_2d):
        for x, _ in enumerate(row):
            graph[(x, y)] = {}
            if x > 0:
                graph[(x, y)][(x - 1, y)] = int(row[x - 1])
            if x + 1 < len(row):
                graph[(x, y)][(x + 1, y)] = int(row[x + 1])
            if y > 0:
                graph[(x, y)][(x, y - 1)] = int(list_2d[y - 1][x])
            if y + 1 < len(list_2d):
                graph[(x, y)][(x, y + 1)] = int(list_2d[y + 1][x])
    return graph


def solve(text: str) -> int:
    """Solve the puzzle."""
    list_2d = unspaced_text_to_2d_list(text, int)
    graph = build_graph(list_2d)
    _, node_costs = dijkstra(graph, (0, 0))
    return int(node_costs[(len(list_2d[0]) - 1, len(list_2d) - 1)])


INPUT_S = """\
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
"""


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((INPUT_S, 40),),
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
