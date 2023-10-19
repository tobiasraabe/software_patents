"""This is the configuration of the project."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any
from typing import Callable

import numpy as np
import pandas as pd
from attrs import define
from pytask import DataCatalog
from pytask import PickleNode


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


@define
class PandasPickleNode(PickleNode):
    load_func: Callable[[bytes], Any] = pd.read_pickle
    dump_func: Callable[[Any, Path], bytes] = pd.to_pickle

    def load(self) -> Any:
        return self.load_func(self.path)

    def save(self, value: Any) -> None:
        self.dump_func(value, self.path)


data_catalog = DataCatalog(default_node=PandasPickleNode)
