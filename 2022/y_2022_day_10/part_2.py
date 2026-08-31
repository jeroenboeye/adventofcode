"""Day 10 part 2 solution."""

import argparse
import textwrap
from pathlib import Path

INPUT_TXT = Path(__file__).parent / "input.txt"


def draw_pixel(x: int, cycle: int) -> str:
    """Draw a pixel on the CRT."""
    if abs(x - cycle % 40) < 2:
        return "#"
    else:
        return "."


def solve(text: str) -> str:
    """Solve the puzzle."""
    cycle = 0
    x = 1
    output = ""
    for line in text.splitlines():
        if line == "noop":
            output += draw_pixel(x, cycle)
            cycle += 1
        else:
            _, value = line.split()
            output += draw_pixel(x, cycle)
            cycle += 1
            output += draw_pixel(x, cycle)
            cycle += 1
            x += int(value)

    return "\n".join(textwrap.wrap(output, 40))


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
