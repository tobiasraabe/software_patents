"""Contains code for merging indicators to one dataset."""

from __future__ import annotations

import pandas as pd
from pytask import task
from typing_extensions import Annotated

from software_patents.config import data_catalog
from software_patents.data_management.indicators import INDICATORS


@task(
    kwargs={
        "indicator_parts": {
            f"indicators_description_{i}": data_catalog[f"indicators_description_{i}"]
            for i in range(1, 6)
        }
    }
)
def merge_description_indicators(
    indicator_parts: dict[str, pd.DataFrame],
) -> Annotated[pd.DataFrame, data_catalog["indicators_description"]]:
    return (
        pd.concat(list(indicator_parts.values()))
        .drop_duplicates()
        .drop_duplicates(subset="ID", keep="first")
    )


@task(produces=data_catalog["indicators"])
def merge_all_indicators(
    description: Annotated[pd.DataFrame, data_catalog["indicators_description"]],
    summary: Annotated[pd.DataFrame, data_catalog["indicators_summary"]],
    abstract: Annotated[pd.DataFrame, data_catalog["indicators_abstract"]],
    title: Annotated[pd.DataFrame, data_catalog["indicators_title"]],
) -> pd.DataFrame:
    _merge_summary_into_description(description, summary).merge(
        abstract, on="ID", how="inner", validate="1:1"
    ).merge(title, on="ID", how="inner", validate="1:1")


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
    return df.drop(columns=summary_cols)
