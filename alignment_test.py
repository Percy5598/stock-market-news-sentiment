import pandas as pd

from src.analysis.temporal_alignment import (
    prepare_temporal_news_data,
)

from src.analysis.market_sentiment import (
    align_news_to_trading_sessions,
)

from src.data.market_data import (
    get_market_data,
)


NEWS_PATH = "data/processed/news_sentiment.csv"


def main():

    print("\nLoading news data...")

    news = pd.read_csv(
        NEWS_PATH
    )

    news = prepare_temporal_news_data(
        news
    )

    print(
        f"News articles: {len(news)}"
    )

    start = (
        pd.to_datetime(
            news["published_at_et"]
        )
        .min()
        .strftime("%Y-%m-%d")
    )

    end = (
        pd.to_datetime(
            news["published_at_et"]
        ).max()
        + pd.Timedelta(days=10)
    ).strftime("%Y-%m-%d")

    print(
        f"Market period: {start} → {end}"
    )

    market = get_market_data(
        ticker="^GSPC",
        start=start,
        end=end,
    )

    print(
        f"Trading sessions: {len(market)}"
    )

    aligned = align_news_to_trading_sessions(
        news,
        market,
    )

    print(
        f"Aligned observations: {len(aligned)}"
    )

    print(
        "\n=== TEMPORAL ALIGNMENT ===\n"
    )

    print(
        aligned[
            [
                "published_at_et",
                "market_session",
                "date",
                "return",
                "next_trading_day_return",
            ]
        ]
        .head(30)
        .to_string(index=False)
    )

    print(
        "\n=== SESSION DISTRIBUTION ===\n"
    )

    print(
        aligned[
            "market_session"
        ].value_counts()
    )


if __name__ == "__main__":
    main()