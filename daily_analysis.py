import pandas as pd

from src.analysis.daily_sentiment import (
    create_daily_sentiment,
)

from src.analysis.quality import (
    validate_sentiment_data,
)


INPUT_PATH = (
    "data/processed/news_sentiment.csv"
)

OUTPUT_PATH = (
    "data/processed/daily_sentiment.csv"
)


def main():

    print("\nLoading processed news...")

    df = pd.read_csv(INPUT_PATH)
    checks = validate_sentiment_data(df)

    print("\n=== DATA QUALITY ===\n")

    for key, value in checks.items():
        print(f"{key}: {value}")

    print(
        f"Articles loaded: {len(df)}"
    )

    daily = create_daily_sentiment(df)

    daily.to_csv(
        OUTPUT_PATH,
        index=False,
    )

    print(
        f"Days available: {len(daily)}"
    )

    print(
        f"\nSaved to: {OUTPUT_PATH}"
    )

    print("\n=== DAILY SENTIMENT ===\n")

    print(
        daily.to_string(index=False)
    )


if __name__ == "__main__":
    main()
