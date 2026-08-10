import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GNEWS_API_KEY")

URL = "https://gnews.io/api/v4/search"


def get_financial_news():

    params = {
        "q": "stock market OR stocks OR Wall Street",
        "lang": "en",
        "country": "us",
        "max": 10,
        "apikey": API_KEY,
    }

    response = requests.get(
        URL,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    return data["articles"]