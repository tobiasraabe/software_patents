"""Create datasets from the raw data or copies processed and downloaded files.

The dynamic task creation needs to be better supported by pytask.

"""
from __future__ import annotations

from pytask import PickleNode
from software_patents.config import data_catalog
from software_patents.config import Mode
from software_patents.config import ProjectMode
from upath import UPath

if ProjectMode == Mode.REPLICATION:
    data_catalog.add(
        "indicators_abstract",
        PickleNode(
            path=UPath(
                "http://dl.dropboxusercontent.com/s/ckleerbtm54ddpm/indicators_abstract.pkl?dl=0"
            )
        ),
    )
    data_catalog.add(
        "indicators_description_1",
        PickleNode(
            path=UPath(
                "http://dl.dropboxusercontent.com/s/tfhzex5o18ocugu/indicators_description_1.pkl?dl=0"
            )
        ),
    )
    data_catalog.add(
        "indicators_description_2",
        PickleNode(
            path=UPath(
                "http://dl.dropboxusercontent.com/s/ayvvzdzr8kihx4e/indicators_description_2.pkl?dl=0"
            )
        ),
    )
    data_catalog.add(
        "indicators_description_3",
        PickleNode(
            path=UPath(
                "http://dl.dropboxusercontent.com/s/frnos85yq97sps4/indicators_description_3.pkl?dl=0"
            )
        ),
    )
    data_catalog.add(
        "indicators_description_4",
        PickleNode(
            path=UPath(
                "http://dl.dropboxusercontent.com/s/hsswas2hgwvb8et/indicators_description_4.pkl?dl=0"
            )
        ),
    )
    data_catalog.add(
        "indicators_description_5",
        PickleNode(
            path=UPath(
                "http://dl.dropboxusercontent.com/s/42but1qhjil1trg/indicators_description_5.pkl?dl=0"
            )
        ),
    )
    data_catalog.add(
        "indicators_title",
        PickleNode(
            path=UPath(
                "http://dl.dropboxusercontent.com/s/0fxqnvyhsljwprt/indicators_title.pkl?dl=0"
            )
        ),
    )
    data_catalog.add(
        "patent",
        PickleNode(
            path=UPath(
                "http://dl.dropboxusercontent.com/s/atu4974la2p8d5s/patent.pkl?dl=0"
            )
        ),
    )
    data_catalog.add(
        "indicators_summary",
        PickleNode(
            path=UPath(
                "http://dl.dropboxusercontent.com/s/8mffjyvintl757a/indicators_summary.pkl?dl=0"
            )
        ),
    )

elif ProjectMode == Mode.RAW:
    # Needs to be reimplemented since data is not available anymore.
    ...

else:
    msg = f"ProjectMode {ProjectMode} is not implemented."
    raise NotImplementedError(msg)
