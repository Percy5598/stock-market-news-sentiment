import pandas as pd

from src.data.market_data import (
    get_market_data,
)

from src.analysis.market_sentiment import (
    merge_sentiment_with_market,
)


SENTIMENT_PATH = (
    "data/processed/daily_sentiment.csv"
)

OUTPUT_PATH = (
    "data/processed/"
    "sentiment_market.csv"
)


def main():

    print("\nLoading daily sentiment...")

    sentiment = pd.read_csv(
        SENTIMENT_PATH
    )

    print(
        f"Sentiment observations: "
        f"{len(sentiment)}"
    )

    # Determine date range
    start = sentiment["date"].min()
    end = sentiment["date"].max()

    print(f"Sentiment period: {start} → {end}")

    print("\nDownloading market data...")

    market = get_market_data(
        ticker="^GSPC",
        start=start,
        end=end,
    )

    print(
        f"Market observations: "
        f"{len(market)}"
    )

    # Merge datasets
    merged = merge_sentiment_with_market(
        sentiment,
        market,
    )

    print(
        f"\nMatched trading days: "
        f"{len(merged)}"
    )

    merged.to_csv(
        OUTPUT_PATH,
        index=False,
    )

    print(
        f"\nSaved to: {OUTPUT_PATH}"
    )

    if not merged.empty:

        print(
            "\n=== SENTIMENT + MARKET ===\n"
        )

        print(
            merged[
                [
                    "date",
                    "article_count",
                    "mean_sentiment",
                    "return",
                    "next_day_return",
                ]
            ].to_string(
                index=False
            )
        )


if __name__ == "__main__":
    main()
