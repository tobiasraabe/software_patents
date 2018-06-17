"""Contains variables shared over the project."""

import numpy as np
import os

SEED = np.random.RandomState(42)
PROCESSES_SCRAPE_PATENTS = os.cpu_count() * 6
DASK_THREAD_NUMBER = 2
