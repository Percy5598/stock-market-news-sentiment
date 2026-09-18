from pathlib import Path

import pandas as pd

from src.data.preprocessing import (
    articles_to_dataframe,
)
from src.news_api import (
    get_financial_news,
)


RAW_PATH = Path(
    "data/raw/news.csv"
)


def collect_news(
    query: str = "stock market",
    max_articles: int = 10,
) -> pd.DataFrame:

    articles = get_financial_news(
        query=query,
        max_articles=max_articles,
    )

    return articles_to_dataframe(
        articles,
        collection_query=query,
    )


def append_news_data(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Append new articles to the raw dataset.

    Deduplication:
        1. URL
        2. title
    """

    RAW_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if df.empty:
        if RAW_PATH.exists():
            return pd.read_csv(
                RAW_PATH
            )

        return df.copy()

    df = df.copy()

    if RAW_PATH.exists():

        existing = pd.read_csv(
            RAW_PATH
        )

        # Ensure both DataFrames have
        # the same columns.
        for column in df.columns:

            if column not in existing.columns:
                existing[column] = None

        for column in existing.columns:

            if column not in df.columns:
                df[column] = None

        columns = list(
            dict.fromkeys(
                list(existing.columns)
                + list(df.columns)
            )
        )

        existing = existing.reindex(
            columns=columns
        )

        df = df.reindex(
            columns=columns
        )

        combined = pd.concat(
            [
                existing,
                df,
            ],
            ignore_index=True,
        )

    else:

        combined = df.copy()

    combined["title"] = (
        combined["title"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    combined["url"] = (
        combined["url"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    # URL-level deduplication.
    with_url = combined[
        combined["url"] != ""
    ].drop_duplicates(
        subset=["url"],
        keep="first",
    )

    without_url = combined[
        combined["url"] == ""
    ]

    combined = pd.concat(
        [
            with_url,
            without_url,
        ],
        ignore_index=True,
    )

    # Title-level deduplication.
    combined = combined.drop_duplicates(
        subset=["title"],
        keep="first",
    )

    if "published_at" in combined.columns:

        combined["published_at"] = pd.to_datetime(
            combined["published_at"],
            errors="coerce",
            utc=True,
        )

        combined = combined.sort_values(
            "published_at",
            na_position="last",
        )

    combined.to_csv(
        RAW_PATH,
        index=False,
    )

    return combined.reset_index(
        drop=True
    )