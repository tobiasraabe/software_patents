"""Pytest configuration for tests requiring external replication data."""

from __future__ import annotations

import pytest


def pytest_addoption(parser: pytest.Parser) -> None:
    """Allow running the data-dependent replication tests explicitly."""
    parser.addoption("--run-data-tests", action="store_true", default=False)


def pytest_collection_modifyitems(
    config: pytest.Config, items: list[pytest.Item]
) -> None:
    """Skip data-dependent tests unless explicitly requested."""
    if not config.getoption("--run-data-tests"):
        skip = pytest.mark.skip(
            reason="requires replication data; use --run-data-tests"
        )
        for item in items:
            if "data" in item.keywords:
                item.add_marker(skip)
