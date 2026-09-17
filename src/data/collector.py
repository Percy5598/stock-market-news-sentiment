from pathlib import Path

import pandas as pd

from src.news_api import get_financial_news
from src.data.preprocessing import articles_to_dataframe


RAW_PATH = Path("data/raw/news.csv")


def collect_news(max_articles=10):
    """
    Fetch and clean one batch of financial news.
    """

    articles = get_financial_news(
        max_articles=max_articles
    )

    return articles_to_dataframe(articles)


def append_news_data(df):
    """
    Append new raw news to the existing dataset
    and remove duplicate articles.
    """

    RAW_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if RAW_PATH.exists():

        existing = pd.read_csv(
            RAW_PATH
        )

        combined = pd.concat(
            [existing, df],
            ignore_index=True,
        )

    else:

        combined = df.copy()

    # Remove duplicate URLs
    if "url" in combined.columns:

        combined = combined.drop_duplicates(
            subset=["url"],
            keep="first",
        )

    # Remove duplicate titles
    combined = combined.drop_duplicates(
        subset=["title"],
        keep="first",
    )

    combined.to_csv(
        RAW_PATH,
        index=False,
    )

    return combined