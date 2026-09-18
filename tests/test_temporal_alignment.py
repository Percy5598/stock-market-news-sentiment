import pandas as pd

from src.analysis.temporal_alignment import (
    classify_market_session,
)


def test_pre_market():

    df = pd.DataFrame(
        {
            "published_at_et": pd.to_datetime(
                [
                    "2026-09-17 08:30:00"
                ]
            ).tz_localize(
                "America/New_York"
            )
        }
    )

    result = classify_market_session(
        df
    )

    assert (
        result.iloc[0][
            "market_session"
        ]
        == "pre_market"
    )


def test_market_hours():

    df = pd.DataFrame(
        {
            "published_at_et": pd.to_datetime(
                [
                    "2026-09-17 12:00:00"
                ]
            ).tz_localize(
                "America/New_York"
            )
        }
    )

    result = classify_market_session(
        df
    )

    assert (
        result.iloc[0][
            "market_session"
        ]
        == "market_hours"
    )


def test_after_market():

    df = pd.DataFrame(
        {
            "published_at_et": pd.to_datetime(
                [
                    "2026-09-17 17:00:00"
                ]
            ).tz_localize(
                "America/New_York"
            )
        }
    )

    result = classify_market_session(
        df
    )

    assert (
        result.iloc[0][
            "market_session"
        ]
        == "after_market"
    )


def test_weekend():

    df = pd.DataFrame(
        {
            "published_at_et": pd.to_datetime(
                [
                    "2026-09-19 12:00:00"
                ]
            ).tz_localize(
                "America/New_York"
            )
        }
    )

    result = classify_market_session(
        df
    )

    assert (
        result.iloc[0][
            "market_session"
        ]
        == "non_trading_day"
    )