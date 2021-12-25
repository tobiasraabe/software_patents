"""This module contains code for merging indicators to one dataset."""
import pandas as pd
import pytask

from src.config import BLD
from src.data_management.indicators import INDICATORS


def merge_description_indicators(depends_on, produces):
    to_concat = []
    for i in range(1, 6):
        df = pd.read_pickle(depends_on[f"indicators_description_{i}"])
        to_concat.append(df)
    df = pd.concat(to_concat)

    df = df.drop_duplicates()

    df = df.drop_duplicates(subset="ID", keep="first")

    df.to_pickle(produces["indicators_description"])


def merge_summary_into_description(description, summary):
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


def merge_all_indicators(depends_on, produces):
    description = pd.read_pickle(produces["indicators_description"])
    summary = pd.read_pickle(depends_on["indicators_summary"])

    df = merge_summary_into_description(description, summary)

    abstract = pd.read_pickle(depends_on["indicators_abstract"])
    title = pd.read_pickle(depends_on["indicators_title"])

    df = df.merge(abstract, on="ID", how="inner", validate="1:1")
    df = df.merge(title, on="ID", how="inner", validate="1:1")

    df.to_pickle(produces["indicators"])


@pytask.mark.depends_on(
    {
        "indicators_abstract": BLD / "data" / "indicators_abstract.pkl",
        "indicators_title": BLD / "data" / "indicators_title.pkl",
        "indicators_summary": BLD / "data" / "indicators_summary.pkl",
        **{
            f"indicators_description_{i}": BLD
            / "data"
            / f"indicators_description_{i}.pkl"
            for i in range(1, 6)
        },
    }
)
@pytask.mark.produces(
    {
        "indicators": BLD / "data" / "indicators.pkl",
        "indicators_description": BLD / "data" / "indicators_description.pkl",
    }
)
def task_merge_indicators(depends_on, produces):
    """Merge all indicators from all parts of text to one dataframe."""
    merge_description_indicators(depends_on, produces)
    merge_all_indicators(depends_on, produces)
