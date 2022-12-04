"""Day 15 part 2 solution."""
import argparse
from pathlib import Path
from typing import Dict, List, Tuple

import pytest

from aoc.compute import dijkstra
from aoc.parsers import unspaced_text_to_2d_list

INPUT_TXT = Path(__file__).parent / "input.txt"
Coord = Tuple[int, int]


def build_graph(list_2d: List[List[int]]) -> Dict[Coord, Dict[Coord, int]]:
    """
    Build a graph from the input text.

    The graph maps coordinates to neighbor coordinates and their values.
    """
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


def wrap_around_nine(x: int) -> int:
    """Set values larger than 9 to x % 9."""
    if x > 9:
        return x % 9
    else:
        return x


def extrapolate_map(list_2d: List[List[int]]) -> List[List[int]]:
    """Extrapolate the map in two directions."""
    # Extrapolate to the right
    wide_list_2d = []
    for row in list_2d:
        wide_list_2d.append([wrap_around_nine(v + i) for i in range(5) for v in row])

    new_list_2d = []
    # Extrapolate to the bottom
    for i in range(5):
        for row in wide_list_2d:
            new_list_2d.append([wrap_around_nine(v + i) for v in row])
    return new_list_2d


def solve(text: str) -> int:
    """Solve the puzzle."""
    list_2d = extrapolate_map(unspaced_text_to_2d_list(text, int))
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
    ((INPUT_S, 315),),
)
def test(input_s: str, expected: int) -> None:
    """Check that the solution is correct."""
    assert solve(input_s) == expected


@pytest.mark.parametrize(
    ("input_s"),
    ((INPUT_S),),
)
def test_map_extrapolation(input_s: str) -> None:
    """Check the map is correctly exptrapolated."""
    list_2d = extrapolate_map(unspaced_text_to_2d_list(input_s, int))
    expected_top_row = unspaced_text_to_2d_list("11637517422274862853338597396444961841755517295286", int)[0]
    expected_bottom_row = unspaced_text_to_2d_list("67554889357866599146897761125791887223681299833479", int)[0]
    assert list_2d[0] == expected_top_row
    assert list_2d[-1] == expected_bottom_row


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
