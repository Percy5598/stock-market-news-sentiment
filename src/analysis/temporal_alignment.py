import pandas as pd


NEW_YORK_TIMEZONE = (
    "America/New_York"
)


def prepare_temporal_news_data(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Convert publication timestamps to US Eastern Time.
    """

    data = df.copy()

    data["published_at"] = (
        pd.to_datetime(
            data["published_at"],
            errors="coerce",
            utc=True,
        )
    )

    data = data.dropna(
        subset=[
            "published_at"
        ]
    )

    data[
        "published_at_et"
    ] = (
        data[
            "published_at"
        ].dt.tz_convert(
            NEW_YORK_TIMEZONE
        )
    )

    data[
        "publication_date"
    ] = (
        data[
            "published_at_et"
        ].dt.date
    )

    data[
        "publication_time"
    ] = (
        data[
            "published_at_et"
        ].dt.time
    )

    data[
        "weekday"
    ] = (
        data[
            "published_at_et"
        ].dt.dayofweek
    )

    return classify_market_session(
        data
    )


def classify_market_session(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Classify publication timing relative
    to regular US equity-market hours.

    09:30–16:00 ET:
        market_hours

    Before 09:30 ET:
        pre_market

    After 16:00 ET:
        after_market

    Saturday/Sunday:
        non_trading_day
    """

    data = df.copy()

    market_open = pd.Timestamp(
        "09:30"
    ).time()

    market_close = pd.Timestamp(
        "16:00"
    ).time()

    publication_time = (
        data[
            "published_at_et"
        ].dt.time
    )

    weekday = (
        data[
            "published_at_et"
        ].dt.dayofweek
    )

    data[
        "market_session"
    ] = "non_trading_day"

    weekday_mask = (
        weekday < 5
    )

    data.loc[
        weekday_mask,
        "market_session",
    ] = "after_market"

    data.loc[
        weekday_mask
        & (
            publication_time
            < market_open
        ),
        "market_session",
    ] = "pre_market"

    data.loc[
        weekday_mask
        & (
            publication_time
            >= market_open
        )
        & (
            publication_time
            < market_close
        ),
        "market_session",
    ] = "market_hours"

    return data