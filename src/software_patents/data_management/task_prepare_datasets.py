"""Create datasets from the raw data or copies processed and downloaded files.

The dynamic task creation needs to be better supported by pytask.

"""

from __future__ import annotations

from pytask import PickleNode
from pytask import task

from software_patents.config import BLD
from software_patents.config import SRC
from software_patents.config import data_catalog
from software_patents.data_management.prepare_description import prepare_description
from software_patents.data_management.prepare_patents import merge_indicators
from software_patents.data_management.prepare_patents import prepare_patents
from software_patents.data_management.prepare_summary import prepare_summary

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
            produces=data_catalog[f"indicators_description_{i}"],
        )(prepare_description)

    else:
        data_catalog.add(f"indicators_description_{i}", PickleNode.from_path(path))


# Paths are relative to the project directory.
paths = {
    path.stem: path
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
            kwargs={"section": section}, produces=data_catalog[f"indicators_{section}"]
        )(merge_indicators)
else:
    data_catalog.add(
        "indicators_abstract", PickleNode.from_path(paths["indicators_abstract"])
    )
    data_catalog.add(
        "indicators_title", PickleNode.from_path(paths["indicators_title"])
    )
    data_catalog.add("patent", PickleNode.from_path(paths["patent"]))


# Paths are relative to the project directory.
path = SRC / "data" / "processed" / "indicators_summary.pkl"
if not path.exists():
    task(produces=data_catalog["indicators_summary"])(prepare_summary)
else:
    data_catalog.add("indicators_summary", PickleNode.from_path(path))
