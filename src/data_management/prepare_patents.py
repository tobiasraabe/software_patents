"""Prepare data from PatentsView.org on general information of patents."""

import pandas as pd
from bld.project_paths import project_paths_join as ppj


PATENTSVIEW_MISSPELLINGS = {
    '\.degree\.': '°',
    '\.gt\.': '>',
    '\.lt\.': '<',
    '\.ltoreq\.': '≦',
    '\.gtoreq\.': '≧',
}


def main():
    df = pd.read_table(
        ppj('IN_DATA_DOWNLOADED', 'patent.tsv.zip'),
        sep='\t',
        error_bad_lines=False,
        usecols=[0, 1, 4, 5, 6, 7, 8],
        low_memory=False,
    )

    # Only utility patents
    df = df.loc[df.type == 'utility'].copy()
    # Ensure that only patents are chosen
    df = df.loc[df.kind.isin(['A', 'B1', 'B2'])]

    # ID is numeric
    df['ID'] = pd.to_numeric(df.id, errors='coerce')
    # CLAIMS_NUMBER is numeric
    df['CLAIMS_NUMBER'] = pd.to_numeric(df.num_claims, errors='coerce')
    # DATE is datetime
    df['DATE'] = pd.to_datetime(df.date)

    # Drop unnecessary columns
    df.drop(columns=['type', 'id', 'date', 'num_claims', 'kind'], inplace=True)

    # Rename columns
    col_names = {'abstract': 'ABSTRACT', 'title': 'TITLE'}
    df = df.rename(columns=col_names)

    # Drop NaNs
    df.dropna(inplace=True)

    # More efficient dtypes
    df.ID = pd.to_numeric(df.ID, downcast='unsigned')
    df.CLAIMS_NUMBER = pd.to_numeric(df.CLAIMS_NUMBER, downcast='unsigned')
    # Edits to text columns
    df.TITLE = df.TITLE.str.strip()
    df.ABSTRACT = df.ABSTRACT.str.strip()

    for column in ['TITLE', 'ABSTRACT']:
        for key, value in PATENTSVIEW_MISSPELLINGS.items():
            df[column] = df[column].str.replace(key, value)

    df.reset_index(drop=True)

    df.to_pickle(ppj('OUT_DATA', 'patents.pkl'))


if __name__ == '__main__':
    main()
