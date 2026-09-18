import pandas as pd

from src.analysis.temporal_alignment import (
    prepare_temporal_news_data,
)


INPUT_PATH = (
    "data/processed/news_sentiment.csv"
)


def main():

    df = pd.read_csv(
        INPUT_PATH
    )

    result = prepare_temporal_news_data(
        df
    )

    print(
        "\n=== TEMPORAL NEWS DATA ===\n"
    )

    print(
        result[
            [
                "published_at",
                "published_at_et",
                "market_session",
                "information_date",
            ]
        ]
        .head(20)
        .to_string(index=False)
    )

    print(
        "\n=== MARKET SESSION DISTRIBUTION ===\n"
    )

    print(
        result[
            "market_session"
        ].value_counts()
    )


if __name__ == "__main__":
    main()