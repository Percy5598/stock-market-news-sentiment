from datetime import datetime, timedelta

from src.data.collector import (
    append_news_data,
)
from src.data.preprocessing import (
    articles_to_dataframe,
)
from src.news_api import (
    GNewsAPIError,
    get_financial_news,
)


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

START_DATE = "2026-09-17"
END_DATE = "2026-09-17"

ARTICLES_PER_QUERY = 10

QUERIES = [
    "stock market",
    "Wall Street",
    '"Federal Reserve" OR inflation OR "interest rates"',
    '"S&P 500" OR "Treasury yields" OR "oil prices"',
]


# --------------------------------------------------
# COLLECTION
# --------------------------------------------------

def main():

    start = datetime.strptime(
        START_DATE,
        "%Y-%m-%d",
    )

    end = datetime.strptime(
        END_DATE,
        "%Y-%m-%d",
    )

    if end < start:

        raise ValueError(
            "END_DATE must be on or after START_DATE."
        )

    current = start

    total_retrieved = 0
    successful_requests = 0
    failed_requests = 0

    print(
        "\n=============================="
    )
    print(
        "HISTORICAL NEWS COLLECTION"
    )
    print(
        "=============================="
    )

    while current <= end:

        next_day = (
            current
            + timedelta(days=1)
        )

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
            f"{current:%Y-%m-%d}"
        )

        for query in QUERIES:

            print(
                f"  Query: {query}"
            )

            try:

                articles = (
                    get_financial_news(
                        query=query,
                        max_articles=(
                            ARTICLES_PER_QUERY
                        ),
                        from_date=from_date,
                        to_date=to_date,
                    )
                )

                df = (
                    articles_to_dataframe(
                        articles,
                        collection_query=query,
                    )
                )

                append_news_data(
                    df
                )

                successful_requests += 1
                total_retrieved += len(
                    df
                )

                print(
                    f"    Retrieved: "
                    f"{len(df)}"
                )

            except GNewsAPIError as error:

                failed_requests += 1

                print(
                    f"    ERROR: {error}"
                )

        current += timedelta(
            days=1
        )

    print(
        "\n=============================="
    )
    print(
        "COLLECTION COMPLETED"
    )
    print(
        "=============================="
    )

    print(
        f"Articles retrieved: "
        f"{total_retrieved}"
    )

    print(
        f"Successful requests: "
        f"{successful_requests}"
    )

    print(
        f"Failed requests: "
        f"{failed_requests}"
    )


if __name__ == "__main__":
    main()