"""Prepare data from PatentsView.org on the description of patents.

Note that the information is previously processed by
``download_data.py`` and ``split_tsv_files.py`` so that many ``.parquet`` files
reside in ``src/data/raw``.

TODO: Implement intermediate step where the fulltext of all 399 is also saved
for manual inspection.

"""
from __future__ import annotations

from pathlib import Path

import dask.dataframe as dd
import numpy as np
import pandas as pd
from dask.distributed import Client
from dask.distributed import LocalCluster
from software_patents.config import BLD
from software_patents.config import DASK_LOCAL_CLUSTER_CONFIGURATION
from software_patents.config import SRC
from software_patents.data_management.indicators import create_indicators


def prepare_description(
    raw_descriptions: dict[str, Path],  # noqa: ARG001
    part: str,
    path_to_bh: Path = BLD / "data" / "bh.pkl",
) -> pd.DataFrame:
    # Get 399 patent numbers from BH2007 to store fulltext of description.
    bh = pd.read_pickle(path_to_bh)

    # Start client for computations
    cluster = LocalCluster(**DASK_LOCAL_CLUSTER_CONFIGURATION)
    client = Client(cluster)  # noqa: F841

    df = dd.read_parquet(SRC / "data" / "raw" / f"detail_desc_text_{part}_*_*.parquet")

    indicators = create_indicators(df, "DESCRIPTION")
    out = pd.concat([df["ID"], indicators], axis="columns")

    out = out.assign(
        DESCRIPTION=df["DESCRIPTION"].where(cond=out.ID.isin(bh.ID), other=np.nan)
    )

    out.compute()
    return out
