import pandas as pd


def create_daily_sentiment(df):
    """
    Aggregate article-level sentiment into daily indicators.
    """

    data = df.copy()

    # Make sure timestamp is datetime
    data["published_at"] = pd.to_datetime(
        data["published_at"],
        errors="coerce",
        utc=True,
    )

    # Remove invalid timestamps
    data = data.dropna(
        subset=["published_at"]
    )

    # Extract calendar date
    data["date"] = (
        data["published_at"]
        .dt.date
    )

    # Create indicator variables
    data["is_positive"] = (
        data["sentiment"] == "Positive"
    ).astype(int)

    data["is_negative"] = (
        data["sentiment"] == "Negative"
    ).astype(int)

    data["is_neutral"] = (
        data["sentiment"] == "Neutral"
    ).astype(int)

    # Aggregate
    daily = (
        data
        .groupby("date")
        .agg(
            article_count=("title", "count"),
            mean_sentiment=("sentiment_score", "mean"),
            median_sentiment=("sentiment_score", "median"),
            sentiment_std=("sentiment_score", "std"),
            positive_articles=("is_positive", "sum"),
            negative_articles=("is_negative", "sum"),
            neutral_articles=("is_neutral", "sum"),
        )
        .reset_index()
    )

    # Convert counts to proportions
    daily["positive_pct"] = (
        daily["positive_articles"]
        / daily["article_count"]
    )

    daily["negative_pct"] = (
        daily["negative_articles"]
        / daily["article_count"]
    )

    daily["neutral_pct"] = (
        daily["neutral_articles"]
        / daily["article_count"]
    )

    # Sentiment intensity
    daily["sentiment_intensity"] = (
        daily["mean_sentiment"].abs()
    )

    return daily
