"""This module contains code for merging indicators to one dataset."""
from __future__ import annotations

from pathlib import Path
from typing import Annotated

import pandas as pd
from pytask import Product
from pytask import task
from software_patents.config import BLD
from software_patents.data_management.indicators import INDICATORS

_INDICATOR_PARTS = {
    f"indicators_description_{i}": BLD / "data" / f"indicators_description_{i}.pkl"
    for i in range(1, 6)
}


@task()
def merge_description_indicators(
    path_to_indicator_parts: dict[str, Path] = _INDICATOR_PARTS,
    path_to_indicators: Annotated[Path, Product] = BLD
    / "data"
    / "indicators_description.pkl",
) -> None:
    to_concat = []
    for i in range(1, 6):
        df = pd.read_pickle(path_to_indicator_parts[f"indicators_description_{i}"])
        to_concat.append(df)

    df = pd.concat(to_concat)

    df = df.drop_duplicates()

    df = df.drop_duplicates(subset="ID", keep="first")

    df.to_pickle(path_to_indicators)


@task()
def merge_all_indicators(
    path_to_indicators_description: Path = BLD / "data" / "indicators_description.pkl",
    path_to_indicators_summary: Path = BLD / "data" / "indicators_summary.pkl",
    path_to_indicators_abstract: Path = BLD / "data" / "indicators_abstract.pkl",
    path_to_indicators_title: Path = BLD / "data" / "indicators_title.pkl",
    path_to_indicators: Annotated[Path, Product] = BLD / "data" / "indicators.pkl",
) -> None:
    description = pd.read_pickle(path_to_indicators_description)
    summary = pd.read_pickle(path_to_indicators_summary)

    df = _merge_summary_into_description(description, summary)

    abstract = pd.read_pickle(path_to_indicators_abstract)
    title = pd.read_pickle(path_to_indicators_title)

    df = df.merge(abstract, on="ID", how="inner", validate="1:1")
    df = df.merge(title, on="ID", how="inner", validate="1:1")

    df.to_pickle(path_to_indicators)


def _merge_summary_into_description(
    description: pd.DataFrame, summary: pd.DataFrame
) -> pd.DataFrame:
    """Merge indicators of summary into description with logical ORs."""
    df = description.merge(summary, on="ID", how="outer")

    for ind in INDICATORS:
        ind_name = ind.upper().replace("-", "_")

        df[f"DESCRIPTION_{ind_name}"] = (
            df[f"DESCRIPTION_{ind_name}"] | df[f"SUMMARY_{ind_name}"]
        )

    summary_cols = df.filter(like="SUMMARY").columns.tolist()
    df = df.drop(columns=summary_cols)

    return df
