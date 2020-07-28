"""Prepare data from PatentsView.org on general information of patents.

Note that the information is previously processed by ``download_data.py`` and
``split_tsv_files.py`` so that many ``.parquet`` files reside in
``src/data/raw``.

"""

import dask.dataframe as dd
import numpy as np
import pandas as pd

from dask.distributed import Client, LocalCluster

from bld.project_paths import project_paths_join as ppj
from src import DASK_LOCAL_CLUSTER_CONFIGURATION
from src.data_management.prepare_bessen_hunt_2007 import create_indicators


def process_data():
    # Get 399 patent numbers from BH2007 to store fulltext of abstract and
    # title.
    bh = pd.read_pickle(ppj('OUT_DATA', 'bh.pkl'))

    # Start client for computations
    cluster = LocalCluster(**DASK_LOCAL_CLUSTER_CONFIGURATION)
    client = Client(cluster)  # noqa: F841

    df = dd.read_parquet(ppj('IN_DATA_RAW', 'patent_*.parquet'))

    for section in ['ABSTRACT', 'TITLE']:

        out = df[['ID']]

        out = create_indicators(df, section, out)

        out = out.assign(
            **{
                section: df[section].where(
                    cond=out.ID.isin(bh.ID), other=np.nan
                )
            }
        )

        out.to_parquet(
            ppj('OUT_DATA', f'indicators_{section.lower()}.parquet'),
            compute=True,
        )


def merge_indicators():
    for section in ['abstract', 'title']:
        df = dd.read_parquet(
            ppj('OUT_DATA', f'indicators_{section}.parquet/*.parquet')
        )
        df = df.compute()
        df.to_pickle(ppj('OUT_DATA', f'indicators_{section}.pkl'))


def main():
    process_data()
    merge_indicators()

    # Save date information
    df = dd.read_parquet(ppj('IN_DATA_RAW', 'patent_*.parquet'))
    df = df[['ID', 'DATE']].compute()
    df.to_pickle(ppj('OUT_DATA', 'patent.pkl'))


if __name__ == '__main__':
    main()
