"""Perform some tests to assert that the data stays the same."""

from __future__ import annotations

from typing import Any
from typing import cast

import numpy.testing as npt
import pandas as pd
import pytest
from sklearn.metrics import confusion_matrix

from software_patents.config import SRC
from software_patents.config import data_catalog

_MISSING_DATA_REASON = "Required data catalog entries are not available."


def _has_loadable_data_catalog_entry(name: str) -> bool:
    try:
        node = cast(Any, data_catalog[name])
        return node.path.exists()
    except (FileNotFoundError, ImportError, OSError):
        return False


_HAS_BH = _has_loadable_data_catalog_entry("bh")
_HAS_PATENT = _has_loadable_data_catalog_entry("patent")


@pytest.mark.skipif(not _HAS_BH, reason=_MISSING_DATA_REASON)
def test_bh() -> None:
    df = data_catalog["bh"].load()

    assert df.shape == (399, 6)
    assert df.notnull().all().all()

    # Bessen and Hunt (2007) states about the performance of the algorithm:
    # Compared to our random sample of 400 patents, this algorithm had a
    # false positive rate of 16 percent (that is, 16 percent of the patents
    # the algorithm said were software patents, were not) and a false
    # negative rate of 22 percent (that is, it failed to identify 22
    # percent of the patents we categorized as software patents).
    matrix = confusion_matrix(df.CLASSIFICATION_MANUAL, df.CLASSIFICATION_ALGORITHM)

    false_positive = matrix[0, 1] / (matrix[0, 1] + matrix[1, 1])
    assert false_positive == 0.16  # noqa: PLR2004

    false_negative = matrix[1, 0] / (matrix[1, 0] + matrix[1, 1])
    npt.assert_almost_equal(false_negative, 0.222_222_222_2, decimal=10)


@pytest.mark.skipif(not _HAS_PATENT, reason=_MISSING_DATA_REASON)
def test_patent() -> None:
    df = data_catalog["patent"].load()

    assert df.shape == (6_024_729, 2)
    assert df.notna().all().all()

    # Assert that the total number of patents is similar to the numbers in
    # Bessen & Hunt (2007), Table 1.
    table = pd.read_excel(
        SRC / "data" / "external" / "bh2007_table_1.xlsx",
        header=2,
        usecols=[0, 3],
    )
    subset = df.loc[df.DATE.dt.year.le(2002)].copy()
    npt.assert_array_almost_equal(
        subset.DATE.dt.year.value_counts().sort_index().values,
        table["Total Utility Patents"].values,
        decimal=-3,
    )
