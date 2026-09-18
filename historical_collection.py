from datetime import datetime, timedelta

from src.news_api import get_financial_news
from src.data.preprocessing import articles_to_dataframe
from src.data.collector import append_news_data


START_DATE = "2026-08-18"
END_DATE = "2026-09-17"

ARTICLES_PER_DAY = 10


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

    total_collected = 0

    print("\n==============================")
    print("HISTORICAL NEWS COLLECTION")
    print("==============================\n")

    while current <= end:

        next_day = current + timedelta(
            days=1
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
            f"Collecting {current.strftime('%Y-%m-%d')}..."
        )

        try:

            articles = get_financial_news(
                max_articles=ARTICLES_PER_DAY,
                from_date=from_date,
                to_date=to_date,
            )

            df = articles_to_dataframe(
                articles
            )

            if not df.empty:

                append_news_data(df)

                total_collected += len(df)

                print(
                    f"  Retrieved: {len(df)}"
                )

            else:

                print(
                    "  No articles found."
                )

        except Exception as error:

            print(
                f"  ERROR: {error}"
            )

        current = next_day

    print(
        "\nCollection completed."
    )

    print(
        f"Articles retrieved across requests: "
        f"{total_collected}"
    )


if __name__ == "__main__":
    main()