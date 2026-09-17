import pandas as pd

from src.sentiment import analyze_sentiment


def combine_article_text(row):
    """
    Combine headline and description for sentiment analysis.
    """

    title = str(row.get("title", "") or "").strip()
    description = str(row.get("description", "") or "").strip()

    if description:
        return f"{title}. {description}"

    return title


def add_sentiment_features(df):
    """
    Add VADER sentiment features to a news DataFrame.
    """

    df = df.copy()

    # Headline sentiment
    headline_results = df["title"].apply(analyze_sentiment)

    df["headline_sentiment_score"] = headline_results.apply(
        lambda x: x["score"]
    )

    df["headline_sentiment"] = headline_results.apply(
        lambda x: x["label"]
    )

    # Combined article text
    df["analysis_text"] = df.apply(
        combine_article_text,
        axis=1,
    )

    # Combined sentiment
    combined_results = df["analysis_text"].apply(
        analyze_sentiment
    )

    df["sentiment_score"] = combined_results.apply(
        lambda x: x["score"]
    )

    df["sentiment"] = combined_results.apply(
        lambda x: x["label"]
    )

    df["sentiment_positive"] = combined_results.apply(
        lambda x: x["positive"]
    )

    df["sentiment_negative"] = combined_results.apply(
        lambda x: x["negative"]
    )

    df["sentiment_neutral"] = combined_results.apply(
        lambda x: x["neutral"]
    )

    return df

