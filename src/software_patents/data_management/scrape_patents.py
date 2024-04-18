"""Contains code to scrape patents by patent ids."""

from __future__ import annotations

import httpx
import numpy as np
from bs4 import BeautifulSoup


async def fetch_patent(patentnr: str) -> bytes:
    """Scrape a patent and return its content."""
    async with httpx.AsyncClient(timeout=10.0) as client:
        result = await client.get(f"https://patents.google.com/patent/US{patentnr}")
        return result.content


def parse_patent_page(patentnr: str, page_content: bytes) -> tuple[str, ...]:
    """Parse the patent page."""
    soup = BeautifulSoup(page_content, "html.parser")

    try:
        title = soup.find("span", itemprop="title").get_text(strip=True, separator=" ")
    except AttributeError:
        title = np.nan

    try:
        abstract = soup.findAll(attrs={"class": "abstract"})
        abstract = [tag.get_text(strip=True) for tag in abstract]
        abstract = " ".join(abstract)
    except AttributeError:
        abstract = np.nan

    try:
        description = soup.find(attrs={"class": "description"}).get_text(
            strip=True, separator=" "
        )
    except AttributeError:
        description = np.nan

    try:
        claims = soup.find(attrs={"class": "claims"}).get_text(
            strip=True, separator=" "
        )
    except AttributeError:
        claims = np.nan

    try:
        claims_number = soup.find("span", itemprop="count").get_text(
            strip=True, separator=" "
        )
    except AttributeError:
        claims_number = np.nan

    return patentnr, title, abstract, description, claims, claims_number
