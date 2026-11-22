"""Tests for the Bessen and Hunt classification algorithm."""

import pandas as pd
import pytest

from software_patents.analysis.task_apply_bh_to_indicators import (
    _apply_bh2007_algorithm,
)
from software_patents.data_management.indicators import create_indicators


@pytest.mark.parametrize(
    ("title", "abstract", "description", "expected"),
    [
        ("A device", "Software for testing", "", "Software"),
        ("A device", "Computer", "a program", "Software"),
        ("A device", "Computer", "", "Non-Software"),
        ("A computer chip", "Software", "", "Non-Software"),
        ("A device", "Software and antigen", "", "Non-Software"),
        ("A device", "Software", "antigenic material", "Non-Software"),
        ("A device", "Software", "chromatography", "Non-Software"),
        ("A device", "Software", "a microchip", "Software"),
    ],
)
def test_classification_from_patent_text(
    title: str, abstract: str, description: str, expected: str
) -> None:
    """Classify examples including inclusion, exclusion and word boundaries."""
    texts = pd.DataFrame(
        {"TITLE": [title], "ABSTRACT": [abstract], "DESCRIPTION": [description]}
    )
    indicators = pd.concat(
        [create_indicators(texts, column) for column in texts.columns], axis=1
    )
    assert _apply_bh2007_algorithm(indicators).iloc[0] == expected
