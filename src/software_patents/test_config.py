"""Tests for the project configuration."""

from pytask import PickleNode

from software_patents.config import data_catalog


def test_replication_data_catalog_entries() -> None:
    """Replication inputs are registered without importing task modules."""
    names = (
        "indicators_abstract",
        *(f"indicators_description_{i}" for i in range(1, 6)),
        "indicators_title",
        "patent",
        "indicators_summary",
    )
    for name in names:
        node = data_catalog[name]
        assert isinstance(node, PickleNode)
        assert str(node.path) == f"s3://software-patents/{name}.pkl"
