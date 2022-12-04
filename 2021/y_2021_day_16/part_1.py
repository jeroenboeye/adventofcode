"""Day 16 part 1 solution."""
from __future__ import annotations

import argparse
from pathlib import Path

import pytest

INPUT_TXT = Path(__file__).parent / "input.txt"


def split_packet(packet: str) -> tuple[int, int, str]:
    """Return version, type_id, and message."""
    return int(packet[:3], 2), int(packet[3:6], 2), packet[6:]


def decode_literal_value(message: str) -> str:
    """Decode a literal value."""
    print(message)
    if message[0] == "0":
        return message[1:5]
    else:
        return message[1:5] + decode_literal_value(message[5:])


def hex_to_binary(hex_str: str) -> str:
    """Convert a hex string to a binary string."""
    # [2:] so that the '0b' prefix is removed
    # zfill because https://stackoverflow.com/a/4859937/5048095
    n_bits = len(hex_str) * 4
    return bin(int(hex_str, 16))[2:].zfill(n_bits)


def unpack_length_type_0(binary_str: str) -> tuple[int, str, str]:
    """Unpack a binary string of length type 0."""
    length_sub_packages = int(binary_str[:15], 2)
    sub_packages = binary_str[15 : 15 + length_sub_packages]
    remainder = binary_str[15 + length_sub_packages :]
    return length_sub_packages, sub_packages, remainder


def read_transmission(binary_string: str) -> int:
    """Read the transmission."""
    if len(binary_string) == 0 or set(binary_string) == {"0"}:
        return 0

    version, type_id, message = split_packet(binary_string)
    if type_id == 4:
        decoded_message = decode_literal_value(message)
        # message_value = int(decoded_message, 2)
        message_length = 5 * len(decoded_message) // 4
        return version + read_transmission(message[message_length:])

    length_type_id = message[0]
    if length_type_id == "0":
        length_sub_packages, sub_packages_str, remainder = unpack_length_type_0(message[1:])
        return version + read_transmission(sub_packages_str) + read_transmission(remainder)
    else:
        # n_sub_packages = int(message[1:12], 2)
        return version + read_transmission(message[12:])


def solve(text: str) -> int:
    """Solve the puzzle."""
    # binary_string = "00111000000000000110111101000101001010010001001000000000"
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


# @pytest.mark.parametrize(
#     ("input_s", "expected"),
#     (("110100101111111000101000", 2021), ("11010001010", 10), ("0101001000100100", 20)),
# )
# def test_unpack_length_type_0(input_s: str, expected: int) -> None:

#     pass


@pytest.mark.parametrize(
    ("input_s", "expected"),
    (("110100101111111000101000", 2021), ("11010001010", 10), ("0101001000100100", 20)),
)
def test_decode_literal_value(input_s: str, expected: int) -> None:
    """Check that the solution is correct."""
    decoded_message = decode_literal_value(input_s[6:])
    assert int(decoded_message, 2) == expected


@pytest.mark.parametrize(
    ("input_s", "expected"),
    (
        ("110100101111111000101000", (6, 4, "101111111000101000")),
        (
            "00111000000000000110111101000101001010010001001000000000",
            (1, 6, "00000000000110111101000101001010010001001000000000"),
        ),
    ),
)
def test_packet_splitter(input_s: str, expected: int) -> None:
    """Check that the solution is correct."""
    assert split_packet(input_s) == expected


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
