from src.news_api import get_financial_news
from src.data.preprocessing import articles_to_dataframe
from src.data.storage import save_news_data
from src.nlp.sentiment_pipeline import add_sentiment_features


def main():

    print("\nFetching financial news...\n")

    articles = get_financial_news(max_articles=10)

    print(f"Articles retrieved: {len(articles)}")

    if not articles:
        print("No articles were retrieved.")
        return

    # -----------------------------
    # Data processing
    # -----------------------------

    df = articles_to_dataframe(articles)

    print(f"Articles after cleaning: {len(df)}")

    # -----------------------------
    # NLP
    # -----------------------------

    df = add_sentiment_features(df)

    # -----------------------------
    # Save dataset
    # -----------------------------

    output_path = save_news_data(df)

    print(f"\nDataset saved to: {output_path}")

    # -----------------------------
    # Summary
    # -----------------------------

    print("\n=== SENTIMENT SUMMARY ===\n")

    print(
        df["sentiment"]
        .value_counts()
        .to_string()
    )

    print("\nAverage sentiment score:")
    print(
        f"{df['sentiment_score'].mean():.3f}"
    )

    # -----------------------------
    # Article results
    # -----------------------------

    print("\n=== MARKET NEWS SENTIMENT ===\n")

    for _, row in df.iterrows():

        print(f"Headline: {row['title']}")
        print(f"Source: {row['source_name']}")
        print(f"Published: {row['published_at']}")
        print(
            f"Headline sentiment: "
            f"{row['headline_sentiment']}"
        )
        print(
            f"Combined sentiment: "
            f"{row['sentiment']}"
        )
        print(
            f"Score: "
            f"{row['sentiment_score']:.3f}"
        )
        print("-" * 70)


if __name__ == "__main__":
    main()