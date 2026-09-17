import pandas as pd


def merge_sentiment_with_market(
    sentiment_df,
    market_df,
):
    """
    Merge daily news sentiment with market data.

    Only dates appearing in both datasets are retained.
    """

    sentiment = sentiment_df.copy()
    market = market_df.copy()

    sentiment["date"] = pd.to_datetime(
        sentiment["date"]
    ).dt.date

    market["date"] = pd.to_datetime(
        market["date"]
    ).dt.date

    merged = sentiment.merge(
        market,
        on="date",
        how="inner",
    )

    return merged
