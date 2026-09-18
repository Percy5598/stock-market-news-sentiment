from src.sentiment import (
    analyze_sentiment,
)


def test_positive_sentiment():

    result = analyze_sentiment(
        "Stocks surged strongly after excellent earnings."
    )

    assert result["label"] == "Positive"
    assert result["score"] > 0


def test_negative_sentiment():

    result = analyze_sentiment(
        "Stocks collapsed after disappointing earnings."
    )

    assert result["label"] == "Negative"
    assert result["score"] < 0


def test_empty_text():

    result = analyze_sentiment("")

    assert result["label"] == "Neutral"
    assert result["score"] == 0.0