"""Day 12 part 1 solution."""
import argparse
from collections import defaultdict
from pathlib import Path
from typing import (
    Dict,
    Iterator,
    Set,
    Tuple,
)

import pytest

INPUT_TXT = Path(__file__).parent / "input.txt"


def parse(text: str) -> Iterator[Tuple[str, str]]:
    """Parse the input."""
    for line in text.splitlines():
        start, end = line.split("-")
        yield start, end


def create_graph(text: str) -> Dict[str, Set[str]]:
    """Create a graph from the input."""
    graph = defaultdict(set)
    for start, end in list(parse(text)):
        graph[start].add(end)
        graph[end].add(start)
    return graph


def walk_graph(graph: Dict[str, Set[str]], position: str, small_caves_visited: Set[str]) -> int:
    """Walk the graph."""
    if position in small_caves_visited:
        return 0
    elif position == "end":
        return 1
    else:
        if position.islower():
            small_caves_visited.add(position)
        to_visit = graph[position] - small_caves_visited
        n_paths = 0
        for next_position in to_visit:
            n_paths += walk_graph(graph, next_position, small_caves_visited.copy())
        return n_paths


def solve(text: str) -> int:
    """Solve the puzzle."""
    graph = dict(create_graph(text))
    return walk_graph(graph, "start", set())


INPUT_S1 = """\
start-A
start-b
A-c
A-b
b-d
A-end
b-end
"""

INPUT_S2 = """\
dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc
"""

INPUT_S3 = """\
fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW
"""


@pytest.mark.parametrize(
    ("input_s", "expected"),
    (
        (INPUT_S1, 10),
        (INPUT_S2, 19),
        (INPUT_S3, 226),
    ),
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
