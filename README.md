# Stock Market News Sentiment

A small Python project that collects financial news using the GNews API and analyzes headline sentiment with VADER.

## Pipeline

```text
GNews API → News Headlines → VADER → Sentiment Score → Market Mood
```

## Tech Stack

* Python
* GNews API
* Pandas
* VADER
* Requests

## Run

```bash
pip install -r requirements.txt
python main.py
```

Create a `.env` file with:

```text
GNEWS_API_KEY=your_api_key
```

## Note

This project measures **financial-news sentiment**, not stock-price predictions or investment signals.
