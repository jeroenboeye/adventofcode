"""Day 10 part 2 solution."""

import argparse
from pathlib import Path
from typing import Dict, List

import pytest

INPUT_TXT = Path(__file__).parent / "input.txt"
OPPOSITE_BRACKETS = {")": "(", "}": "{", "]": "[", ">": "<"}
COMPLETE_VALUES: Dict[str, int] = {
    "(": 1,
    "[": 2,
    "{": 3,
    "<": 4,
}


def score_remaining_brackets(brackets: List[str]) -> int:
    """Score the remaining brackets."""
    total_value = 0
    for bracket in brackets[::-1]:
        total_value *= 5
        total_value += COMPLETE_VALUES[bracket]
    return int(total_value)


def solve(text: str) -> int:
    """Solve the puzzle."""
    values = []
    for line in text.splitlines():
        open_brackets = []
        corrupt = False
        for char in line:
            if char in "({[<":
                open_brackets.append(char)
            else:
                if open_brackets[-1] == OPPOSITE_BRACKETS[char]:
                    open_brackets.pop()
                else:
                    corrupt = True
                    break
        if not corrupt:
            values.append(score_remaining_brackets(open_brackets))
    return sorted(values)[len(values) // 2]


INPUT_S = """\
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
"""


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((INPUT_S, 288957),),
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
