"""This module flexibly creates intermediate datasets from the raw data or copies
processed and downloaded files.

The dynamic task creation needs to be better supported by pytask.

"""
from __future__ import annotations

import shutil
from pathlib import Path

from pytask import task
from software_patents.config import BLD
from software_patents.config import SRC
from software_patents.data_management.prepare_description import prepare_description
from software_patents.data_management.prepare_patents import prepare_patents
from software_patents.data_management.prepare_summary import prepare_summary


paths_to_copy = []

for i in range(1, 6):
    # Path is relative to the project directory
    path = SRC / "data" / "processed" / f"indicators_description_{i}.pkl"

    if not path.exists():
        task(
            name=path.name,
            kwargs={
                "depends_on": {
                    j: SRC / "data" / "raw" / f"detail_desc_text_{i}_{j}.parquet"
                    for j in range(1, 126)
                },
                "part": str(i),
                "path_to_bh": BLD / "data" / "bh.pkl",
                "path_to_pkl": BLD / "data" / f"indicators_description_{i}.pkl",
            },
        )(prepare_description)

    else:
        paths_to_copy.append(path)


# Paths are relative to the project directory.
paths = {
    path.name: path
    for path in (
        SRC / "data" / "processed" / "indicators_abstract.pkl",
        SRC / "data" / "processed" / "indicators_title.pkl",
        SRC / "data" / "processed" / "patent.pkl",
    )
}
if not all(path.exists() for path in paths.values()):
    task(
        kwargs={
            "depends_on": {
                "bh": BLD / "data" / "bh.pkl",
                **{
                    f"patent_{i}": SRC / "data" / "raw" / f"patent_{i}.parquet"
                    for i in range(1, 6)
                },
            },
            "produces": paths,
        }
    )(prepare_patents)

else:
    paths_to_copy.extend(list(paths.values()))


# Paths are relative to the project directory.
path = SRC / "data" / "processed" / "indicators_summary.pkl"
if not path.exists():
    task(
        kwargs={
            "depends_on": {
                "bh": BLD / "data" / "bh.pkl",
                **{
                    f"brf_sum_text_{i}": SRC
                    / "data"
                    / "raw"
                    / f"brf_sum_text_{i}.parquet"
                    for i in range(1, 6)
                },
            },
            "produces": BLD / "data" / "indicators_summary.pkl",
        }
    )(prepare_summary)

else:
    paths_to_copy.append(path)


if paths_to_copy:
    for path in paths_to_copy:

        @task(name=path.name)
        def copy_files(path: Path = path, produces: Path = BLD / "data" / path.name):
            shutil.copyfile(path, produces)
