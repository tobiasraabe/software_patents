# Install the project and typing dependencies.
install:
    uv sync --group typing

# Refresh the uv lockfile.
lock:
    uv lock

# Run all pre-commit hooks.
lint:
    uvx pre-commit run --all-files

# Run the type checker.
typing:
    uv run --group typing ty check

# Run the test suite.
test:
    uv run pytest

# Run the pytask pipeline.
build:
    uv run pytask

# Run the default local checks.
check: lint typing test
