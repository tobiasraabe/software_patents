"""Prepare data from PatentsView.org on the description of patents.

Note that the information is previously processed by
``download_data.py`` and ``split_tsv_files.py`` so that many ``.parquet`` files
reside in ``src/data/raw``.

TODO: Implement intermediate step where the fulltext of all 399 is also saved
for manual inspection.

"""
import sys

import dask.dataframe as dd
import numpy as np
import pandas as pd

from dask.distributed import Client, LocalCluster

from bld.project_paths import project_paths_join as ppj
from src import DASK_LOCAL_CLUSTER_CONFIGURATION
from src.data_management.prepare_bessen_hunt_2007 import create_indicators


def process_data(part: str):
    # Get 399 patent numbers from BH2007 to store fulltext of description.
    bh = pd.read_pickle(ppj('OUT_DATA', 'bh.pkl'))

    # Start client for computations
    cluster = LocalCluster(**DASK_LOCAL_CLUSTER_CONFIGURATION)
    client = Client(cluster)  # noqa: F841

    df = dd.read_parquet(ppj('IN_DATA_RAW', f'detail_desc_text_{part}_*'))

    out = df[['ID']]

    out = create_indicators(df, 'DESCRIPTION', out)

    out = out.assign(
        DESCRIPTION=df['DESCRIPTION'].where(
            cond=out.ID.isin(bh.ID), other=np.nan
        )
    )

    out.to_parquet(
        ppj('OUT_DATA', f'indicators_description_{part}.parquet'), compute=True
    )


def main():
    part = sys.argv[1]

    process_data(part)

    df = dd.read_parquet(
        ppj('OUT_DATA', f'indicators_description_{part}.parquet')
    )
    df = df.compute()

    df.to_pickle(ppj('OUT_DATA', f'indicators_description_{part}.pkl'))


if __name__ == '__main__':
    main()
