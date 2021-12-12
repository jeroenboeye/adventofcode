"""Day 24 part 2 solution."""
import argparse
from pathlib import Path
from typing import (
    Dict,
    Set,
    Tuple,
)

import pytest

INPUT_TXT = Path(__file__).parent / "input.txt"
CubeCoord = Tuple[int, int, int]
direction_effects: Dict[str, CubeCoord] = {
    "ne": (1, 0, -1),
    "e": (1, -1, 0),
    "se": (0, -1, 1),
    "sw": (-1, 0, 1),
    "w": (-1, 1, 0),
    "nw": (0, 1, -1),
}


def get_initial_black_tiles(text: str) -> Set[CubeCoord]:
    """Get the initial black tile coordinates.

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
    return {k for k, v in tile_black.items() if v}


def get_neigbors(coord: CubeCoord) -> Set[CubeCoord]:
    """Get the neigbors of a cube coord."""
    return {tuple(map(sum, zip(coord, effect))) for effect in direction_effects.values()}  # type: ignore


def get_white_neigbor_tiles(black_tiles: Set[CubeCoord]) -> Set[CubeCoord]:
    """Get white tiles that neighbor the black tiles."""
    white_tiles = set()
    for tile in black_tiles:
        neigbors = get_neigbors(tile)
        white_tiles.update(neigbors - black_tiles)
    return white_tiles


def n_neigbor_black_tiles(tile: CubeCoord, black_tiles: Set[CubeCoord]) -> int:
    """Get the number of black tiles that are neighbors of a white tile."""
    return len(get_neigbors(tile).intersection(black_tiles))


def solve(text: str) -> int:
    """Solves the puzzle.

    Directions are e, se, sw, w, nw, and ne
    """
    black_tiles = get_initial_black_tiles(text)
    for _ in range(100):
        white_tiles = get_white_neigbor_tiles(black_tiles)
        new_black_tiles = {tile for tile in black_tiles if 0 < n_neigbor_black_tiles(tile, black_tiles) < 3}
        new_black_tiles.update(tile for tile in white_tiles if n_neigbor_black_tiles(tile, black_tiles) == 2)
        black_tiles = new_black_tiles.copy()
    return len(black_tiles)


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
    ((INPUT_S, 2208),),
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
