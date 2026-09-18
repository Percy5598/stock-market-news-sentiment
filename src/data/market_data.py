import pandas as pd
import yfinance as yf


def get_market_data(
    ticker="^GSPC",
    start=None,
    end=None,
):
    """
    Download historical market data and calculate
    trading-session returns.
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

    if isinstance(
        data.columns,
        pd.MultiIndex,
    ):
        data.columns = (
            data.columns
            .get_level_values(0)
        )

    data = data.reset_index()

    data.columns = [
        str(column).lower()
        for column in data.columns
    ]

    data["date"] = pd.to_datetime(
        data["date"],
        errors="coerce",
    )

    data = data.dropna(
        subset=["date"]
    )

    data = data.sort_values(
        "date"
    )

    # Close-to-close return
    data["return"] = (
        data["close"]
        .pct_change()
    )

    # Return during the next actual trading session
    data["next_trading_day_return"] = (
        data["return"]
        .shift(-1)
    )

    # Five-trading-session forward return
    data["five_trading_day_forward_return"] = (
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
            "next_trading_day_return",
            "five_trading_day_forward_return",
        ]
    ]