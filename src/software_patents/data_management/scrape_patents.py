"""Contains code to scrape patents by patent ids."""

from __future__ import annotations

import asyncio
from typing import Union

import httpx
import numpy as np
from bs4 import BeautifulSoup
from bs4 import Tag

from software_patents.config import THREADS_SCRAPE_PATENTS

PatentField = Union[str, float]
_PATENT_URL = "https://patents.google.com/patent/US{patentnr}"


async def _fetch_patent(
    patentnr: str, client: httpx.AsyncClient, semaphore: asyncio.Semaphore
) -> bytes:
    async with semaphore:
        result = await client.get(_PATENT_URL.format(patentnr=patentnr))
        return result.content


async def fetch_patents(patentnrs: list[str]) -> list[bytes]:
    """Scrape patents while reusing one client and a bounded connection pool."""
    limits = httpx.Limits(
        max_connections=THREADS_SCRAPE_PATENTS,
        max_keepalive_connections=THREADS_SCRAPE_PATENTS,
    )
    semaphore = asyncio.Semaphore(THREADS_SCRAPE_PATENTS)
    async with httpx.AsyncClient(limits=limits, timeout=10.0) as client:
        tasks = [_fetch_patent(patentnr, client, semaphore) for patentnr in patentnrs]
        return await asyncio.gather(*tasks)


def _get_text(tag: Tag | None) -> PatentField:
    if tag is None:
        return np.nan
    return tag.get_text(strip=True, separator=" ")


def parse_patent_page(
    patentnr: str, page_content: bytes
) -> tuple[str, PatentField, PatentField, PatentField, PatentField, PatentField]:
    """Parse the patent page."""
    soup = BeautifulSoup(page_content, "html.parser")

    title = _get_text(soup.find("span", itemprop="title"))

    abstract_tags = soup.find_all(attrs={"class": "abstract"})
    if abstract_tags:
        abstract = " ".join(tag.get_text(strip=True) for tag in abstract_tags)
    else:
        abstract = np.nan

    description = _get_text(soup.find(attrs={"class": "description"}))
    claims = _get_text(soup.find(attrs={"class": "claims"}))
    claims_number = _get_text(soup.find("span", itemprop="count"))

    return patentnr, title, abstract, description, claims, claims_number
