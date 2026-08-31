"""Day 7 part 2 solution."""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from pathlib import Path

import pytest

INPUT_TXT = Path(__file__).parent / "input.txt"


@dataclass
class Dir:
    """Directory class does directory things."""

    name: str
    parent: Dir | None
    subdirs: dict[str, Dir] = field(default_factory=dict)
    files: dict[str, int] = field(default_factory=dict)

    @property
    def size(self) -> int:
        """Get the size of the dir by summing the sizes of its contents."""
        return sum(self.files.values()) + sum([dir.size for dir in self.subdirs.values()])

    def add_subdir(self, subdir_name: str) -> None:
        """Add a subdir if it does not yet exist."""
        if subdir_name not in self.subdirs.keys():
            self.subdirs[subdir_name] = Dir(subdir_name, self)

    def add_file(self, file_name: str, file_size: int) -> None:
        """Add a file if it does not yet exist."""
        if file_name not in self.files.keys():
            self.files[file_name] = file_size


def smallest_size_big_enough(dir: Dir, minimal_size: int, current_closest: int) -> int:
    """Get the size of the smallest directory big enough to free up needed space."""
    if minimal_size < dir.size < current_closest:
        current_closest = dir.size
    if dir.size < minimal_size:
        return current_closest
    if len(dir.subdirs):
        closest_subdir = min([smallest_size_big_enough(d, minimal_size, current_closest) for d in dir.subdirs.values()])
        if closest_subdir < current_closest:
            current_closest = closest_subdir
    return current_closest


def solve(text: str) -> int:
    """Solve the puzzle."""
    list_output = False
    current_dir = Dir(name="/", parent=None)
    for line in text.splitlines():
        commands = line.split()
        if commands[0] == "$":
            if list_output:
                list_output = False
            if commands[1] == "cd":
                if commands[2] == "/":
                    continue
                elif commands[2] == ".." and current_dir.parent is not None:
                    current_dir = current_dir.parent
                else:
                    current_dir = current_dir.subdirs[commands[2]]
            if commands[1] == "ls":
                list_output = True
        else:
            if commands[0] == "dir":
                current_dir.add_subdir(commands[1])
            else:
                current_dir.add_file(commands[1], int(commands[0]))

    # move to root
    while current_dir.parent is not None:
        current_dir = current_dir.parent

    system_size = 70_000_000
    free_size_needed = 30_000_000
    current_free_size = system_size - current_dir.size
    minimal_size_to_delete = free_size_needed - current_free_size

    return smallest_size_big_enough(current_dir, minimal_size_to_delete, system_size)


INPUT_S = """\
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""
EXPECTED = 24933642


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
