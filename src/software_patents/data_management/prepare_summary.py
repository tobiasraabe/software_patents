"""Prepare data from PatentsView.org on the description of patents.

Note that the information is previously processed by
``download_data.py`` and ``split_tsv_files.py`` so that many ``.parquet`` files
reside in ``src/data/raw``.

TODO: Implement intermediate step where the fulltext of all 399 is also saved
for manual inspection.

"""
import dask.dataframe as dd
import numpy as np
import pandas as pd
from dask.distributed import Client
from dask.distributed import LocalCluster
from software_patents.config import BLD
from software_patents.config import DASK_LOCAL_CLUSTER_CONFIGURATION
from software_patents.config import SRC
from software_patents.data_management.indicators import create_indicators


def _process_data():
    # Get 399 patent numbers from BH2007 to store fulltext of description.
    bh = pd.read_pickle(BLD / "data" / "bh.pkl")

    # Start client for computations
    cluster = LocalCluster(**DASK_LOCAL_CLUSTER_CONFIGURATION)
    client = Client(cluster)  # noqa: F841

    df = dd.read_parquet(SRC / "data" / "raw" / "brf_sum_text_*")

    out = df[["ID"]]

    out = create_indicators(df, "SUMMARY", out)

    out = out.assign(SUMMARY=df["SUMMARY"].where(cond=out.ID.isin(bh.ID), other=np.nan))

    out.to_parquet(BLD / "data" / "indicators_summary.parquet", compute=True)


def prepare_summary(depends_on, produces):
    _process_data(depends_on)

    df = dd.read_parquet(SRC / "data" / "indicators_summary.parquet")
    df = df.compute()

    df.to_pickle(produces)
