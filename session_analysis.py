import pandas as pd

from src.analysis.temporal_alignment import (
    prepare_temporal_news_data,
)

from src.analysis.market_sentiment import (
    align_news_to_trading_sessions,
)

from src.analysis.session_features import (
    create_session_features,
)

from src.data.market_data import (
    get_market_data,
)


NEWS_PATH = (
    "data/processed/news_sentiment.csv"
)

OUTPUT_PATH = (
    "data/processed/session_features.csv"
)


def main():

    print(
        "\n=============================="
    )
    print(
        "TRADING SESSION ANALYSIS"
    )
    print(
        "==============================\n"
    )

    # --------------------------------------------------
    # Load news
    # --------------------------------------------------

    print("1. Loading news...")

    news = pd.read_csv(
        NEWS_PATH
    )

    print(
        f"   Articles: {len(news)}"
    )

    # --------------------------------------------------
    # Prepare timestamps
    # --------------------------------------------------

    print(
        "\n2. Preparing temporal information..."
    )

    news = prepare_temporal_news_data(
        news
    )

    # --------------------------------------------------
    # Determine market period
    # --------------------------------------------------

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
        f"   Market period: {start} → {end}"
    )

    # --------------------------------------------------
    # Market data
    # --------------------------------------------------

    print(
        "\n3. Downloading market data..."
    )

    market = get_market_data(
        ticker="^GSPC",
        start=start,
        end=end,
    )

    print(
        f"   Trading sessions: {len(market)}"
    )

    # --------------------------------------------------
    # Align news
    # --------------------------------------------------

    print(
        "\n4. Aligning news with trading sessions..."
    )

    aligned = align_news_to_trading_sessions(
        news,
        market,
    )

    print(
        f"   Aligned articles: {len(aligned)}"
    )

    # --------------------------------------------------
    # Aggregate
    # --------------------------------------------------

    print(
        "\n5. Creating session-level features..."
    )

    session = create_session_features(
        aligned
    )

    # --------------------------------------------------
    # Sort
    # --------------------------------------------------

    session = session.sort_values(
        "date"
    ).reset_index(
        drop=True
    )

    # --------------------------------------------------
    # Save
    # --------------------------------------------------

    session.to_csv(
        OUTPUT_PATH,
        index=False,
    )

    print(
        f"\n6. Saved dataset:"
    )

    print(
        f"   {OUTPUT_PATH}"
    )

    # --------------------------------------------------
    # Summary
    # --------------------------------------------------

    print(
        "\n=== SESSION DATASET ===\n"
    )

    print(
        session.to_string(
            index=False
        )
    )

    print(
        "\n=== DATASET SHAPE ==="
    )

    print(
        session.shape
    )

    print(
        "\n=== MISSING VALUES ==="
    )

    print(
        session.isna()
        .sum()
        .to_string()
    )


if __name__ == "__main__":
    main()
