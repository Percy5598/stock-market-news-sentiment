from datetime import datetime, timedelta

from src.news_api import get_financial_news
from src.data.preprocessing import articles_to_dataframe
from src.data.collector import append_news_data


START_DATE = "2026-09-17"
END_DATE = "2026-09-17"

ARTICLES_PER_QUERY = 10

QUERIES = [
    "stock market",
    "S&P 500",
    "Wall Street",
    "Federal Reserve",
    "interest rates",
    "Treasury yields",
    "inflation",
    "US economy",
    "stock earnings",
    "corporate earnings",
    "oil prices",
]


def main():
    start = datetime.strptime(
        START_DATE,
        "%Y-%m-%d",
    )

    end = datetime.strptime(
        END_DATE,
        "%Y-%m-%d",
    )

    current = start

    total_retrieved = 0

    print("\n==============================")
    print("HISTORICAL NEWS COLLECTION")
    print("==============================\n")

    while current <= end:

        next_day = current + timedelta(days=1)

        from_date = (
            current.strftime(
                "%Y-%m-%dT00:00:00Z"
            )
        )

        to_date = (
            next_day.strftime(
                "%Y-%m-%dT00:00:00Z"
            )
        )

        print(
            f"\nDATE: "
            f"{current.strftime('%Y-%m-%d')}"
        )

        for query in QUERIES:

            print(
                f"  Query: {query}"
            )

            try:

                articles = get_financial_news(
                    query=query,
                    max_articles=ARTICLES_PER_QUERY,
                    from_date=from_date,
                    to_date=to_date,
                )

                df = articles_to_dataframe(
                    articles
                )

                if df.empty:

                    print(
                        "    Retrieved: 0"
                    )

                    continue

                df["collection_query"] = query

                append_news_data(df)

                total_retrieved += len(df)

                print(
                    f"    Retrieved: "
                    f"{len(df)}"
                )

            except Exception as error:

                print(
                    f"    ERROR: {error}"
                )

        current += timedelta(days=1)

    print("\n==============================")
    print("COLLECTION COMPLETED")
    print("==============================")

    print(
        f"\nArticles retrieved: "
        f"{total_retrieved}"
    )


if __name__ == "__main__":
    main()