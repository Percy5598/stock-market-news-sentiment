from src.news_api import get_financial_news
from src.sentiment import analyze_sentiment


articles = get_financial_news()

results = []

for article in articles:

    title = article["title"]

    sentiment = analyze_sentiment(title)

    results.append({
        "title": title,
        "sentiment_score": sentiment["score"],
        "sentiment": sentiment["label"],
    })


print("\n=== MARKET NEWS SENTIMENT ===\n")

for result in results:

    print(f"Headline: {result['title']}")
    print(f"Sentiment: {result['sentiment']}")
    print(f"Score: {result['sentiment_score']:.3f}")
    print("-" * 60)