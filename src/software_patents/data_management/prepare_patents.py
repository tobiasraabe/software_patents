"""Prepare data from PatentsView.org on general information of patents.

Note that the information is previously processed by ``download_data.py`` and
``split_tsv_files.py`` so that many ``.parquet`` files reside in ``src/data/raw``.

"""
from __future__ import annotations

from pathlib import Path

import dask.dataframe as dd
import numpy as np
import pandas as pd
from dask.distributed import Client
from dask.distributed import LocalCluster
from pytask import Product
from software_patents.config import BLD
from software_patents.config import DASK_LOCAL_CLUSTER_CONFIGURATION
from software_patents.config import SRC
from software_patents.data_management.indicators import create_indicators
from typing_extensions import Annotated


_RAW_PATENTS = {
    f"patent_{i}": SRC / "data" / "raw" / f"patent_{i}.parquet" for i in range(1, 6)
}


def prepare_patents(
    path_to_bh: Path = BLD / "data" / "bh.pkl",
    raw_patents: dict[str, Path] = _RAW_PATENTS,  # noqa: ARG001
    path_to_patents: Annotated[Path, Product] = BLD
    / "data"
    / "processed"
    / "patent.pkl",
) -> None:
    process_data(path_to_bh)
    # Save date information
    df = dd.read_parquet(SRC / "data" / "raw" / "patent_*.parquet")
    df = df[["ID", "DATE"]].compute()
    df.to_pickle(path_to_patents)


def process_data(path_to_bh: Path) -> None:
    # Get 399 patent numbers from BH2007 to store fulltext of abstract and
    # title.
    bh = pd.read_pickle(path_to_bh)

    # Start client for computations
    cluster = LocalCluster(**DASK_LOCAL_CLUSTER_CONFIGURATION)
    client = Client(cluster)  # noqa: F841

    df = dd.read_parquet(SRC / "data" / "raw" / "patent_*.parquet")

    for section in ("ABSTRACT", "TITLE"):
        indicators = create_indicators(df, section)
        out = pd.concat([df["ID"], indicators], axis="columns")

        out = out.assign(
            **{section: df[section].where(cond=out.ID.isin(bh.ID), other=np.nan)}
        )

        out.to_parquet(
            BLD / "data" / f"indicators_{section.lower()}.parquet",
            compute=True,
        )


def merge_indicators(section: str) -> pd.DataFrame:
    df = dd.read_parquet(BLD / "data" / f"indicators_{section}.parquet/*.parquet")
    return df.compute()
