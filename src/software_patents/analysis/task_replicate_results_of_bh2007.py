"""This module contains tasks to replicate the result of Bessen and Hunt."""
from __future__ import annotations

import pandas as pd
from pytask import task
from software_patents.config import data_catalog


for bh_with_texts, replication in (
    (
        data_catalog["bh_with_crawled_text_analysis"],
        data_catalog["replication_bh_with_crawled_text"],
    ),
    (data_catalog["bh_with_patent_db"], data_catalog["replication_bh_with_patent_db"]),
):

    @task(
        kwargs={"bh": data_catalog["bh"], "bh_with_texts": bh_with_texts},
        produces=replication,
    )
    def task_replicate_results_of_bh2007(
        bh: pd.DataFrame, bh_with_texts: pd.DataFrame
    ) -> pd.DataFrame:
        bh = bh.merge(bh_with_texts, on="ID", how="inner", validate="1:1")
        return bh
