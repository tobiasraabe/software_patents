import pytask
from software_patents.config import BLD
from software_patents.config import SRC


@pytask.mark.latex
@pytask.mark.depends_on(SRC / "paper" / "thesis.tex")
@pytask.mark.produces(BLD / "paper" / "thesis.pdf")
def task_compile_thesis():
    pass
