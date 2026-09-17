from pathlib import Path

import pandas as pd


RAW_DATA_PATH = Path("data/raw/news.csv")


def save_news_data(df: pd.DataFrame):
    """
    Save news data to the raw data directory.
    """

    RAW_DATA_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_csv(
        RAW_DATA_PATH,
        index=False,
    )

    return RAW_DATA_PATH
