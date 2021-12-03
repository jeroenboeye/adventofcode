"""Conftest file with global fixture and pytest imports."""
import pytest


@pytest.fixture(scope="session")
def integers_as_text() -> str:
    """Text fixture for integers."""
    text = """\
199
200
208
210
200
207
240
269
260
263
"""
    return text
