"""Prepare data from Bessen and Hunt (2007)."""

import re
import pandas as pd
from bld.project_paths import project_paths_join as ppj
from src.data_management.scrape_patents import multiprocessed
from src.data_management.scrape_patents import scrape_patent_info


def change_dtypes(df):
    for col in ['CLASSIFICATION_ALGORITHM', 'CLASSIFICATION_MANUAL']:
        df[col] = df[col].astype('category')
    df.CLAIMS_NUMBER = pd.to_numeric(
        df.CLAIMS_NUMBER, errors='coerce', downcast='unsigned'
    )

    return df


def create_indicators(df):
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
        for part in ['TITLE', 'ABSTRACT', 'DESCRIPTION']:
            df[part + '_' + indicator.replace('-', '_').upper()] = df[
                part
            ].str.contains(r'\b' + indicator + r'\b', flags=re.IGNORECASE)

    return df


if __name__ == '__main__':
    # Read the dataset of BH2007
    df = pd.read_stata(ppj('IN_DATA_EXTERNAL', 'bessen_hunt_2007.dta'))

    # Setting the correct column names
    dict_columns = dict()
    dict_columns['patent'] = 'ID'
    dict_columns['sw'] = 'CLASSIFICATION_MANUAL'
    dict_columns['mowpat'] = 'CLASSIFICATION_MOWERY'
    dict_columns['swpat2'] = 'CLASSIFICATION_ALGORITHM'

    df.rename(columns=dict_columns, inplace=True)

    # Splitting df.classification_manual because of entries with 2 as 0 and 1
    df['CLASSIFICATION_MANUAL_STRICTER'] = df.CLASSIFICATION_MANUAL == 1
    df['CLASSIFICATION_MANUAL_LOOSER'] = (df.CLASSIFICATION_MANUAL == 1) | (
        df.CLASSIFICATION_MANUAL == 2
    )

    # Drop the former manual classification
    df.drop('CLASSIFICATION_MANUAL', axis=1, inplace=True)

    # Setting the correct dtypes
    df = df[df.columns.difference(['ID'])].astype(bool).join(df.ID)

    # Crawl information from Google and append to existing data
    out = multiprocessed(scrape_patent_info, df.ID.values)
    out = pd.DataFrame(
        out,
        columns=[
            'TITLE',
            'ABSTRACT',
            'DESCRIPTION',
            'CLAIMS',
            'CLAIMS_NUMBER',
        ],
    )
    df = df.join(out)

    # Drop unnecessary columns
    df.drop(
        columns=['CLASSIFICATION_MOWERY', 'CLASSIFICATION_MANUAL_STRICTER'],
        inplace=True,
    )
    # Drop incomplete data
    df.dropna(inplace=True)

    # Rename columns
    df = df.rename(
        columns={'CLASSIFICATION_MANUAL_LOOSER': 'CLASSIFICATION_MANUAL'}
    )

    # Convert booleans to labels
    df.replace({False: 'Non-Software', True: 'Software'}, inplace=True)

    df = change_dtypes(df)

    df.to_pickle(ppj('OUT_DATA', 'bh_text.pkl'))

    df = create_indicators(df)

    df.drop(
        columns=[
            'TITLE',
            'ABSTRACT',
            'DESCRIPTION',
            'CLAIMS',
            'CLAIMS_NUMBER',
        ],
        inplace=True,
    )

    df.to_pickle(ppj('OUT_DATA', 'bh_bool.pkl'))
