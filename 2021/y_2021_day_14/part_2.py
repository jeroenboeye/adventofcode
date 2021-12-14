"""Day 14 part 2 solution."""
import argparse
from collections import defaultdict
from pathlib import Path
from typing import (
    Dict,
    List,
    Tuple,
)

import pytest

INPUT_TXT = Path(__file__).parent / "input.txt"
Count = Dict[str, int]


def parse_input(text: str) -> Tuple[List[str], Dict[str, str]]:
    """Parse the input."""
    polymer_raw, reactions_raw = text.split("\n\n")
    polymer = [x for x in polymer_raw]
    reactions = {k: v for k, v in [x.split(" -> ") for x in reactions_raw.splitlines()]}
    return polymer, reactions


def update_dimers(dimers: Count, reactions: Dict[str, str]) -> Count:
    """Perform monomer insertion and update the dimer counts."""
    for dimer, count in dimers.copy().items():
        dimers[dimer] -= count
        dimers[dimer[0] + reactions[dimer]] += count
        dimers[reactions[dimer] + dimer[1]] += count
    if min(dimers.values()) < 0:
        raise ValueError("Negative count")
    return dimers


def polymer_to_dimer_count(polymer: List[str]) -> Count:
    """Count the number of times each monomer appears in the polymer."""
    dimers: Dict[str, int] = defaultdict(int)
    for i, monomer in enumerate(polymer):
        if i == 0:
            continue
        dimers[polymer[i - 1] + monomer] += 1
    return dimers


def dimer_to_monomer_count(dimers: Count, first: str, last: str) -> Count:
    """Count the number of times each monomer appears in the dimers."""
    monomers: Dict[str, float] = defaultdict(int)
    monomers[first] = 0.5
    monomers[last] = 0.5
    for dimer, count in dimers.items():
        for monomer in dimer:
            monomers[monomer] += count / 2
    return {k: int(v) for k, v in monomers.items()}


def solve(text: str) -> int:
    """Solve the puzzle."""
    polymer, reactions = parse_input(text)
    dimers = polymer_to_dimer_count(polymer)
    for _ in range(40):
        dimers = update_dimers(dimers, reactions)
    monomers = dimer_to_monomer_count(dimers, polymer[0], polymer[-1])
    return max(monomers.values()) - min([v for v in monomers.values() if v > 0])


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
    ((INPUT_S, 2188189693529),),
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
def test_reaction(input_s: str, iteration: int, expected: str) -> None:
    """Check that the solution is correct."""
    polymer, reactions = parse_input(input_s)
    expected_polymer = [x for x in expected]

    dimers = polymer_to_dimer_count(polymer)
    for _ in range(iteration):
        dimers = update_dimers(dimers, reactions)

    dimers_no_zeros = {k: v for k, v in dimers.items() if v > 0}
    expected_dict = dict(polymer_to_dimer_count(expected_polymer))

    assert dimers_no_zeros == expected_dict


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
