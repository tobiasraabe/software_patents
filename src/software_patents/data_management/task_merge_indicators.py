"""This module contains code for merging indicators to one dataset."""
from __future__ import annotations

import pandas as pd
from pytask import task
from software_patents.config import data_catalog
from software_patents.data_management.indicators import INDICATORS
from typing_extensions import Annotated


@task(
    kwargs={
        "indicator_parts": {
            f"indicators_description_{i}": data_catalog[f"indicators_description_{i}"]
            for i in range(1, 6)
        }
    }
)
def merge_description_indicators(
    indicator_parts: dict[str, pd.DataFrame]
) -> Annotated[pd.DataFrame, data_catalog["indicators_description"]]:
    df = pd.concat(list(indicator_parts.values()))
    df = df.drop_duplicates()
    df = df.drop_duplicates(subset="ID", keep="first")
    return df


@task(produces=data_catalog["indicators"])
def merge_all_indicators(
    description: Annotated[pd.DataFrame, data_catalog["indicators_description"]],
    summary: Annotated[pd.DataFrame, data_catalog["indicators_summary"]],
    abstract: Annotated[pd.DataFrame, data_catalog["indicators_abstract"]],
    title: Annotated[pd.DataFrame, data_catalog["indicators_title"]],
) -> pd.DataFrame:
    df = _merge_summary_into_description(description, summary)
    df = df.merge(abstract, on="ID", how="inner", validate="1:1")
    df = df.merge(title, on="ID", how="inner", validate="1:1")
    return df


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
