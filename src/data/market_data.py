import pandas as pd
import yfinance as yf


def get_market_data(
    ticker="^GSPC",
    start=None,
    end=None,
):
    """
    Download historical market data.

    Parameters
    ----------
    ticker : str
        Yahoo Finance ticker symbol.

    start : str
        Start date, e.g. "2026-01-01".

    end : str
        End date.

    Returns
    -------
    pandas.DataFrame
        Historical market prices and returns.
    """

    data = yf.download(
        ticker,
        start=start,
        end=end,
        auto_adjust=False,
        progress=False,
    )

    if data.empty:
        raise ValueError(
            f"No market data returned for {ticker}."
        )

    # yfinance can return MultiIndex columns
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    data = data.reset_index()

    # Standardize column names
    data.columns = [
        str(column).lower()
        for column in data.columns
    ]

    data["date"] = pd.to_datetime(
        data["date"],
        errors="coerce",
    ).dt.date

    # Daily close-to-close return
    data["return"] = (
        data["close"]
        .pct_change()
    )

    # Next trading-day return
    data["next_day_return"] = (
        data["return"]
        .shift(-1)
    )

    # Five-trading-day forward return
    data["five_day_forward_return"] = (
        data["close"]
        .shift(-5)
        / data["close"]
        - 1
    )

    return data[
        [
            "date",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "return",
            "next_day_return",
            "five_day_forward_return",
        ]
    ]

