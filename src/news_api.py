import os
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("GNEWS_API_KEY")

URL = "https://gnews.io/api/v4/search"


def get_financial_news(max_articles=10):
    """
    Fetch financial news articles from GNews.

    Returns:
        list[dict]: Raw article records.
    """

    if not API_KEY:
        raise ValueError(
            "GNEWS_API_KEY is not set. "
            "Add it to your .env file."
        )

    params = {
        "q": "stock market OR stocks OR Wall Street",
        "lang": "en",
        "country": "us",
        "max": max_articles,
        "apikey": API_KEY,
    }

    response = requests.get(
        URL,
        params=params,
        timeout=10,
    )

    response.raise_for_status()

    data = response.json()

    articles = data.get("articles", [])

    fetched_at = datetime.now(timezone.utc).isoformat()

    records = []

    for article in articles:

        source = article.get("source") or {}

        records.append(
            {
                "title": article.get("title"),
                "description": article.get("description"),
                "content": article.get("content"),
                "url": article.get("url"),
                "published_at": article.get("publishedAt"),
                "source_name": source.get("name"),
                "source_url": source.get("url"),
                "fetched_at": fetched_at,
            }
        )

    return records