"""Create datasets from the raw data or copies processed and downloaded files.

The dynamic task creation needs to be better supported by pytask.

"""

from __future__ import annotations

from pytask import PickleNode
from upath import UPath

from software_patents.config import Mode
from software_patents.config import ProjectMode
from software_patents.config import data_catalog

_BaseURL = "s3://software-patents"

if ProjectMode == Mode.REPLICATION:
    data_catalog.add(
        "indicators_abstract",
        PickleNode(path=UPath(f"{_BaseURL}/indicators_abstract.pkl")),
    )
    data_catalog.add(
        "indicators_description_1",
        PickleNode(path=UPath(f"{_BaseURL}/indicators_description_1.pkl")),
    )
    data_catalog.add(
        "indicators_description_2",
        PickleNode(path=UPath(f"{_BaseURL}/indicators_description_2.pkl")),
    )
    data_catalog.add(
        "indicators_description_3",
        PickleNode(path=UPath(f"{_BaseURL}/indicators_description_3.pkl")),
    )
    data_catalog.add(
        "indicators_description_4",
        PickleNode(path=UPath(f"{_BaseURL}/indicators_description_4.pkl")),
    )
    data_catalog.add(
        "indicators_description_5",
        PickleNode(path=UPath(f"{_BaseURL}/indicators_description_5.pkl")),
    )
    data_catalog.add(
        "indicators_title",
        PickleNode(path=UPath(f"{_BaseURL}/indicators_title.pkl")),
    )
    data_catalog.add(
        "patent",
        PickleNode(path=UPath(f"{_BaseURL}/patent.pkl")),
    )
    data_catalog.add(
        "indicators_summary",
        PickleNode(path=UPath(f"{_BaseURL}/indicators_summary.pkl")),
    )

elif ProjectMode == Mode.RAW:
    # Needs to be reimplemented since data is not available anymore.
    ...

else:
    msg = f"ProjectMode {ProjectMode} is not implemented."
    raise NotImplementedError(msg)
