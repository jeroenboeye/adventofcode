"""Day 24 part 1 solution."""

import argparse
from pathlib import Path
from typing import Dict, Tuple

import pytest

INPUT_TXT = Path(__file__).parent / "input.txt"
CubeCoord = Tuple[int, int, int]
direction_effects = {
    "ne": (1, 0, -1),
    "e": (1, -1, 0),
    "se": (0, -1, 1),
    "sw": (-1, 0, 1),
    "w": (-1, 1, 0),
    "nw": (0, 1, -1),
}


def solve(text: str) -> int:
    """Solves the puzzle.

    Directions are e, se, sw, w, nw, and ne
    """
    tile_black: Dict[CubeCoord, bool] = {}
    for line in text.splitlines():
        compound_direction = False
        coord: CubeCoord = (0, 0, 0)
        for c in line:
            if c in "sn":
                compound_direction = True
                direction = c
            elif not compound_direction:
                direction = c
            else:
                direction += c
                compound_direction = False
            if not compound_direction:
                effect = direction_effects[direction]
                coord = tuple(map(sum, zip(coord, effect)))  # type: ignore
        if not tile_black.get(coord, False):
            tile_black[coord] = True
        else:
            tile_black[coord] = False
    return int(sum(tile_black.values()))


INPUT_S = """\
sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew
"""


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((INPUT_S, 10),),
)
def test(input_s: str, expected: int) -> None:
    """Check that the solution is correct."""
    assert solve(input_s) == expected


def main() -> int:
    """Run the solution."""
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", nargs="?", default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(solve(f.read()))

    return 0


if __name__ == "__main__":
    exit(main())
