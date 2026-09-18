import pandas as pd

from src.data.preprocessing import (
    articles_to_dataframe,
)


def test_articles_to_dataframe():

    articles = [
        {
            "title": "Test Article",
            "description": "Description",
            "content": "Content",
            "url": "https://example.com/1",
            "published_at": (
                "2026-09-17T12:00:00Z"
            ),
            "source_name": "Example",
            "source_url": (
                "https://example.com"
            ),
            "fetched_at": (
                "2026-09-17T12:05:00Z"
            ),
        },
        {
            "title": "Test Article",
            "description": "Duplicate",
            "content": "Duplicate",
            "url": "https://example.com/1",
            "published_at": (
                "2026-09-17T12:00:00Z"
            ),
            "source_name": "Example",
            "source_url": (
                "https://example.com"
            ),
            "fetched_at": (
                "2026-09-17T12:05:00Z"
            ),
        },
    ]

    df = articles_to_dataframe(
        articles,
        collection_query="stock market",
    )

    assert len(df) == 1
    assert df.iloc[0]["title"] == "Test Article"
    assert (
        df.iloc[0]["collection_query"]
        == "stock market"
    )


def test_empty_articles():

    df = articles_to_dataframe([])

    assert isinstance(
        df,
        pd.DataFrame,
    )

    assert df.empty