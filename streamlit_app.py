import pandas as pd
import plotly.express as px
import streamlit as st

from src.data.market_data import get_market_data
from src.analysis.daily_sentiment import create_daily_sentiment
from src.analysis.market_sentiment import merge_sentiment_with_market


st.set_page_config(
    page_title="Financial News & Market Sentiment",
    page_icon="📈",
    layout="wide",
)


SENTIMENT_PATH = "data/processed/news_sentiment.csv"


# --------------------------------------------------
# Data loading
# --------------------------------------------------

@st.cache_data
def load_sentiment_data():

    try:
        return pd.read_csv(SENTIMENT_PATH)

    except FileNotFoundError:
        return pd.DataFrame()


@st.cache_data
def load_market_data(start, end):

    return get_market_data(
        ticker="^GSPC",
        start=start,
        end=end,
    )


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("📈 Financial News & Market Sentiment")

st.markdown(
    """
    **End-to-end financial NLP analytics pipeline**

    This dashboard explores the relationship between financial
    news sentiment and S&P 500 market dynamics.
    """
)

st.warning(
    """
    **Research note:** This is an exploratory analytics project.
    Correlation does not imply causation, and the results should
    not be interpreted as investment advice.
    """
)


# --------------------------------------------------
# Load sentiment data
# --------------------------------------------------

df = load_sentiment_data()

if df.empty:

    st.error(
        """
        No processed sentiment data was found.

        Run:

        `python pipeline.py`

        before launching the dashboard.
        """
    )

    st.stop()


# --------------------------------------------------
# Prepare data
# --------------------------------------------------

df["published_at"] = pd.to_datetime(
    df["published_at"],
    errors="coerce",
    utc=True,
)

df = df.dropna(
    subset=["published_at"]
)

daily = create_daily_sentiment(df)

daily["date"] = pd.to_datetime(
    daily["date"]
)


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

st.sidebar.header("Filters")

maximum_articles = max(
    1,
    int(daily["article_count"].max()),
)

minimum_articles = st.sidebar.slider(
    "Minimum articles per day",
    min_value=1,
    max_value=maximum_articles,
    value=1,
)

filtered_daily = daily[
    daily["article_count"] >= minimum_articles
].copy()


# --------------------------------------------------
# KPIs
# --------------------------------------------------

st.header("Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Articles",
    f"{len(df):,}",
)

col2.metric(
    "Days",
    f"{len(daily):,}",
)

col3.metric(
    "Average Sentiment",
    f"{df['sentiment_score'].mean():.3f}",
)

negative_share = (
    df["sentiment"]
    .eq("Negative")
    .mean()
)

col4.metric(
    "Negative Articles",
    f"{negative_share:.1%}",
)


# --------------------------------------------------
# Sentiment distribution
# --------------------------------------------------

st.header("Sentiment Distribution")

sentiment_counts = (
    df["sentiment"]
    .value_counts()
    .reset_index()
)

sentiment_counts.columns = [
    "sentiment",
    "count",
]

fig = px.bar(
    sentiment_counts,
    x="sentiment",
    y="count",
    title="Financial News Sentiment",
)

st.plotly_chart(
    fig,
    use_container_width=True,
)


# --------------------------------------------------
# Daily sentiment
# --------------------------------------------------

st.header("Daily Sentiment")

fig = px.line(
    filtered_daily,
    x="date",
    y="mean_sentiment",
    markers=True,
    title="Average Daily Sentiment",
)

fig.add_hline(
    y=0,
    line_dash="dash",
)

st.plotly_chart(
    fig,
    use_container_width=True,
)


# --------------------------------------------------
# News volume
# --------------------------------------------------

st.header("News Volume")

fig = px.bar(
    filtered_daily,
    x="date",
    y="article_count",
    title="Financial News Volume",
)

st.plotly_chart(
    fig,
    use_container_width=True,
)


# --------------------------------------------------
# Market analysis
# --------------------------------------------------

st.header("Sentiment vs. Market Returns")

start = (
    filtered_daily["date"]
    .min()
    .strftime("%Y-%m-%d")
)

end = (
    filtered_daily["date"]
    .max()
    .strftime("%Y-%m-%d")
)

try:

    market = load_market_data(
        start,
        end,
    )

    merged = merge_sentiment_with_market(
        filtered_daily,
        market,
    )

except Exception as error:

    st.error(
        f"Market data could not be loaded: {error}"
    )

    merged = pd.DataFrame()


if merged.empty:

    st.info(
        """
        There are currently no overlapping observations
        between the news and market datasets.
        """
    )

else:

    fig = px.scatter(
        merged,
        x="mean_sentiment",
        y="return",
        size="article_count",
        hover_data=[
            "date",
            "article_count",
        ],
        title="Daily News Sentiment vs. S&P 500 Return",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    if len(merged) >= 3:

        correlation = (
            merged[
                [
                    "mean_sentiment",
                    "return",
                ]
            ]
            .corr()
            .iloc[0, 1]
        )

        st.metric(
            "Pearson Correlation",
            f"{correlation:.3f}",
        )

    else:

        st.info(
            f"""
            Only {len(merged)} matched trading day(s) are available.
            At least 3 observations are required before displaying
            a correlation statistic.
            """
        )


# --------------------------------------------------
# Recent news
# --------------------------------------------------

st.header("Recent Financial News")

display_columns = [
    "published_at",
    "source_name",
    "title",
    "sentiment",
    "sentiment_score",
]

recent = (
    df[display_columns]
    .sort_values(
        "published_at",
        ascending=False,
    )
    .head(20)
)

st.dataframe(
    recent,
    use_container_width=True,
    hide_index=True,
)


# --------------------------------------------------
# Methodology
# --------------------------------------------------

with st.expander("Methodology"):

    st.markdown(
        """
        ### News data

        Financial news is collected using the GNews API.

        ### Sentiment analysis

        VADER is used as the initial sentiment-analysis baseline.

        Both headlines and article descriptions contribute to
        the combined sentiment score.

        ### Daily aggregation

        Article-level sentiment is aggregated into:

        - Mean sentiment
        - Median sentiment
        - Sentiment standard deviation
        - Positive article proportion
        - Negative article proportion
        - Neutral article proportion
        - Article volume

        ### Market data

        S&P 500 historical prices are retrieved using Yahoo Finance.

        Daily close-to-close returns are calculated from market prices.

        ### Limitations

        The analysis is observational.

        Correlation does not establish causality.

        Publication timing must also be considered carefully because
        news published after a market session cannot explain that
        session's return without introducing look-ahead bias.

        A sufficiently large historical dataset is required before
        statistical inference or predictive modelling is appropriate.
        """
    )