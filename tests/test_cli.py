"""Smoke tests for the amail-md console entry point."""

from amail_md import main


def test_main_returns_none() -> None:
    """main() runs without error."""
    assert main() is None
