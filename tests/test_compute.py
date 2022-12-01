"""Test compute module."""
import pytest

from aoc.compute import run_intcode

INPUT_S1 = """\
1,0,0,0,99
"""

INPUT_S2 = """\
2,3,0,3,99
"""

INPUT_S3 = """\
2,4,4,5,99,0
"""

INPUT_S4 = """\
1,1,1,4,99,5,6,0,99
"""

INPUT_S5 = """\
1,9,10,3,2,3,11,0,99,30,40,50
"""


@pytest.mark.parametrize(
    ("input_s", "expected"),
    (
        (INPUT_S1, [2, 0, 0, 0, 99]),
        (INPUT_S2, [2, 3, 0, 6, 99]),
        (INPUT_S3, [2, 4, 4, 5, 99, 9801]),
        (INPUT_S4, [30, 1, 1, 4, 2, 5, 6, 0, 99]),
        (INPUT_S5, [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]),
    ),
)
def test_intcode(input_s: str, expected: int) -> None:
    """Check that the solution is correct."""
    code = [int(x) for x in input_s.split(",")]
    assert run_intcode(code) == expected
