import pandas as pd


def _get_trading_dates(
    market_df: pd.DataFrame,
) -> list[str]:

    market = market_df.copy()

    market["date"] = pd.to_datetime(
        market["date"],
        errors="coerce",
    )

    dates = (
        market["date"]
        .dropna()
        .dt.strftime(
            "%Y-%m-%d"
        )
        .drop_duplicates()
        .sort_values()
        .tolist()
    )

    return dates


def _first_trading_session_on_or_after(
    date_text: str,
    trading_dates: list[str],
):
    for trading_date in trading_dates:

        if trading_date >= date_text:
            return trading_date

    return None


def align_news_to_trading_sessions(
    news_df: pd.DataFrame,
    market_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Assign news to an information-relevant trading session.

    Rules:

    pre_market
        -> same trading session

    market_hours
        -> next trading session

    after_market
        -> next trading session

    non_trading_day
        -> next trading session

    Important:
        This function determines the session assignment.
        It does NOT establish causal or predictive validity
        of a particular return target.
    """

    news = news_df.copy()
    market = market_df.copy()

    news[
        "published_at_et"
    ] = pd.to_datetime(
        news[
            "published_at_et"
        ],
        errors="coerce",
    )

    news = news.dropna(
        subset=[
            "published_at_et"
        ]
    )

    news[
        "news_date"
    ] = (
        news[
            "published_at_et"
        ]
        .dt.tz_localize(
            None
        )
        .dt.strftime(
            "%Y-%m-%d"
        )
    )

    market["date"] = pd.to_datetime(
        market["date"],
        errors="coerce",
    )

    market = market.dropna(
        subset=["date"]
    )

    market[
        "market_date"
    ] = (
        market[
            "date"
        ].dt.strftime(
            "%Y-%m-%d"
        )
    )

    trading_dates = (
        _get_trading_dates(
            market
        )
    )

    news[
        "date"
    ] = news[
        "news_date"
    ].apply(
        lambda value:
        _first_trading_session_on_or_after(
            value,
            trading_dates,
        )
    )

    next_session_map = {
        trading_dates[index]:
        (
            trading_dates[index + 1]
            if index + 1
            < len(trading_dates)
            else None
        )
        for index in range(
            len(trading_dates)
        )
    }

    shift_mask = (
        news[
            "market_session"
        ].isin(
            [
                "market_hours",
                "after_market",
                "non_trading_day",
            ]
        )
    )

    news.loc[
        shift_mask,
        "date",
    ] = (
        news.loc[
            shift_mask,
            "date",
        ].map(
            next_session_map
        )
    )

    # Remove duplicate date column
    # before merge.
    market_for_merge = (
        market.drop(
            columns=[
                "date"
            ]
        )
    )

    aligned = news.merge(
        market_for_merge,
        left_on="date",
        right_on="market_date",
        how="left",
        validate="many_to_one",
    )

    aligned = aligned.drop(
        columns=[
            "news_date",
            "market_date",
        ],
        errors="ignore",
    )

    return aligned