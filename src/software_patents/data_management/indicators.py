"""Contains code for the indicators used by Bessen and Hunt."""
from __future__ import annotations

import re

import pandas as pd


INDICATORS = [
    "software",
    "computer",
    "program",
    "chip",
    "semiconductor",
    "semi-conductor",
    "bus",
    "circuit",
    "circuitry",
    "antigen",
    "antigenic",
    "chromatography",
]


def create_indicators(df: pd.DataFrame, column: str) -> pd.DataFrame:
    return pd.concat(
        [
            pd.Series(
                data=df[column].str.contains(
                    r"\b" + indicator + r"\b", flags=re.IGNORECASE
                ),
                name=column + "_" + indicator.replace("-", "_").upper(),
            )
            for indicator in INDICATORS
        ],
        axis="columns",
    )
