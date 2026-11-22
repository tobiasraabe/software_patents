"""Tests for fetching and parsing patent pages."""

import asyncio

import httpx2
import pytest

from software_patents.data_management.scrape_patents import _fetch_patent
from software_patents.data_management.scrape_patents import parse_patent_page


def test_fetch_patent_returns_successful_response() -> None:
    """Return a successful response's content for the requested patent."""

    def handle(request: httpx2.Request) -> httpx2.Response:
        assert str(request.url) == "https://patents.google.com/patent/US123"
        return httpx2.Response(200, content=b"patent")

    async def fetch() -> bytes:
        async with httpx2.AsyncClient(transport=httpx2.MockTransport(handle)) as client:
            return await _fetch_patent("123", client, asyncio.Semaphore(1))

    assert asyncio.run(fetch()) == b"patent"


@pytest.mark.parametrize("status", [404, 429, 500])
def test_fetch_patent_rejects_http_errors(status: int) -> None:
    """Do not parse error pages as patent content."""

    async def fetch() -> bytes:
        transport = httpx2.MockTransport(lambda _request: httpx2.Response(status))
        async with httpx2.AsyncClient(transport=transport) as client:
            return await _fetch_patent("123", client, asyncio.Semaphore(1))

    with pytest.raises(httpx2.HTTPStatusError) as exc:
        asyncio.run(fetch())
    assert exc.value.response.status_code == status


def test_parse_patent_page() -> None:
    """Extract the text fields from a patent page."""
    page = b"""
    <span itemprop="title">A device</span>
    <div class="abstract">Some abstract</div>
    <div class="description">The description</div>
    <div class="claims">The claims</div>
    <span itemprop="count">3</span>
    """
    assert parse_patent_page("123", page) == (
        "123",
        "A device",
        "Some abstract",
        "The description",
        "The claims",
        "3",
    )
