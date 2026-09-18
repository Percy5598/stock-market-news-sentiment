import pandas as pd


def prepare_news_timestamps(df):
    data = df.copy()

    data["published_at"] = pd.to_datetime(
        data["published_at"],
        errors="coerce",
        utc=True,
    )

    data = data.dropna(
        subset=["published_at"]
    )

    data["published_at_et"] = (
        data["published_at"]
        .dt.tz_convert("America/New_York")
    )

    data["publication_date"] = (
        data["published_at_et"]
        .dt.date
    )

    data["publication_time"] = (
        data["published_at_et"]
        .dt.time
    )

    data["weekday"] = (
        data["published_at_et"]
        .dt.dayofweek
    )

    return data


def classify_market_session(df):
    data = df.copy()

    market_open = pd.Timestamp(
        "09:30"
    ).time()

    market_close = pd.Timestamp(
        "16:00"
    ).time()

    time = data["published_at_et"].dt.time

    # Monday = 0
    # Friday = 4
    # Saturday = 5
    # Sunday = 6

    weekday = (
        data["published_at_et"]
        .dt.dayofweek
    )

    # Weekends are not trading sessions.
    data["market_session"] = "non_trading_day"

    weekday_mask = weekday < 5

    data.loc[
        weekday_mask,
        "market_session",
    ] = "after_market"

    data.loc[
        weekday_mask
        & (time < market_open),
        "market_session",
    ] = "pre_market"

    data.loc[
        weekday_mask
        & (time >= market_open)
        & (time < market_close),
        "market_session",
    ] = "market_hours"

    return data


def prepare_temporal_news_data(df):
    data = prepare_news_timestamps(df)

    data = classify_market_session(
        data
    )

    return data