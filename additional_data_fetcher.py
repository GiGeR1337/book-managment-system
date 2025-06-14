import json
import logging
import os
from typing import Optional

import pandas as pd
import requests

logger = logging.getLogger(__name__)

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")
with open(CONFIG_PATH) as f:
    config = json.load(f)

API_AUTHOR_URL = config["api_endpoints"]["author_search"]
API_BOOK_URL = config["api_endpoints"]["book_search"]


def fetch_author_biography(author_name: str) -> Optional[str]:
    url = f"{API_AUTHOR_URL}{author_name}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data["docs"]:
            logger.debug("Fetched bio for %s", author_name)
            return data["docs"][0].get("bio", None)
    return None


def fetch_book_metadata(title: str) -> dict:
    url = f"{API_BOOK_URL}{title}"
    response = requests.get(url)
    result = {"division": None, "suggested_age": None}
    if response.status_code == 200:
        docs = response.json().get("docs", [])
        if docs:
            book = docs[0]
            result["division"] = book.get("publisher", [None])[0]
            result["suggested_age"] = book.get("reading_level", None)
    return result


def enrich_books(df: pd.DataFrame) -> pd.DataFrame:
    df["division"] = None
    df["author_bio"] = None
    df["suggested_age"] = None

    for i, row in df.iterrows():
        author = row.get("author")
        title = row.get("title")

        if pd.notna(author):
            df.at[i, "author_bio"] = fetch_author_biography(author)

        if pd.notna(title):
            metadata = fetch_book_metadata(title)
            df.at[i, "division"] = metadata["division"]
            df.at[i, "suggested_age"] = metadata["suggested_age"]

    logger.info("Metadata enrichment complete.")
    return df
