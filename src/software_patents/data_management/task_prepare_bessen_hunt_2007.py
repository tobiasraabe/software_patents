"""Prepare data from Bessen and Hunt (2007)."""

from __future__ import annotations

import asyncio
from itertools import starmap
from pathlib import Path

import pandas as pd
from typing_extensions import Annotated

from software_patents.config import SRC
from software_patents.config import data_catalog
from software_patents.data_management.indicators import create_indicators
from software_patents.data_management.scrape_patents import fetch_patent
from software_patents.data_management.scrape_patents import parse_patent_page


def task_prepare_bessen_hunt_2007(
    path_to_external: Path = SRC / "data" / "external" / "bessen_hunt_2007.dta",
) -> Annotated[
    pd.DataFrame, (data_catalog["bh"], data_catalog["bh_with_crawled_text"])
]:
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

    bh = df.copy()

    # Crawl information from Google and append to existing data
    loop = asyncio.get_event_loop()
    tasks = [loop.create_task(fetch_patent(id_)) for id_ in df.ID.to_list()]
    pages = loop.run_until_complete(asyncio.gather(*tasks))
    infos = list(starmap(parse_patent_page, zip(df.ID.to_list(), pages)))

    out = pd.DataFrame(
        infos,
        columns=["ID", "TITLE", "ABSTRACT", "DESCRIPTION", "CLAIMS", "CLAIMS_NUMBER"],
    )
    df = df.merge(out, on="ID", how="inner", validate="1:1")

    for column in ("ABSTRACT", "DESCRIPTION", "TITLE"):
        indicators = create_indicators(df, column)
        df = pd.concat([df, indicators], axis="columns")

    return bh, df
