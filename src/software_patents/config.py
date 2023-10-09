"""This is the configuration of the project."""
from __future__ import annotations

import os
from pathlib import Path

import numpy as np


SRC = Path(__file__).parent.resolve()
BLD = SRC.joinpath("..", "..", "bld").resolve()


SEED = np.random.RandomState(42)
THREADS_SCRAPE_PATENTS = os.cpu_count() * 6
DASK_WORKER_NUMBER = os.cpu_count() - 1

DASK_LOCAL_CLUSTER_CONFIGURATION = {
    "memory_limit": 12e9,
    "n_workers": DASK_WORKER_NUMBER,
    "threads_per_worker": 1,
    "diagnostics_port": 8787,
}
