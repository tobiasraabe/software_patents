"""This module contains tasks to replicate the result of Bessen and Hunt."""
from __future__ import annotations

from pathlib import Path
from typing import Annotated

import pandas as pd
from pytask import Product
from pytask import task
from software_patents.config import BLD


for replication, path_to_replication in (
    (
        BLD / "analysis" / "bh_with_crawled_text.pkl",
        BLD / "analysis" / "replication_bh_with_crawled_text.pkl",
    ),
    (
        BLD / "analysis" / "bh_with_patent_db.pkl",
        BLD / "analysis" / "replication_bh_with_patent_db.pkl",
    ),
):

    @task()
    def task_replicate_results_of_bh2007(
        path_to_bh: Path = BLD / "data" / "bh.pkl",
        path_to_bh_with_texts: Path = replication,
        path_to_replication: Annotated[Path, Product] = path_to_replication,
    ) -> None:
        bh = pd.read_pickle(path_to_bh)
        replication = pd.read_pickle(path_to_bh_with_texts)
        bh = bh.merge(replication, on="ID", how="inner", validate="1:1")
        bh.to_pickle(path_to_replication)
