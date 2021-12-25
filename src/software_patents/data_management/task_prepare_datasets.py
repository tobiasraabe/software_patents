"""This module flexibly creates intermediate datasets from the raw data or copies
processed and downloaded files.

The dynamic task creation needs to be better supported by pytask.

"""
import functools
import shutil

import pytask
from software_patents.config import BLD
from software_patents.config import SRC
from software_patents.data_management.prepare_description import prepare_description
from software_patents.data_management.prepare_patents import prepare_patents
from software_patents.data_management.prepare_summary import prepare_summary


paths_to_copy = []

for i in range(1, 6):
    # Path is relative to the project directory
    path = SRC / "data" / "processed" / f"indicators_description_{i}.pkl"

    if not path.exists():
        depends_on = pytask.mark.depends_on(
            {
                j: SRC / "data" / "raw" / f"detail_desc_text_{i}_{j}.parquet"
                for j in range(1, 126)
            }
        )
        produces = pytask.mark.produces(
            BLD / "data" / f"indicators_description_{i}.pkl"
        )
        task_func = functools.partial(prepare_description, part=str(i))

        locals()[f"task_prepare_description_{i}"] = produces(depends_on(task_func))

    else:
        paths_to_copy.append(path)


# Paths are relative to the project directory.
paths = {
    path.name: path
    for path in (
        SRC / "data" / "processed" / "indicators_abstract.pkl",
        SRC / "data" / "processed" / "indicators_title.pkl",
        SRC / "data" / "processed" / "patent.pkl",
    )
}
if not all(path.exists() for path in paths.values()):

    depends_on = pytask.mark.depends_on(
        {
            "bh": BLD / "data" / "bh.pkl",
            **{f"patent_{i}": SRC / "data" / "raw" / f"patent_{i}.parquet"},
        }
    )
    produces = pytask.mark.produces(paths)
    locals()["task_prepare_patents"] = produces(depends_on(prepare_patents))

else:
    paths_to_copy.extend(list(paths.values()))


# Paths are relative to the project directory.
path = SRC / "data" / "processed" / "indicators_summary.pkl"
if not path.exists():

    depends_on = pytask.mark.depends_on(
        {
            "bh": BLD / "data" / "bh.pkl",
            **{f"brf_sum_text_{i}": SRC / "data" / "raw" / f"brf_sum_text_{i}.parquet"},
        }
    )
    produces = BLD / "data" / "indicators_summary.pkl"
    locals()["task_prepare_summary"] = produces(depends_on(prepare_summary))

else:
    paths_to_copy.append(path)


if paths_to_copy:

    @pytask.mark.parametrize(
        "depends_on, produces",
        [(path, BLD / "data" / path.name) for path in paths_to_copy],
    )
    def task_copy_files(depends_on, produces):
        shutil.copyfile(depends_on, produces)
