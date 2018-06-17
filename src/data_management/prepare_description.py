"""Prepare data from PatentsView.org on the description of patents.

Note that the information is previously processed by
``download_data.py`` and ``split_tsv_files.py`` so that many ``.parquet`` files
reside in ``src/data/raw``.

"""

import dask
import dask.dataframe as dd
import re

from bld.project_paths import project_paths_join as ppj
from dask import compute
from multiprocessing.pool import ThreadPool
from src import DASK_THREAD_NUMBER


dask.set_options(pool=ThreadPool(DASK_THREAD_NUMBER))


def main():
    df = dd.read_parquet(ppj('IN_DATA_RAW', 'detail_desc_text_*'))

    out = df[['ID']]

    for indicator in [
        'software',
        'computer',
        'program',
        'chip',
        'semiconductor',
        'semi-conductor',
        'bus',
        'circuit',
        'circuitry',
        'antigen',
        'antigenic',
        'chromatography',
    ]:
        out['DESCRIPTION_' + indicator.replace('-', '_').upper()] = df[
            'DESCRIPTION'
        ].str.contains(r'\b' + indicator + r'\b', flags=re.IGNORECASE)

    out = compute(out)

    out.to_parquet(ppj('OUT_DATA', 'indicators_description.parquet'))


if __name__ == '__main__':
    main()
