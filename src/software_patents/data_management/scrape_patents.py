"""Contains code to scrape patents by patent ids."""

from __future__ import annotations

import numpy as np
import requests
from bs4 import BeautifulSoup


def scrape_patent_info(patentnr: str) -> tuple[str, ...]:
    """Scrape information on a single patent."""
    s = requests.Session()
    adapter = requests.adapters.HTTPAdapter(max_retries=3)
    s.mount("https://", adapter)

    url = f"https://www.google.de/patents/US{patentnr}"
    result = s.get(url)
    htmldoc = result.content
    soup = BeautifulSoup(htmldoc, "html.parser")

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
