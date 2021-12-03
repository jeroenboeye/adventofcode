"""Test utils."""

from aoc.parsers import text_to_integer_array


def test_text_to_integer_array(integers_as_text: str) -> None:
    """Test the text_to_integer_array function."""
    array = text_to_integer_array(integers_as_text)
    assert len(array) == 10
    assert array[0].dtype == int
    assert sum(array) == 2256
