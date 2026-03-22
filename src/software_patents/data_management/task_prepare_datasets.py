"""Create datasets from the raw data or copies processed and downloaded files.

The dynamic task creation needs to be better supported by pytask.

"""

from __future__ import annotations

from pathlib import Path
from typing import cast

from pytask import PickleNode
from upath import UPath

from software_patents.config import Mode
from software_patents.config import ProjectMode
from software_patents.config import data_catalog

_BaseURL = "s3://software-patents"


def _pickle_node(name: str) -> PickleNode:
    return PickleNode(path=cast(Path, UPath(f"{_BaseURL}/{name}.pkl")))


if ProjectMode == Mode.REPLICATION:
    data_catalog.add(
        "indicators_abstract",
        _pickle_node("indicators_abstract"),
    )
    data_catalog.add(
        "indicators_description_1",
        _pickle_node("indicators_description_1"),
    )
    data_catalog.add(
        "indicators_description_2",
        _pickle_node("indicators_description_2"),
    )
    data_catalog.add(
        "indicators_description_3",
        _pickle_node("indicators_description_3"),
    )
    data_catalog.add(
        "indicators_description_4",
        _pickle_node("indicators_description_4"),
    )
    data_catalog.add(
        "indicators_description_5",
        _pickle_node("indicators_description_5"),
    )
    data_catalog.add(
        "indicators_title",
        _pickle_node("indicators_title"),
    )
    data_catalog.add(
        "patent",
        _pickle_node("patent"),
    )
    data_catalog.add(
        "indicators_summary",
        _pickle_node("indicators_summary"),
    )

elif ProjectMode == Mode.RAW:
    # Needs to be reimplemented since data is not available anymore.
    ...

else:
    msg = f"ProjectMode {ProjectMode} is not implemented."
    raise NotImplementedError(msg)
