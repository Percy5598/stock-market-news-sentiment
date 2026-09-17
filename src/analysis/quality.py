import pandas as pd


def validate_sentiment_data(df):
    """
    Run basic quality checks on sentiment data.
    """

    checks = {}

    checks["rows"] = len(df)

    checks["missing_titles"] = (
        df["title"]
        .isna()
        .sum()
    )

    checks["duplicate_urls"] = (
        df["url"]
        .duplicated()
        .sum()
    )

    checks["missing_dates"] = (
        df["published_at"]
        .isna()
        .sum()
    )

    checks["invalid_sentiment_scores"] = (
        (
            (df["sentiment_score"] < -1)
            |
            (df["sentiment_score"] > 1)
        )
        .sum()
    )

    checks["sentiment_labels"] = (
        df["sentiment"]
        .value_counts()
        .to_dict()
    )

    return checks
