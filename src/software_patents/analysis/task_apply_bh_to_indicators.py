"""This file classifies the patents of the original data of Bessen and Hunt (2007)
according to their algorithm.

The algorithm is defined as follows:

````
(("software" in specification) OR ("computer" AND "program" in specification))

AND (utility patent excluding reissues)

ANDNOT ("chip" OR "semiconductor" OR "bus" OR "circuit" OR
        "circuitry" in title)

ANDNOT ("antigen" OR "antigenic" OR "chromatography" in specification)
````

"""
from __future__ import annotations

from pathlib import Path
from typing import Annotated

import pandas as pd
from pytask import Product
from pytask import task
from software_patents.config import BLD


for path_to_indicators, path_to_result in (
    (BLD / "data" / "indicators.pkl", BLD / "analysis" / "bh_with_patent_db.pkl"),
    (
        BLD / "data" / "bh_with_crawled_text.pkl",
        BLD / "analysis" / "bh_with_crawled_text.pkl",
    ),
):

    @task
    def task_apply_bh_to_indicators(
        path_to_indicators: Path = path_to_indicators,
        path_to_result: Annotated[Path, Product] = path_to_result,
    ):
        df = pd.read_pickle(path_to_indicators)
        df["CLASSIFICATION_REPLICATION"] = _apply_bh2007_algorithm(df)
        df = df[
            [
                "ID",
                "CLASSIFICATION_REPLICATION",
                "ABSTRACT",
                "DESCRIPTION",
                "TITLE",
            ]
        ]
        df.to_pickle(path_to_result)


def _apply_bh2007_algorithm(df):
    df["ALGO_FIRST_SPEC_SOFTWARE"] = df.ABSTRACT_SOFTWARE | df.DESCRIPTION_SOFTWARE
    df["ALGO_FIRST_SPEC_COMPUTER"] = df.ABSTRACT_COMPUTER | df.DESCRIPTION_COMPUTER
    df["ALGO_FIRST_SPEC_PROGRAM"] = df.ABSTRACT_PROGRAM | df.DESCRIPTION_PROGRAM
    df["ALGO_FIRST_LINE"] = df.ALGO_FIRST_SPEC_SOFTWARE | (
        df.ALGO_FIRST_SPEC_COMPUTER & df.ALGO_FIRST_SPEC_PROGRAM
    )

    # Second line
    # Reissues are already excluded

    # Third line
    df["ALGO_THIRD_LINE"] = (
        df.TITLE_CHIP
        | df.TITLE_SEMICONDUCTOR
        | df.TITLE_SEMI_CONDUCTOR
        | df.TITLE_BUS
        | df.TITLE_CIRCUIT
        | df.TITLE_CIRCUITRY
    )

    # Fourth line
    df["ALGO_FOURTH_SPEC_ANTIGEN"] = df.ABSTRACT_ANTIGEN | df.DESCRIPTION_ANTIGEN
    df["ALGO_FOURTH_SPEC_ANTIGENIC"] = df.ABSTRACT_ANTIGENIC | df.DESCRIPTION_ANTIGENIC
    df["ALGO_FOURTH_SPEC_CHROMATOGRAPHY"] = (
        df.ABSTRACT_CHROMATOGRAPHY | df.DESCRIPTION_CHROMATOGRAPHY
    )
    df["ALGO_FOURTH_LINE"] = (
        df.ALGO_FOURTH_SPEC_ANTIGENIC
        | df.ALGO_FOURTH_SPEC_ANTIGENIC
        | df.ALGO_FOURTH_SPEC_CHROMATOGRAPHY
    )

    df["REPLICATION_BH2007"] = (
        df.ALGO_FIRST_LINE & ~df.ALGO_THIRD_LINE & ~df.ALGO_FOURTH_LINE
    )

    df.REPLICATION_BH2007.replace(
        {False: "Non-Software", True: "Software"}, inplace=True
    )

    df.REPLICATION_BH2007 = df.REPLICATION_BH2007.astype("category")

    return df.REPLICATION_BH2007
