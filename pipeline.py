from src.data.collector import (
    collect_news,
    append_news_data,
)

from src.data.process import process_news


def main():

    print("\n==============================")
    print("FINANCIAL NEWS PIPELINE")
    print("==============================\n")

    # --------------------------------
    # 1. Collect
    # --------------------------------

    print("1. Collecting news...")

    new_data = collect_news(
        max_articles=10
    )

    print(
        f"   Retrieved: {len(new_data)} articles"
    )

    # --------------------------------
    # 2. Store raw data
    # --------------------------------

    print("\n2. Updating raw dataset...")

    raw_data = append_news_data(
        new_data
    )

    print(
        f"   Total unique articles: "
        f"{len(raw_data)}"
    )

    # --------------------------------
    # 3. Process
    # --------------------------------

    print("\n3. Processing sentiment...")

    processed_data = process_news()

    print(
        f"   Processed articles: "
        f"{len(processed_data)}"
    )

    # --------------------------------
    # 4. Summary
    # --------------------------------

    print("\n4. Sentiment distribution:\n")

    print(
        processed_data[
            "sentiment"
        ].value_counts()
    )

    print(
        "\nPipeline completed successfully."
    )


if __name__ == "__main__":
    main()
