from src.data.collector import (
    append_news_data,
    collect_news,
)
from src.data.process import (
    process_news,
)


def main():

    print(
        "\n=============================="
    )
    print(
        "FINANCIAL NEWS PIPELINE"
    )
    print(
        "=============================="
    )

    query = input(
        "\nNews query [stock market]: "
    ).strip()

    if not query:
        query = "stock market"

    print(
        f"\n1. Collecting news..."
    )

    print(
        f"   Query: {query}"
    )

    new_data = collect_news(
        query=query,
        max_articles=10,
    )

    print(
        f"   Retrieved: "
        f"{len(new_data)} articles"
    )

    if new_data.empty:

        print(
            "\nNo articles returned."
        )

        return

    print(
        "\n2. Updating raw dataset..."
    )

    raw_data = append_news_data(
        new_data
    )

    print(
        f"   Total unique articles: "
        f"{len(raw_data)}"
    )

    print(
        "\n3. Processing sentiment..."
    )

    processed_data = process_news()

    print(
        f"   Processed articles: "
        f"{len(processed_data)}"
    )

    print(
        "\n4. Sentiment distribution:"
    )

    print(
        processed_data[
            "sentiment"
        ]
        .value_counts()
        .to_string()
    )

    print(
        "\nPipeline completed successfully."
    )


if __name__ == "__main__":
    main()