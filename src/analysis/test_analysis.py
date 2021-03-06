#!/usr/bin/env python

"""This module tests the equality of the two algorithms in
classifcation_bh2007.py and replication_bh2007.py as well as the data quality.
"""

import numpy.testing as npt
import pandas as pd
import pytest

from bld.project_paths import project_paths_join as ppj


def test_equality_of_bh2007_and_replication_with_crawled_texts():
    # Load the dataset
    df = pd.read_pickle(
        ppj('OUT_ANALYSIS', 'replication_bh_with_crawled_text.pkl')
    )

    different_classifications = df.loc[
        ~df.CLASSIFICATION_ALGORITHM.eq(df.CLASSIFICATION_REPLICATION)
    ]

    # The replication with crawled texts differs from the one in the paper
    # Bessen, Hunt (2007) only in one case where the authors overlooked the
    # word `chromatography` in the description of the patent 5489660.
    assert different_classifications.shape[0] == 1
    assert different_classifications.ID.eq(5489660).all()


def test_equality_of_bh2007_and_replication_with_patent_db():
    # Load the dataset
    df = pd.read_pickle(
        ppj('OUT_ANALYSIS', 'replication_bh_with_patent_db.pkl')
    )

    different_classifications = df.loc[
        ~df.CLASSIFICATION_ALGORITHM.eq(df.CLASSIFICATION_REPLICATION)
    ]

    #
    assert different_classifications.shape[0] == 1


def test_equality_of_replication_with_crawled_texts_and_patent_db():
    bh = pd.read_pickle(
        ppj('OUT_ANALYSIS', 'replication_bh_with_crawled_text.pkl')
    )
    db = pd.read_pickle(
        ppj('OUT_ANALYSIS', 'replication_bh_with_patent_db.pkl')
    )

    columns = ['ID', 'CLASSIFICATION_REPLICATION']
    bh = bh[columns]
    db = db[columns]

    df = db.merge(
        bh, on='ID', how='inner', suffixes=('_DB', '_CT'), validate='1:1'
    )
    df = df.loc[
        ~df.CLASSIFICATION_REPLICATION_CT.eq(df.CLASSIFICATION_REPLICATION_DB)
    ]

    assert df.shape[0] == 0


def test_equality_of_ml_replication():
    # Here are the kappa scores from my thesis.
    # thesis_kappa = [0.875, 0.875, 0.875, 0.771, 0.895,
    #                 0.875, 0.543, 0.875, 0.448, 0.314]

    pass


@pytest.fixture(scope='module')
def table(request):
    """Fixture for Table 1 of Bessen and Hunt (2007)."""
    table = pd.read_excel(
        ppj('IN_DATA_EXTERNAL', 'bh2007_table_1.xlsx'),
        header=2,
        usecols=[0, 1, 4],
    )

    return table


@pytest.fixture(scope='module')
def sp(request):
    """Fixture for all classified patents."""
    bh = pd.read_pickle(ppj('OUT_ANALYSIS', 'bh_with_patent_db.pkl'))
    date = pd.read_pickle(ppj('OUT_DATA', 'patent.pkl'))
    df = bh.merge(date, on='ID', how='inner', validate='1:1')

    return df


@pytest.mark.xfail(
    reason='The number of software patents is underestimated with PatentsView'
)
def test_absolute_number_of_software_patents_between_1976_and_1999(sp):
    """Test number of software patents in the period from 1976 to 1999.

    Bessen and Hunt (2007) state on p. 163 that they found 130,650 software
    patents during this period.

    """
    sp = sp.loc[
        sp.DATE.dt.year.le(1999) & sp.CLASSIFICATION_REPLICATION.eq('Software')
    ]

    num_software_patents = sp.shape[0]

    for decimal in [-6, -5]:
        assert npt.assert_almost_equal(
            num_software_patents, 130650, decimal=decimal
        )


@pytest.mark.xfail(
    reason='The number of software patents is underestimated with PatentsView'
)
def test_absolute_number_of_software_patents_between_1976_and_2002(table, sp):
    """Test number of software patents between 1976 and 2002.

    The data comes from Table 1 of Bessen and Hunt (2007).

    """
    sp = sp.loc[sp.DATE.dt.year.le(2002)]

    num_software_patents = (
        sp.groupby([sp.DATE.dt.year, sp.CLASSIFICATION_REPLICATION])
        .ID.count()
        .unstack()['Software']
        .values
    )

    for decimal in [-5, -4]:
        assert npt.assert_array_almost_equal(
            num_software_patents, table['Software Patents'], decimal=decimal
        )


@pytest.mark.xfail(
    reason='The number of software patents is underestimated with PatentsView'
)
def test_share_of_software_patents_to_total_between_1976_and_2002(table, sp):
    """Test share of software patents between 1976 and 2002.

    The data comes from Table 1 of Bessen and Hunt (2007).

    """
    sp = sp.loc[sp.DATE.dt.year.le(2002)]

    share_software_patents = (
        sp.groupby([sp.DATE.dt.year, sp.CLASSIFICATION_REPLICATION])
        .ID.count()
        .unstack()
        .apply(lambda x: x / x.sum(), axis=1)['Software']
        .values
    )

    for decimal in [1, 2]:
        assert npt.assert_array_almost_equal(
            share_software_patents, table['Software/Total'], decimal=decimal
        )
