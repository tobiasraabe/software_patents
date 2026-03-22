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
from pytask_parallel import ParallelBackend
from pytask_parallel import registry


class Mode(Enum):
    """Mode of the project."""

    REPLICATION = auto()
    RAW = auto()


ProjectMode = Mode.REPLICATION


SRC = Path(__file__).parent.resolve()
BLD = SRC.joinpath("..", "..", "bld").resolve()


SEED = np.random.RandomState(42)
THREADS_SCRAPE_PATENTS = (os.cpu_count() or 1) * 6

data_catalog = DataCatalog()


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
