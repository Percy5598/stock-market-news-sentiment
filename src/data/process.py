from pathlib import Path

import pandas as pd

from src.nlp.sentiment_pipeline import add_sentiment_features


RAW_PATH = Path("data/raw/news.csv")
PROCESSED_PATH = Path(
    "data/processed/news_sentiment.csv"
)


def process_news():

    if not RAW_PATH.exists():
        raise FileNotFoundError(
            f"Raw dataset not found: {RAW_PATH}"
        )

    df = pd.read_csv(RAW_PATH)

    if df.empty:
        raise ValueError(
            "Raw dataset is empty."
        )

    # Make sure publication dates are timestamps
    df["published_at"] = pd.to_datetime(
        df["published_at"],
        errors="coerce",
        utc=True,
    )

    # Remove records without timestamps
    df = df.dropna(
        subset=["published_at"]
    )

    # Add NLP features
    df = add_sentiment_features(df)

    # Sort chronologically
    df = df.sort_values(
        "published_at"
    )

    PROCESSED_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_csv(
        PROCESSED_PATH,
        index=False,
    )

    return df