"""Configuration of the project."""
from __future__ import annotations

import os
from enum import auto
from enum import Enum
from pathlib import Path

import numpy as np
from pytask import DataCatalog


class Mode(Enum):
    """Mode of the project."""

    REPLICATION = auto()
    RAW = auto()


ProjectMode = Mode.REPLICATION


SRC = Path(__file__).parent.resolve()
BLD = SRC.joinpath("..", "..", "bld").resolve()


SEED = np.random.RandomState(42)
THREADS_SCRAPE_PATENTS = os.cpu_count() * 6  # type: ignore[operator]
DASK_WORKER_NUMBER = os.cpu_count() - 1  # type: ignore[operator]

DASK_LOCAL_CLUSTER_CONFIGURATION = {
    "memory_limit": 12e9,
    "n_workers": DASK_WORKER_NUMBER,
    "threads_per_worker": 1,
    "diagnostics_port": 8787,
}


data_catalog = DataCatalog()
