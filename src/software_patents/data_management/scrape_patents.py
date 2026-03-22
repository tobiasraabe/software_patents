"""Contains code to scrape patents by patent ids."""

from __future__ import annotations

from typing import Union

import httpx
import numpy as np
from bs4 import BeautifulSoup
from bs4 import Tag

PatentField = Union[str, float]


async def fetch_patent(patentnr: str) -> bytes:
    """Scrape a patent and return its content."""
    async with httpx.AsyncClient(timeout=10.0) as client:
        result = await client.get(f"https://patents.google.com/patent/US{patentnr}")
        return result.content


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
