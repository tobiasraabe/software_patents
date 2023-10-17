"""This module contains code to produce confusion matrices."""
from __future__ import annotations

from pathlib import Path
from typing import Annotated

import pandas as pd
from pytask import Product
from sklearn.metrics import confusion_matrix
from software_patents.config import BLD


TABLE = """\\begin{tabular}{@{}cp{0.5cm}cp{0.5cm}c@{}}
\t\\toprule
\t& &  Relevant & & Not Relevant \\\\ \\cline{1-1} \\cline{2-2} \\cline{3-3}
\tRetrieved & & TP & & FP \\\\
\tNot Retrieved & & FN & & TN \\\\
\t\\bottomrule
\\end{tabular}
"""

TABLE_WITH_INFO = """\\begin{tabular}{@{}cp{0.5cm}cp{0.5cm}c@{}}
\t\\toprule
\t& & Relevant & & Not Relevant \\\\ \\cline{1-1} \\cline{3-3} \\cline{5-5}
\tRetrieved & & TP (true-positive) & & FP (false-positive) \\\\
\tNot Retrieved & & FN (false-negative) & & TN (true-negative) \\\\
\t\\bottomrule
\\end{tabular}
"""


def create_confusion_matrix(
    actual_class: pd.Series, predicted_class: pd.Series, path: Path
) -> None:
    (tp, fn), (fp, tn) = confusion_matrix(
        actual_class, predicted_class, labels=["Software", "Non-Software"]
    )

    table = (
        TABLE_WITH_INFO.replace("TP", str(tp))
        .replace("FN", str(fn))
        .replace("FP", str(fp))
        .replace("TN", str(tn))
    )

    path.write_text(table)


def create_confusion_matrix_with_info(
    actual_class: pd.Series, predicted_class: pd.Series, path: Path
) -> None:
    (tp, fn), (fp, tn) = confusion_matrix(
        actual_class, predicted_class, labels=["Software", "Non-Software"]
    )

    table = (
        TABLE.replace("TP", str(tp))
        .replace("FN", str(fn))
        .replace("FP", str(fp))
        .replace("TN", str(tn))
    )

    path.write_text(table)


def task_table_bessen_hunt_2007_and_replicate(
    bh_with_crawled_text: Path = BLD
    / "analysis"
    / "replication_bh_with_crawled_text.pkl",
    bh_with_patent_db: Path = BLD / "analysis" / "replication_bh_with_patent_db.pkl",
    cf_crawled_text: Annotated[Path, Product] = BLD
    / "tables"
    / "tab-cf-replication-bh-with-crawled-text.tex",
    cf_crawled_text_info: Annotated[Path, Product] = BLD
    / "tables"
    / "tab-cf-replication-bh-with-crawled-text-info.tex",
    cf_patent_db: Annotated[Path, Product] = BLD
    / "tables"
    / "tab-cf-replication-bh-with-patent-db.tex",
) -> None:
    df = pd.read_pickle(bh_with_crawled_text)

    create_confusion_matrix(
        df.CLASSIFICATION_MANUAL,
        df.CLASSIFICATION_ALGORITHM,
        cf_crawled_text,
    )
    create_confusion_matrix_with_info(
        df.CLASSIFICATION_MANUAL,
        df.CLASSIFICATION_REPLICATION,
        cf_crawled_text_info,
    )

    temp = pd.read_pickle(bh_with_patent_db)

    df = df[["ID", "CLASSIFICATION_MANUAL"]].merge(
        temp[["ID", "CLASSIFICATION_REPLICATION"]], on="ID", how="left"
    )

    create_confusion_matrix(
        df.CLASSIFICATION_MANUAL,
        df.CLASSIFICATION_REPLICATION,
        cf_patent_db,
    )
