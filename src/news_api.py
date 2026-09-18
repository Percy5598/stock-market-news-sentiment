import os
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv


load_dotenv()

GNEWS_URL = "https://gnews.io/api/v4/search"


class GNewsAPIError(RuntimeError):
    """Raised when the GNews API request fails."""


def get_financial_news(
    query: str = "stock market",
    max_articles: int = 10,
    from_date: str | None = None,
    to_date: str | None = None,
) -> list[dict]:
    """
    Retrieve financial/news articles from GNews.

    Parameters
    ----------
    query:
        GNews search query.
    max_articles:
        Maximum number of articles requested.
    from_date:
        Optional ISO-8601 start timestamp.
    to_date:
        Optional ISO-8601 end timestamp.

    Returns
    -------
    list[dict]
        Normalized article records.
    """

    api_key = os.getenv("GNEWS_API_KEY")

    if not api_key:
        raise GNewsAPIError(
            "GNEWS_API_KEY is not set. "
            "Create a .env file and add your API key."
        )

    if max_articles < 1:
        raise ValueError("max_articles must be at least 1.")

    params = {
        "q": query,
        "lang": "en",
        "country": "us",
        "max": max_articles,
        "apikey": api_key,
    }

    if from_date:
        params["from"] = from_date

    if to_date:
        params["to"] = to_date

    try:
        response = requests.get(
            GNEWS_URL,
            params=params,
            timeout=20,
        )
    except requests.RequestException as error:
        raise GNewsAPIError(
            f"Network error while contacting GNews: {error}"
        ) from error

    if response.status_code != 200:
        try:
            detail = response.json()
        except ValueError:
            detail = response.text[:500]

        raise GNewsAPIError(
            f"GNews request failed with HTTP "
            f"{response.status_code}: {detail}"
        )

    try:
        payload = response.json()
    except ValueError as error:
        raise GNewsAPIError(
            "GNews returned an invalid JSON response."
        ) from error

    articles = payload.get("articles", [])

    fetched_at = datetime.now(
        timezone.utc
    ).isoformat()

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