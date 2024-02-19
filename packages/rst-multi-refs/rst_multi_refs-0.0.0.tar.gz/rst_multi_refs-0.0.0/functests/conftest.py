"""Configuration for pytest."""
from pathlib import Path

import pytest

pytest_plugins = "sphinx.testing.fixtures"
collect_ignore = ["roots"]


@pytest.fixture(scope="session")
def rootdir():
    """Set root directory to use testing sphinx project."""
    return Path(__file__).parent.resolve() / "roots"
