"""Prepare data from Bessen and Hunt (2007)."""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Annotated

import pandas as pd
from pytask import Product
from software_patents.config import BLD
from software_patents.config import SRC
from software_patents.config import THREADS_SCRAPE_PATENTS
from software_patents.data_management.indicators import create_indicators
from software_patents.data_management.scrape_patents import scrape_patent_info


def task_prepare_bessen_hunt_2007(
    path_to_external: Path = SRC / "data" / "external" / "bessen_hunt_2007.dta",
    path_to_bh: Annotated[Path, Product] = BLD / "data" / "bh.pkl",
    path_to_bh_with_crawled_text: Annotated[Path, Product] = BLD
    / "data"
    / "bh_with_crawled_text.pkl",
) -> None:
    # Read the dataset of BH2007
    df = pd.read_stata(path_to_external)

    # Setting the correct column names
    dict_columns = {
        "patent": "ID",
        "sw": "CLASSIFICATION_BASE",
        "mowpat": "CLASSIFICATION_MOWERY",
        "swpat2": "CLASSIFICATION_ALGORITHM",
    }

    df.rename(columns=dict_columns, inplace=True)

    # Split the original manual classification. The first is the one used in
    # the paper.
    df["CLASSIFICATION_MANUAL"] = df.CLASSIFICATION_BASE.isin([1, 2])
    df["CLASSIFICATION_MANUAL_ALT"] = df.CLASSIFICATION_BASE.eq(1)

    # Setting the correct dtypes
    df = df[df.columns.difference(["ID"])].astype(bool).join(df.ID)

    # Convert booleans to labels
    df.replace({False: "Non-Software", True: "Software"}, inplace=True)

    object_cols = df.select_dtypes(object).columns.tolist()
    df[object_cols] = df[object_cols].astype("category")

    # Exclude patent which is not available anymore
    df = df.loc[~df.ID.eq(5_785_646)]

    df.to_pickle(path_to_bh)

    # Crawl information from Google and append to existing data
    with ThreadPoolExecutor(max_workers=THREADS_SCRAPE_PATENTS) as executor:
        results = executor.map(scrape_patent_info, df.ID.to_list())

    out = pd.DataFrame(
        results,
        columns=[
            "ID",
            "TITLE",
            "ABSTRACT",
            "DESCRIPTION",
            "CLAIMS",
            "CLAIMS_NUMBER",
        ],
    )
    df = df.merge(out, on="ID", how="inner", validate="1:1")

    for column in ("ABSTRACT", "DESCRIPTION", "TITLE"):
        indicators = create_indicators(df, column)
        df = pd.concat([df, indicators], axis="columns")

    df.to_pickle(path_to_bh_with_crawled_text)
