import os
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("GNEWS_API_KEY")

URL = "https://gnews.io/api/v4/search"


def get_financial_news(
    query="stock market",
    max_articles=10,
    from_date=None,
    to_date=None,
):
    """
    Fetch financial news articles from GNews.

    Parameters
    ----------
    max_articles : int
        Maximum number of articles to request.

    from_date : str, optional
        Start date/time in ISO format.

    to_date : str, optional
        End date/time in ISO format.
    """

    if not API_KEY:
        raise ValueError(
            "GNEWS_API_KEY is not set. "
            "Add it to your .env file."
        )

    params = {
        "q": query,
        "lang": "en",
        "country": "us",
        "max": max_articles,
        "apikey": API_KEY,
    }

    if from_date:
        params["from"] = from_date

    if to_date:
        params["to"] = to_date

    response = requests.get(
        URL,
        params=params,
        timeout=10,
    )

    response.raise_for_status()

    data = response.json()

    articles = data.get("articles", [])

    fetched_at = datetime.now(
        timezone.utc
    ).isoformat()

    records = []

    for article in articles:

        source = article.get(
            "source"
        ) or {}

        records.append(
            {
                "title": article.get(
                    "title"
                ),
                "description": article.get(
                    "description"
                ),
                "content": article.get(
                    "content"
                ),
                "url": article.get(
                    "url"
                ),
                "published_at": article.get(
                    "publishedAt"
                ),
                "source_name": source.get(
                    "name"
                ),
                "source_url": source.get(
                    "url"
                ),
                "fetched_at": fetched_at,
            }
        )

    return records