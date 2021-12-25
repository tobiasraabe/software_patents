"""This module contains code for the indicators used by Bessen and Hunt."""
import re


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


def create_indicators(df_source, column: str, df_out=None):
    if df_out is None:
        df_out = df_source

    for indicator in INDICATORS:
        df_out[column + "_" + indicator.replace("-", "_").upper()] = df_source[
            column
        ].str.contains(r"\b" + indicator + r"\b", flags=re.IGNORECASE)

    return df_out
