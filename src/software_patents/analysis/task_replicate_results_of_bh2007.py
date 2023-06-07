"""This module contains tasks to replicate the result of Bessen and Hunt."""
from __future__ import annotations

import pandas as pd
import pytask
from software_patents.config import BLD


for depends_on, produces in (
    (
        BLD / "analysis" / "bh_with_crawled_text.pkl",
        BLD / "analysis" / "replication_bh_with_crawled_text.pkl",
    ),
    (
        BLD / "analysis" / "bh_with_patent_db.pkl",
        BLD / "analysis" / "replication_bh_with_patent_db.pkl",
    ),
):

    @pytask.mark.task
    @pytask.mark.depends_on({"bh": BLD / "data" / "bh.pkl", "replication": depends_on})
    def task_replicate_results_of_bh2007(depends_on, produces=produces):
        bh = pd.read_pickle(depends_on["bh"])
        replication = pd.read_pickle(depends_on["replication"])

        bh = bh.merge(replication, on="ID", how="inner", validate="1:1")

        bh.to_pickle(produces)
