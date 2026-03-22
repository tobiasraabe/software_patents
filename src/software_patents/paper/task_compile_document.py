"""Contains code for compiling the thesis."""

from __future__ import annotations

from pytask import mark

from software_patents.config import BLD
from software_patents.config import SRC


@mark.latex(script=SRC / "paper" / "thesis.tex", document=BLD / "paper" / "thesis.pdf")
def task_compile_thesis() -> None:
    pass
