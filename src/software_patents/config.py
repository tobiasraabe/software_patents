"""Configuration of the project."""

from __future__ import annotations

import os
from concurrent.futures import Executor
from enum import Enum
from enum import auto
from pathlib import Path
from typing import cast

import coiled
import numpy as np
from pytask import DataCatalog
from pytask import PickleNode
from pytask_parallel import ParallelBackend
from pytask_parallel import registry
from upath import UPath


class Mode(Enum):
    """Mode of the project."""

    REPLICATION = auto()
    RAW = auto()


ProjectMode = Mode.REPLICATION


SRC = Path(__file__).parent.resolve()
BLD = SRC.joinpath("..", "..", "bld").resolve()


SEED = np.random.RandomState(42)
THREADS_SCRAPE_PATENTS = min((os.cpu_count() or 1) * 2, 32)

data_catalog = DataCatalog()

if ProjectMode == Mode.REPLICATION:
    for name in (
        "indicators_abstract",
        *(f"indicators_description_{i}" for i in range(1, 6)),
        "indicators_title",
        "patent",
        "indicators_summary",
    ):
        path = UPath(f"s3://software-patents/{name}.pkl", anon=True)
        data_catalog.add(name, PickleNode(name=name, path=cast(Path, path)))
elif ProjectMode == Mode.RAW:
    # Needs to be reimplemented since data is not available anymore.
    ...
else:
    msg = f"ProjectMode {ProjectMode} is not implemented."
    raise NotImplementedError(msg)


def build_custom_backend(n_workers: int) -> Executor:
    """Build custom executor."""
    cluster = coiled.Cluster(  # ty: ignore[invalid-argument-type]
        name="software-patents",
        n_workers=n_workers,
    )
    return cast(Executor, cluster.get_client().get_executor())


registry.register_parallel_backend(
    ParallelBackend.CUSTOM, build_custom_backend, worker_type="processes", remote=True
)
