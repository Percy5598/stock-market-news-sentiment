import pandas as pd


def build_session_features(
    aligned_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Aggregate article-level news and market information
    into trading-session-level features.
    """

    data = aligned_df.copy()

    required_columns = [
        "date",
        "title",
        "sentiment_score",
        "sentiment",
        "market_session",
        "return",
        "next_trading_day_return",
        "five_trading_day_forward_return",
    ]

    missing = [
        column
        for column in required_columns
        if column not in data.columns
    ]

    if missing:
        raise ValueError(
            f"Missing required columns: {missing}"
        )

    # ---------------------------------------------------------
    # Sentiment indicators
    # ---------------------------------------------------------

    data["is_positive"] = (
        data["sentiment"] == "Positive"
    ).astype(int)

    data["is_negative"] = (
        data["sentiment"] == "Negative"
    ).astype(int)

    data["is_neutral"] = (
        data["sentiment"] == "Neutral"
    ).astype(int)

    # ---------------------------------------------------------
    # Aggregate article-level data by trading session
    # ---------------------------------------------------------

    session = (
        data.groupby("date")
        .agg(
            article_count=("title", "count"),
            mean_sentiment=("sentiment_score", "mean"),
            median_sentiment=("sentiment_score", "median"),
            sentiment_std=("sentiment_score", "std"),
            positive_articles=("is_positive", "sum"),
            negative_articles=("is_negative", "sum"),
            neutral_articles=("is_neutral", "sum"),
            market_return=("return", "first"),
            next_trading_day_return=(
                "next_trading_day_return",
                "first",
            ),
            five_trading_day_forward_return=(
                "five_trading_day_forward_return",
                "first",
            ),
        )
        .reset_index()
    )

    # ---------------------------------------------------------
    # Sentiment proportions
    # ---------------------------------------------------------

    session["positive_share"] = (
        session["positive_articles"]
        / session["article_count"]
    )

    session["negative_share"] = (
        session["negative_articles"]
        / session["article_count"]
    )

    session["neutral_share"] = (
        session["neutral_articles"]
        / session["article_count"]
    )

    # ---------------------------------------------------------
    # Overall sentiment intensity
    # ---------------------------------------------------------

    session["sentiment_intensity"] = (
        session["mean_sentiment"].abs()
    )

    # ---------------------------------------------------------
    # Sentiment by publication timing
    # ---------------------------------------------------------

    session_types = [
        "pre_market",
        "market_hours",
        "after_market",
        "non_trading_day",
    ]

    for market_session in session_types:

        subset = data[
            data["market_session"] == market_session
        ]

        if subset.empty:
            continue

        grouped = (
            subset.groupby("date")["sentiment_score"]
            .mean()
            .rename(
                f"{market_session}_sentiment"
            )
        )

        session = session.merge(
            grouped,
            on="date",
            how="left",
        )

    # ---------------------------------------------------------
    # Sort chronologically
    # ---------------------------------------------------------

    session = session.sort_values(
        "date"
    ).reset_index(drop=True)

    return session