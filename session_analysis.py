import pandas as pd

from src.analysis.market_sentiment import (
    align_news_to_trading_sessions,
)
from src.analysis.session_features import (
    build_session_features,
)
from src.analysis.temporal_alignment import (
    prepare_temporal_news_data,
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
        "=============================="
    )

    print(
        "\n1. Loading processed news..."
    )

    news = pd.read_csv(
        NEWS_PATH
    )

    if news.empty:

        raise ValueError(
            "Processed news dataset is empty."
        )

    print(
        f"   Articles: {len(news)}"
    )

    print(
        "\n2. Preparing publication timestamps..."
    )

    news = (
        prepare_temporal_news_data(
            news
        )
    )

    start = (
        news[
            "published_at_et"
        ]
        .min()
        .strftime(
            "%Y-%m-%d"
        )
    )

    end = (
        news[
            "published_at_et"
        ]
        .max()
        + pd.Timedelta(
            days=10
        )
    ).strftime(
        "%Y-%m-%d"
    )

    print(
        f"   Market period: "
        f"{start} -> {end}"
    )

    print(
        "\n3. Downloading market data..."
    )

    market = get_market_data(
        ticker="^GSPC",
        start=start,
        end=end,
    )

    print(
        f"   Trading sessions: "
        f"{len(market)}"
    )

    print(
        "\n4. Aligning news..."
    )

    aligned = (
        align_news_to_trading_sessions(
            news,
            market,
        )
    )

    print(
        f"   Aligned articles: "
        f"{len(aligned)}"
    )

    print(
        "\n5. Creating session features..."
    )

    session = (
        build_session_features(
            aligned
        )
    )

    session = (
        session
        .sort_values("date")
        .reset_index(
            drop=True
        )
    )

    output_path = (
        OUTPUT_PATH
    )

    session.to_csv(
        output_path,
        index=False,
    )

    print(
        "\n6. Dataset saved:"
    )

    print(
        f"   {output_path}"
    )

    print(
        "\nDataset shape:"
    )

    print(
        session.shape
    )

    print(
        "\nMissing values:"
    )

    print(
        session.isna()
        .sum()
        .to_string()
    )


if __name__ == "__main__":
    main()