"""Day 16 part 1 solution."""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import pytest

INPUT_TXT = Path(__file__).parent / "input.txt"


@dataclass
class Packet:
    """Base class for packet."""

    version: int
    type_id: int
    start: int


@dataclass
class Operator(Packet):
    """Child class for operator packet."""

    length_type_id: str
    n: int
    packets: list[Packet]

    def is_done(self, i: int) -> bool:
        """Check whether operators actions are completed."""
        if self.length_type_id == "0":
            return i > self.start + self.n + 22  # 22 = 6 for header + 1 for length type id + 15 for length code
        else:
            return len(self.packets) == self.n


@dataclass
class LiteralValue(Packet):
    """Child class for literal value packet."""

    decoded_value: str

    @property
    def value(self) -> int:
        """Binary to decimal transform."""
        return int(self.decoded_value, 2)


def hex_to_binary(hex_str: str) -> str:
    """Convert a hex string to a binary string."""
    # [2:] so that the '0b' prefix is removed
    # zfill because https://stackoverflow.com/a/4859937/5048095
    n_bits = len(hex_str) * 4
    return bin(int(hex_str, 16))[2:].zfill(n_bits)


def active_operator(operators: list[Operator], i: int) -> Operator | None:
    """Get the currently active operator."""
    for o in operators[::-1]:
        if not o.is_done(i):
            return o
    return None


def read_transmission(binary_str: str) -> int:
    """Read the transmission."""
    i = 0
    packets: list[LiteralValue | Operator] = []
    operators: list[Operator] = []

    while i == 0 or active_operator(operators, i + 1) is not None:
        packet_start = i
        version, type_id = int(binary_str[i : i + 3], 2), int(binary_str[i + 3 : i + 6], 2)
        i += 6
        if type_id == 4:
            decoded_message = binary_str[i + 1 : i + 5]
            while binary_str[i] == "1":
                i += 5
                decoded_message += binary_str[i + 1 : i + 5]
            i += 5
            lv = LiteralValue(version, type_id, packet_start, decoded_message)
            packets.append(lv)
            operator = active_operator(operators, i)
            if operator is not None:
                operator.packets.append(lv)
        else:
            length_type_id = binary_str[i]
            i += 1
            old_operator = active_operator(operators, i)
            if length_type_id == "0":
                n = int(binary_str[i : i + 15], 2)  # N characters
                i += 15
            else:
                n = int(binary_str[i : i + 11], 2)  # N sub-packets
                i += 11
            new_operator = Operator(version, type_id, packet_start, length_type_id, n, [])
            operators.append(new_operator)
            packets.append(new_operator)
            if old_operator is not None:
                old_operator.packets.append(new_operator)
    total_packets = 0
    for op in operators:
        total_packets += len(op.packets)
        print(op.version, op.start, op.start + op.n + 22, op.length_type_id, op.n, len(op.packets))
    print(i, total_packets, len(packets))
    return sum([p.version for p in packets])


def solve(text: str) -> int:
    """Solve the puzzle."""
    binary_string = hex_to_binary(text)
    version_sum = read_transmission(binary_string)
    return version_sum


@pytest.mark.parametrize(
    ("input_s", "expected"),
    (
        ("D2FE28", 6),
        ("8A004A801A8002F478", 16),
        ("620080001611562C8802118E34", 12),
        ("C0015000016115A2E0802F182340", 23),
        ("A0016C880162017C3686B18A3D4780", 31),
    ),
)
def test(input_s: str, expected: int) -> None:
    """Check that the solution is correct."""
    assert solve(input_s) == expected


@pytest.mark.parametrize(
    ("input_s", "expected"),
    (
        ("D2FE28", "110100101111111000101000"),
        ("EE00D40C823060", "11101110000000001101010000001100100000100011000001100000"),
        ("38006F45291200", "00111000000000000110111101000101001010010001001000000000"),
    ),
)
def test_hex_to_binary(input_s: str, expected: int) -> None:
    """Check that the solution is correct."""
    assert hex_to_binary(input_s) == expected


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
