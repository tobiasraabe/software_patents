"""This module performs some tests to assert that the data stays the same."""

import numpy.testing as npt
import pandas as pd

from sklearn.metrics import confusion_matrix

from bld.project_paths import project_paths_join as ppj


def test_bh():
    df = pd.read_pickle(ppj('OUT_DATA', 'bh.pkl'))

    assert df.shape == (399, 6)
    assert df.notnull().all().all()

    # Bessen and Hunt (2007) states about the performance of the algorithm:
    # Compared to our random sample of 400 patents, this algorithm had a
    # false positive rate of 16 percent (that is, 16 percent of the patents
    # the algorithm said were software patents, were not) and a false
    # negative rate of 22 percent (that is, it failed to identify 22
    # percent of the patents we categorized as software patents).
    matrix = confusion_matrix(
        df.CLASSIFICATION_MANUAL, df.CLASSIFICATION_ALGORITHM
    )

    false_positive = matrix[0, 1] / (matrix[0, 1] + matrix[1, 1])
    assert false_positive == 0.16

    false_negative = matrix[1, 0] / (matrix[1, 0] + matrix[1, 1])
    npt.assert_almost_equal(false_negative, 0.2222222222, decimal=10)


def test_patent():
    df = pd.read_pickle(ppj('OUT_DATA', 'patent.pkl'))

    assert df.shape == (6024729, 2)
    assert df.notna().all().all()

    # Assert that the total number of patents is similar to the numbers in
    # Bessen & Hunt (2007), Table 1.
    table = pd.read_excel(
        ppj('IN_DATA_EXTERNAL', 'bh2007_table_1.xlsx'),
        header=2,
        usecols=[0, 3],
    )
    subset = df.loc[df.DATE.dt.year.le(2002)].copy()
    npt.assert_array_almost_equal(
        subset.DATE.dt.year.value_counts().sort_index().values,
        table['Total Utility Patents'].values,
        decimal=-3,
    )


def test_data_against_crawled_patents():
    pass
