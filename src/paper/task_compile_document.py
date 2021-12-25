import pytask

from src.config import BLD
from src.config import SRC


@pytask.mark.latex
@pytask.mark.depends_on(SRC / "paper" / "thesis.tex")
@pytask.mark.produces(BLD / "paper" / "thesis.pdf")
def task_compile_thesis():
    pass
