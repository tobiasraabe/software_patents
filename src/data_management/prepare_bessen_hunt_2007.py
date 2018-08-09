"""Prepare data from Bessen and Hunt (2007)."""

import re

import pandas as pd

from bld.project_paths import project_paths_join as ppj
from src.data_management.scrape_patents import (
    multiprocessed,
    scrape_patent_info,
)


INDICATORS = [
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
]


def create_indicators(df_source, column: str, df_out=None):
    if df_out is None:
        df_out = df_source

    for indicator in INDICATORS:
        df_out[column + '_' + indicator.replace('-', '_').upper()] = df_source[
            column
        ].str.contains(r'\b' + indicator + r'\b', flags=re.IGNORECASE)

    return df_out


def main():
    # Read the dataset of BH2007
    df = pd.read_stata(ppj('IN_DATA_EXTERNAL', 'bessen_hunt_2007.dta'))

    # Setting the correct column names
    dict_columns = {
        'patent': 'ID',
        'sw': 'CLASSIFICATION_BASE',
        'mowpat': 'CLASSIFICATION_MOWERY',
        'swpat2': 'CLASSIFICATION_ALGORITHM',
    }

    df.rename(columns=dict_columns, inplace=True)

    # Split the original manual classification. The first is the one used in
    # the paper.
    df['CLASSIFICATION_MANUAL'] = df.CLASSIFICATION_BASE.isin([1, 2])
    df['CLASSIFICATION_MANUAL_ALT'] = df.CLASSIFICATION_BASE.eq(1)

    # Setting the correct dtypes
    df = df[df.columns.difference(['ID'])].astype(bool).join(df.ID)

    # Convert booleans to labels
    df.replace({False: 'Non-Software', True: 'Software'}, inplace=True)

    object_cols = df.select_dtypes(object).columns.tolist()
    df[object_cols] = df[object_cols].astype('category')

    # Exclude patent which is not available anymore
    df = df.loc[~df.ID.eq(5785646)]

    df.to_pickle(ppj('OUT_DATA', 'bh.pkl'))

    # Crawl information from Google and append to existing data
    out = multiprocessed(scrape_patent_info, df.ID.values)
    out = pd.DataFrame(
        out,
        columns=[
            'ID',
            'TITLE',
            'ABSTRACT',
            'DESCRIPTION',
            'CLAIMS',
            'CLAIMS_NUMBER',
        ],
    )
    df = df.merge(out, on='ID', how='inner', validate='1:1')

    for column in ['ABSTRACT', 'DESCRIPTION', 'TITLE']:
        df = create_indicators(df, column)

    df.to_pickle(ppj('OUT_DATA', 'bh_with_crawled_text.pkl'))


if __name__ == '__main__':
    main()
