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
from software_patents.data_management.prepare_patents import merge_indicators
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
                "raw_descriptions": {
                    j: SRC / "data" / "raw" / f"detail_desc_text_{i}_{j}.parquet"
                    for j in range(1, 126)
                },
                "part": str(i),
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
    task()(prepare_patents)

    for section in ("abstract", "title"):
        task(
            kwargs={
                "section": section,
                "path_to_pkl": BLD / "data" / f"indicators_{section}.pkl",
            }
        )(merge_indicators)
else:
    paths_to_copy.extend(list(paths.values()))


# Paths are relative to the project directory.
path = SRC / "data" / "processed" / "indicators_summary.pkl"
if not path.exists():
    task()(prepare_summary)
else:
    paths_to_copy.append(path)


if paths_to_copy:
    for path in paths_to_copy:

        @task(name=path.name)
        def copy_files(path: Path = path, produces: Path = BLD / "data" / path.name):
            shutil.copyfile(path, produces)
