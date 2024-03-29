"""Day 14 part 1 solution."""
import argparse
from collections import Counter
from pathlib import Path
from typing import Dict, Iterator, List, Tuple

import pytest

INPUT_TXT = Path(__file__).parent / "input.txt"


def parse_input(text: str) -> Tuple[List[str], Dict[str, str]]:
    """Parse the input."""
    polymer_raw, reactions_raw = text.split("\n\n")
    polymer = [x for x in polymer_raw]
    reactions = {k: v for k, v in [x.split(" -> ") for x in reactions_raw.splitlines()]}
    return polymer, reactions


def grow_polymer(polymer: List[str], reactions: Dict[str, str]) -> Iterator[str]:
    """Grow the polymer by inserting elements."""
    for i, monomer in enumerate(polymer):
        if i == 0:
            yield monomer
            continue
        yield reactions[polymer[i - 1] + monomer]
        yield monomer


def solve(text: str) -> int:
    """Solve the puzzle."""
    polymer, reactions = parse_input(text)
    for _ in range(10):
        polymer = list(grow_polymer(polymer, reactions))
    # Returns a sorted list of tuples: [(letter, count), ...]
    sorted_counts = Counter(polymer).most_common()
    return sorted_counts[0][1] - sorted_counts[-1][1]


INPUT_S = """\
NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
"""


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((INPUT_S, 1588),),
)
def test(input_s: str, expected: int) -> None:
    """Check that the solution is correct."""
    assert solve(input_s) == expected


@pytest.mark.parametrize(
    ("input_s", "iteration", "expected"),
    (
        (INPUT_S, 1, "NCNBCHB"),
        (INPUT_S, 2, "NBCCNBBBCBHCB"),
        (INPUT_S, 3, "NBBBCNCCNBBNBNBBCHBHHBCHB"),
        (INPUT_S, 4, "NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB"),
    ),
)
def test_reaction(input_s: str, iteration: int, expected: int) -> None:
    """Check that the solution is correct."""
    polymer, reactions = parse_input(input_s)
    for _ in range(iteration):
        polymer = list(grow_polymer(polymer, reactions))

    assert "".join(polymer) == expected


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
