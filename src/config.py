"""This is the configuration of the project."""
from pathlib import Path


SRC = Path(__file__).parent.resolve()
BLD = SRC.joinpath("..", "bld").resolve()
