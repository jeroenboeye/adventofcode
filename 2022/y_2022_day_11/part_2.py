"""Day 11 part 2 solution."""

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterator

import pytest

INPUT_TXT = Path(__file__).parent / "input.txt"


@dataclass
class Monkey:
    """Monkey business."""

    id: int
    items: list[int]
    operation: Callable
    divisor: int
    true_target_id: int
    false_target_id: int
    inspection_count: int = 0

    def find_target_monkey(self, x: int) -> int:
        """Find a monkey to throw item to."""
        if x % self.divisor == 0:
            return self.true_target_id
        else:
            return self.false_target_id


def create_operator(ops_str: str) -> Callable:
    """Create operation function from string."""

    def operation(old: int) -> int:
        """Perform monkey operation."""
        return int(eval(ops_str))

    return operation


def parse(text: str) -> Iterator[Monkey]:
    """Parse monkey text."""
    for block in text.split("\n\n"):
        l0, l1, l2, l3, l4, l5 = block.splitlines()
        money_id = int(re.findall(r"\d+", l0)[0])
        items = [int(x) for x in re.findall(r"\d+", l1)]
        operation = create_operator(l2.split(" = ")[1])
        divisor = int(re.findall(r"\d+", l3)[0])
        true_target_id = int(re.findall(r"\d+", l4)[0])
        false_target_id = int(re.findall(r"\d+", l5)[0])
        yield Monkey(money_id, items, operation, divisor, true_target_id, false_target_id)


def solve(text: str) -> int:
    """Solve the puzzle."""
    monkeys = list(parse(text))
    monkey_divisor_multiple = 1
    for m in monkeys:
        monkey_divisor_multiple *= m.divisor
    for _ in range(10_000):
        for monkey in monkeys:
            while monkey.items:
                monkey.inspection_count += 1
                new_score = monkey.operation(monkey.items.pop(0))
                new_score %= monkey_divisor_multiple
                target = monkey.find_target_monkey(new_score)
                monkeys[target].items.append(new_score)
    m1, m2 = sorted([m.inspection_count for m in monkeys])[-2:]
    return m1 * m2


INPUT_S = """\
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
"""
EXPECTED = 2713310158


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
    # solution = solve(INPUT_S)
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
