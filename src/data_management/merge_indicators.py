import dask.dataframe as dd
import pandas as pd

from bld.project_paths import project_paths_join as ppj
from src.data_management.prepare_bessen_hunt_2007 import INDICATORS


def merge_description_indicators():
    df = dd.read_parquet(
        ppj('OUT_DATA', 'indicators_description_*.parquet/*.parquet')
    )
    df = df.compute()

    df = df.drop_duplicates()

    assert df.ID.duplicated().sum() == 8879

    df = df.drop_duplicates(subset='ID', keep='first')

    df.to_pickle(ppj('OUT_DATA', 'indicators_description.pkl'))


def merge_summary_into_description(description, summary):
    """Merge indicators of summary into description with logical ORs."""
    df = description.merge(summary, on='ID', how='outer')

    for ind in INDICATORS:
        ind_name = ind.upper().replace('-', '_')

        df[f'DESCRIPTION_{ind_name}'] = (
            df[f'DESCRIPTION_{ind_name}'] | df[f'SUMMARY_{ind_name}']
        )

    summary_cols = df.filter(like='SUMMARY').columns.tolist()
    df = df.drop(columns=summary_cols)

    return df


def merge_all_indicators():
    description = pd.read_pickle(ppj('OUT_DATA', 'indicators_description.pkl'))
    summary = pd.read_pickle(ppj('OUT_DATA', 'indicators_summary.pkl'))

    df = merge_summary_into_description(description, summary)

    abstract = pd.read_pickle(ppj('OUT_DATA', 'indicators_abstract.pkl'))
    title = pd.read_pickle(ppj('OUT_DATA', 'indicators_title.pkl'))

    df = df.merge(abstract, on='ID', how='inner', validate='1:1')
    df = df.merge(title, on='ID', how='inner', validate='1:1')

    df.to_pickle(ppj('OUT_DATA', 'indicators.pkl'))


def main():
    merge_description_indicators()
    merge_all_indicators()


if __name__ == '__main__':
    main()
