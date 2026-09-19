# Financial News Sentiment and Market Dynamics

Demo: https://stock-market-news-sentiment.streamlit.app/

An end-to-end NLP and financial analytics project examining the relationship between financial-news sentiment and US equity-market dynamics.

## Research question

How is the sentiment of financial news associated with subsequent S&P 500 market returns after accounting for publication timing and trading-session structure?

## Project architecture

News API
↓
Data collection
↓
Preprocessing
↓
Deduplication
↓
VADER sentiment
↓
Publication-time classification
↓
Trading-session alignment
↓
S&P 500 market data
↓
Session-level feature engineering
↓
Exploratory analysis
↓
Streamlit dashboard

## Technologies

- Python
- Pandas
- VADER
- GNews API
- yfinance
- Plotly
- Streamlit
- pytest

## Project structure

```text
stock-market-news-sentiment/
│
├── streamlit_app.py
├── pipeline.py
├── historical_collection.py
├── session_analysis.py
│
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
│
├── src/
│   ├── news_api.py
│   ├── sentiment.py
│   │
│   ├── data/
│   │   ├── collector.py
│   │   ├── preprocessing.py
│   │   ├── process.py
│   │   ├── market_data.py
│   │   └── deduplication.py
│   │
│   ├── nlp/
│   │   └── sentiment_pipeline.py
│   │
│   └── analysis/
│       ├── daily_sentiment.py
│       ├── temporal_alignment.py
│       ├── market_sentiment.py
│       └── session_features.py
│
├── data/
│   ├── raw/
│   └── processed/
│
└── tests/
    ├── test_sentiment.py
    ├── test_preprocessing.py
    └── test_temporal_alignment.py