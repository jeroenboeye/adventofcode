"""Day 8 part 1 solution."""
import argparse
from pathlib import Path
from typing import (
    Dict,
    Iterator,
    List,
    Set,
    Tuple,
)

import pytest

INPUT_TXT = Path(__file__).parent / "input.txt"

DIGITS = {
    "abcefg": "0",
    "cf": "1",
    "acdeg": "2",
    "acdfg": "3",
    "bcdf": "4",
    "abdfg": "5",
    "abdefg": "6",
    "acf": "7",
    "abcdefg": "8",
    "abcdfg": "9",
}


def parse(text: str) -> Iterator[Tuple[List[Set[str]], List[Set[str]]]]:
    """Parse the input."""
    for line in text.splitlines():
        signal_text, output_text = line.split(" | ")
        signal = [{letter for letter in code} for code in signal_text.split()]
        output = [{letter for letter in code} for code in output_text.split()]
        yield signal, output


def get_cipher(signal: List[Set[str]]) -> Dict[str, str]:
    """Get a cipher that maps encoded letters to decoded ones."""
    mapping = {}
    encoded_one = [code for code in signal if len(code) == 2].pop()
    encoded_four = [code for code in signal if len(code) == 4].pop()
    encoded_seven = [code for code in signal if len(code) == 3].pop()
    encoded_eight = [code for code in signal if len(code) == 7].pop()
    encoded_len_5 = [code for code in signal if len(code) == 5]
    encoded_len_6 = [code for code in signal if len(code) == 6]

    mapping["a"] = encoded_seven - encoded_one
    mapping["g"] = set.intersection(*encoded_len_6) - encoded_four - mapping["a"]
    mapping["d"] = set.intersection(*encoded_len_5) - mapping["a"] - mapping["g"]
    mapping["b"] = encoded_four - encoded_one - mapping["d"]
    mapping["f"] = set.intersection(*encoded_len_6) - mapping["a"] - mapping["b"] - mapping["g"]
    mapping["c"] = encoded_one - mapping["f"]
    mapping["e"] = encoded_eight - encoded_four - mapping["a"] - mapping["g"]

    return {v.pop(): k for k, v in mapping.items()}


def decode(output: List[Set[str]], cipher: Dict[str, str]) -> int:
    """Decode the output."""
    digit_str = ""
    for code in output:
        decoded = "".join(sorted([cipher[letter] for letter in code]))
        digit_str += DIGITS[decoded]
    return int(digit_str)


def solve(text: str) -> int:
    """Solve the puzzle."""
    digit_sum = 0
    for signal, output in parse(text):
        cipher = get_cipher(signal)
        digit_sum += decode(output, cipher)
    return digit_sum


INPUT_S1 = """\
acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf
"""

INPUT_S2 = """\
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
"""


@pytest.mark.parametrize(
    ("input_s", "expected"),
    (
        (INPUT_S1, 5353),
        (INPUT_S2, 61229),
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
        # Derive day from parent directory name, dirname should end in e.g. _01
        day = int(Path(__file__).parent.absolute().name.split("_")[1])
        submit(solution, year=2021, day=day)

    return 0


if __name__ == "__main__":
    exit(main())
