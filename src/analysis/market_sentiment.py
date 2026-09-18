import pandas as pd


def merge_sentiment_with_market(
    sentiment_df,
    market_df,
):
    """
    Contemporaneous daily merge.

    Matches daily sentiment with the same trading date.

    This is descriptive rather than predictive because
    news may have been published after the market session
    began.
    """

    sentiment = sentiment_df.copy()
    market = market_df.copy()

    sentiment["date"] = (
        pd.to_datetime(
            sentiment["date"],
            errors="coerce",
        )
        .dt.strftime("%Y-%m-%d")
    )

    market["date"] = (
        pd.to_datetime(
            market["date"],
            errors="coerce",
        )
        .dt.strftime("%Y-%m-%d")
    )

    sentiment = sentiment.dropna(
        subset=["date"]
    )

    market = market.dropna(
        subset=["date"]
    )

    return sentiment.merge(
        market,
        on="date",
        how="inner",
        validate="one_to_one",
    )


def align_news_to_trading_sessions(
    news_df,
    market_df,
):
    """
    Align each news article with the relevant
    subsequent US equity trading session.

    Rules:

    pre-market:
        same trading session

    market-hours:
        next trading session

    after-market:
        next trading session

    non-trading day:
        next available trading session
    """

    news = news_df.copy()
    market = market_df.copy()

    # --------------------------------------------------
    # NEWS
    # --------------------------------------------------

    news["published_at_et"] = pd.to_datetime(
        news["published_at_et"],
        errors="coerce",
    )

    news = news.dropna(
        subset=["published_at_et"]
    )

    news["news_date"] = (
        news["published_at_et"]
        .dt.tz_localize(None)
        .dt.strftime("%Y-%m-%d")
    )

    # --------------------------------------------------
    # MARKET
    # --------------------------------------------------

    market["date"] = pd.to_datetime(
        market["date"],
        errors="coerce",
    )

    market = market.dropna(
        subset=["date"]
    )

    market["market_date"] = (
        market["date"]
        .dt.strftime("%Y-%m-%d")
    )

    # We don't need the original datetime column
    # for the alignment itself.
    market = market.drop(
        columns=["date"]
    )

    # --------------------------------------------------
    # TRADING CALENDAR
    # --------------------------------------------------

    trading_dates = (
        market["market_date"]
        .drop_duplicates()
        .sort_values()
        .tolist()
    )

    # --------------------------------------------------
    # FIRST TRADING SESSION ON OR AFTER NEWS DATE
    # --------------------------------------------------

    def first_trading_session(news_date):
        for trading_date in trading_dates:
            if trading_date >= news_date:
                return trading_date

        return None

    news["date"] = news["news_date"].apply(
        first_trading_session
    )

    # --------------------------------------------------
    # NEXT TRADING SESSION
    # --------------------------------------------------

    next_session_map = {
        trading_dates[i]: (
            trading_dates[i + 1]
            if i + 1 < len(trading_dates)
            else None
        )
        for i in range(len(trading_dates))
    }

    # --------------------------------------------------
    # NEWS THAT CANNOT EXPLAIN THE CURRENT SESSION
    # --------------------------------------------------

    shift_mask = news[
        "market_session"
    ].isin(
        [
            "market_hours",
            "after_market",
            "non_trading_day",
        ]
    )

    news.loc[
        shift_mask,
        "date",
    ] = news.loc[
        shift_mask,
        "date",
    ].map(
        next_session_map
    )

    # --------------------------------------------------
    # MERGE
    # --------------------------------------------------

    aligned = news.merge(
        market,
        left_on="date",
        right_on="market_date",
        how="left",
        validate="many_to_one",
    )

    # --------------------------------------------------
    # CLEANUP
    # --------------------------------------------------

    aligned = aligned.drop(
        columns=[
            "news_date",
            "market_date",
        ],
        errors="ignore",
    )

    return aligned