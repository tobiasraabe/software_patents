"""Contains auxiliary functions for plots."""
from __future__ import annotations

from typing import Any


def format_thousands_with_comma(value: float, pos: Any) -> str:  # noqa: ARG001
    return f"{value:,.0f}"
