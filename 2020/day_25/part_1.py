"""Day 25 part 1 solution."""
import argparse
from pathlib import Path

import pytest

INPUT_TXT = Path(__file__).parent / "input.txt"


def handshake(subject_nr: int, loop_size: int) -> int:
    """Perform full cryptographic handshake, result is private key."""
    value = 1
    for _ in range(loop_size):
        value = transform_subject_nr(value, subject_nr)
    return value


def transform_subject_nr(value: int, subject_nr: int) -> int:
    """Transform a subject number in context of a cryptographic handshake."""
    value *= subject_nr
    value = value % 20201227
    return value


def find_secret_loop_size(public_key: int) -> int:
    """Find the secret loop size of a handshake."""
    value = 1
    loop_size = 0
    while value != public_key:
        value = transform_subject_nr(value, 7)
        loop_size += 1
    return loop_size


def solve(text: str) -> int:
    """Solve the puzzle."""
    card_pub_key, door_pub_key = [int(x) for x in text.splitlines()]
    card_loop_size = find_secret_loop_size(card_pub_key)
    key = handshake(door_pub_key, card_loop_size)
    return key


INPUT_S = """\
5764801
17807724
"""


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((INPUT_S, 14897079),),
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
        # Derive day from parent directory name, dirname should end in e.g. _01
        day = int(Path(__file__).parent.absolute().name.split("_")[1])
        submit(solution, year=2020, day=day)

    return 0


if __name__ == "__main__":
    exit(main())
