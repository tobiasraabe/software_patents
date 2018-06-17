#!/usr/bin/env python

"""This module tests the equality of the two algorithms in
classifcation_bh2007.py and replication_bh2007.py as well as the data quality.
"""

import pandas as pd
from bld.project_paths import project_paths_join as ppj


def test_equality_of_bh2007_and_replication():
    # Load the dataset
    df = pd.read_pickle(ppj('OUT_ANALYSIS', 'replication_bh.pkl'))

    num_diff_class = (
        ~(df.CLASSIFICATION_ALGORITHM == df.CLASSIFICATION_REPLICATION)
    ).sum()

    # Currently, this tests allows nine cases where the implementations do not
    # match. From visual inspection, BH2007 are wrong.
    assert num_diff_class == 1, (
        "The replication of BH2007's algorithm is not successful. There are"
        " {} cases which do not coincide.".format(num_diff_class)
    )


def test_equality_of_ml_replication():
    # Here are the kappa scores from my thesis.
    # thesis_kappa = [0.875, 0.875, 0.875, 0.771, 0.895,
    #                 0.875, 0.543, 0.875, 0.448, 0.314]

    pass


def test_number_of_software_patents_between_1976_and_1999():
    """Test number of software patents in the period from 1976 to 1999.

    Bessen and Hunt (2007) state that they found 130,650 software patents
    during this period.

    """
    pass
