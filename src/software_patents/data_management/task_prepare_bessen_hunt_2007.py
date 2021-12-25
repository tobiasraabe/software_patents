"""Prepare data from Bessen and Hunt (2007)."""
import pandas as pd
import pytask
from software_patents.config import BLD
from software_patents.config import SRC
from software_patents.data_management.indicators import create_indicators
from software_patents.data_management.scrape_patents import multiprocessed
from software_patents.data_management.scrape_patents import scrape_patent_info


@pytask.mark.depends_on(SRC / "data" / "external" / "bessen_hunt_2007.dta")
@pytask.mark.produces(
    {
        "bh": BLD / "data" / "bh.pkl",
        "bh_w_text": BLD / "data" / "bh_with_crawled_text.pkl",
    }
)
def task_prepare_bessen_hunt_2007(depends_on, produces):
    # Read the dataset of BH2007
    df = pd.read_stata(depends_on)

    # Setting the correct column names
    dict_columns = {
        "patent": "ID",
        "sw": "CLASSIFICATION_BASE",
        "mowpat": "CLASSIFICATION_MOWERY",
        "swpat2": "CLASSIFICATION_ALGORITHM",
    }

    df.rename(columns=dict_columns, inplace=True)

    # Split the original manual classification. The first is the one used in
    # the paper.
    df["CLASSIFICATION_MANUAL"] = df.CLASSIFICATION_BASE.isin([1, 2])
    df["CLASSIFICATION_MANUAL_ALT"] = df.CLASSIFICATION_BASE.eq(1)

    # Setting the correct dtypes
    df = df[df.columns.difference(["ID"])].astype(bool).join(df.ID)

    # Convert booleans to labels
    df.replace({False: "Non-Software", True: "Software"}, inplace=True)

    object_cols = df.select_dtypes(object).columns.tolist()
    df[object_cols] = df[object_cols].astype("category")

    # Exclude patent which is not available anymore
    df = df.loc[~df.ID.eq(5_785_646)]

    df.to_pickle(produces["bh"])

    # Crawl information from Google and append to existing data
    out = multiprocessed(scrape_patent_info, df.ID.values)
    out = pd.DataFrame(
        out,
        columns=[
            "ID",
            "TITLE",
            "ABSTRACT",
            "DESCRIPTION",
            "CLAIMS",
            "CLAIMS_NUMBER",
        ],
    )
    df = df.merge(out, on="ID", how="inner", validate="1:1")

    for column in ["ABSTRACT", "DESCRIPTION", "TITLE"]:
        df = create_indicators(df, column)

    df.to_pickle(produces["bh_w_text"])
