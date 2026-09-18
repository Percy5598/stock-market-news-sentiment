from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


analyzer = SentimentIntensityAnalyzer()


def analyze_sentiment(text: str) -> dict:
    """
    Calculate VADER sentiment features.

    Returns:
        score: VADER compound score in [-1, 1]
        label: Positive, Negative, or Neutral
        positive: positive probability
        negative: negative probability
        neutral: neutral probability
    """

    if not text or not str(text).strip():
        return {
            "score": 0.0,
            "label": "Neutral",
            "positive": 0.0,
            "negative": 0.0,
            "neutral": 1.0,
        }

    scores = analyzer.polarity_scores(
        str(text)
    )

    compound = scores["compound"]

    if compound >= 0.05:
        label = "Positive"
    elif compound <= -0.05:
        label = "Negative"
    else:
        label = "Neutral"

    return {
        "score": compound,
        "label": label,
        "positive": scores["pos"],
        "negative": scores["neg"],
        "neutral": scores["neu"],
    }
