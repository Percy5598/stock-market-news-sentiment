import pandas as pd


def prepare_news_timestamps(df):
    """
    Convert publication timestamps to US Eastern Time.

    Financial markets in the US operate according to
    America/New_York trading hours.
    """

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

    return data


def classify_market_session(df):
    """
    Classify news according to US market session.

    Categories:

    pre_market
        Published before 09:30 ET.

    market_hours
        Published between 09:30 and 16:00 ET.

    after_market
        Published after 16:00 ET.
    """

    data = df.copy()

    time = data["published_at_et"].dt.time

    market_open = pd.Timestamp(
        "09:30"
    ).time()

    market_close = pd.Timestamp(
        "16:00"
    ).time()

    data["market_session"] = "after_market"

    data.loc[
        time < market_open,
        "market_session"
    ] = "pre_market"

    data.loc[
        (time >= market_open)
        & (time < market_close),
        "market_session"
    ] = "market_hours"

    return data


def assign_information_date(df):
    """
    Determine which trading date a news observation
    can be associated with without look-ahead bias.

    Pre-market news:
        Same trading date.

    Market-hours news:
        Same trading date for exploratory
        contemporaneous analysis.

    After-market news:
        Next calendar/trading date is handled
        later when merged with market data.
    """

    data = df.copy()

    data["information_date"] = (
        data["publication_date"]
    )

    after_market = (
        data["market_session"]
        == "after_market"
    )

    data.loc[
        after_market,
        "information_date"
    ] = (
        pd.to_datetime(
            data.loc[
                after_market,
                "publication_date"
            ]
        )
        + pd.Timedelta(days=1)
    ).dt.date

    return data


def prepare_temporal_news_data(df):
    """
    Complete temporal preprocessing pipeline.
    """

    data = prepare_news_timestamps(df)

    data = classify_market_session(data)

    data = assign_information_date(data)

    return data