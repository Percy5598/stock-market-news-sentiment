from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


SESSION_PATH = Path(
    "data/processed/session_features.csv"
)

NEWS_PATH = Path(
    "data/processed/news_sentiment.csv"
)


# --------------------------------------------------
# PAGE
# --------------------------------------------------

st.set_page_config(
    page_title=(
        "Financial News & "
        "Market Dynamics"
    ),
    page_icon="📈",
    layout="wide",
)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title(
    "Financial News Sentiment "
    "& Market Dynamics"
)

st.caption(
    "An exploratory NLP and financial "
    "market analytics dashboard."
)


# --------------------------------------------------
# DATA
# --------------------------------------------------

if not SESSION_PATH.exists():

    st.warning(
        "Session-level data is not available."
    )

    st.markdown(
        """
        Run the pipeline first:

        ```bash
        python historical_collection.py
        python -c "from src.data.process import process_news; process_news()"
        python session_analysis.py
        ```
        """
    )

    st.stop()


session = pd.read_csv(
    SESSION_PATH
)

session["date"] = pd.to_datetime(
    session["date"],
    errors="coerce",
)

session = (
    session
    .dropna(subset=["date"])
    .sort_values("date")
)


if NEWS_PATH.exists():

    news = pd.read_csv(
        NEWS_PATH
    )

else:

    news = pd.DataFrame()


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.header(
    "Dashboard filters"
)

min_date = (
    session["date"]
    .min()
    .date()
)

max_date = (
    session["date"]
    .max()
    .date()
)

date_range = st.sidebar.date_input(
    "Date range",
    value=(
        min_date,
        max_date,
    ),
    min_value=min_date,
    max_value=max_date,
)


if (
    isinstance(
        date_range,
        tuple,
    )
    and len(date_range) == 2
):

    start_date, end_date = (
        date_range
    )

    filtered = session[
        (
            session["date"].dt.date
            >= start_date
        )
        & (
            session["date"].dt.date
            <= end_date
        )
    ]

else:

    filtered = session.copy()


# --------------------------------------------------
# KPI
# --------------------------------------------------

st.subheader(
    "Overview"
)

col1, col2, col3, col4 = (
    st.columns(4)
)


if filtered.empty:

    article_count = 0
    mean_sentiment = None
    mean_return = None

else:

    article_count = int(
        filtered[
            "article_count"
        ].sum()
    )

    mean_sentiment = (
        filtered[
            "mean_sentiment"
        ].mean()
    )

    mean_return = (
        filtered[
            "market_return"
        ].mean()
    )


col1.metric(
    "Trading sessions",
    len(filtered),
)

col2.metric(
    "Articles",
    article_count,
)

col3.metric(
    "Mean sentiment",
    (
        f"{mean_sentiment:.3f}"
        if mean_sentiment is not None
        else "N/A"
    ),
)

col4.metric(
    "Mean S&P 500 return",
    (
        f"{mean_return:.2%}"
        if mean_return is not None
        else "N/A"
    ),
)


# --------------------------------------------------
# SENTIMENT CHART
# --------------------------------------------------

st.subheader(
    "News sentiment over time"
)

if not filtered.empty:

    figure = px.line(
        filtered,
        x="date",
        y="mean_sentiment",
        markers=True,
        title=(
            "Mean Session-Level "
            "News Sentiment"
        ),
    )

    figure.add_hline(
        y=0,
        line_dash="dash",
    )

    figure.update_layout(
        xaxis_title="Date",
        yaxis_title="Mean sentiment",
    )

    st.plotly_chart(
        figure,
        use_container_width=True,
    )

else:

    st.info(
        "No data in the selected period."
    )


# --------------------------------------------------
# RETURN VS SENTIMENT
# --------------------------------------------------

st.subheader(
    "Sentiment vs. S&P 500 return"
)

if not filtered.empty:

    scatter = px.scatter(
        filtered,
        x="mean_sentiment",
        y="market_return",
        size="article_count",
        hover_data=[
            "date",
            "article_count",
        ],
        trendline="ols",
        title=(
            "Daily News Sentiment "
            "vs. Same-Session Return"
        ),
    )

    scatter.update_layout(
        xaxis_title="Mean sentiment",
        yaxis_title="Market return",
    )

    st.plotly_chart(
        scatter,
        use_container_width=True,
    )


# --------------------------------------------------
# ARTICLE COVERAGE
# --------------------------------------------------

st.subheader(
    "News coverage"
)

if not filtered.empty:

    coverage = px.bar(
        filtered,
        x="date",
        y="article_count",
        title=(
            "Articles Assigned "
            "to Trading Sessions"
        ),
    )

    coverage.update_layout(
        xaxis_title="Date",
        yaxis_title="Article count",
    )

    st.plotly_chart(
        coverage,
        use_container_width=True,
    )


# --------------------------------------------------
# SENTIMENT DISTRIBUTION
# --------------------------------------------------

st.subheader(
    "Sentiment composition"
)

if not filtered.empty:

    sentiment_columns = [
        "positive_articles",
        "negative_articles",
        "neutral_articles",
    ]

    available_columns = [
        column
        for column in sentiment_columns
        if column in filtered.columns
    ]

    distribution = (
        filtered[
            available_columns
        ]
        .sum()
        .reset_index()
    )

    distribution.columns = [
        "sentiment",
        "articles",
    ]

    distribution[
        "sentiment"
    ] = distribution[
        "sentiment"
    ].str.replace(
        "_articles",
        "",
    )

    distribution[
        "sentiment"
    ] = distribution[
        "sentiment"
    ].str.title()

    figure = px.bar(
        distribution,
        x="sentiment",
        y="articles",
        title=(
            "Positive, Negative "
            "and Neutral Articles"
        ),
    )

    st.plotly_chart(
        figure,
        use_container_width=True,
    )


# --------------------------------------------------
# SESSION DATA
# --------------------------------------------------

st.subheader(
    "Session-level dataset"
)

st.dataframe(
    filtered,
    use_container_width=True,
)


# --------------------------------------------------
# NEWS TABLE
# --------------------------------------------------

if not news.empty:

    st.subheader(
        "Recent news"
    )

    display_columns = [
        column
        for column in [
            "published_at",
            "source_name",
            "title",
            "sentiment",
            "sentiment_score",
        ]
        if column in news.columns
    ]

    recent_news = (
        news.sort_values(
            "published_at",
            ascending=False,
        )
        .head(50)
    )

    st.dataframe(
        recent_news[
            display_columns
        ],
        use_container_width=True,
    )


# --------------------------------------------------
# METHODOLOGICAL NOTE
# --------------------------------------------------

st.divider()

st.subheader(
    "Interpretation"
)

st.info(
    """
    This dashboard is descriptive.

    A relationship between news sentiment and
    market returns does not by itself establish
    causality or predictive power.

    Publication timing is explicitly considered,
    but the current daily market data do not provide
    intraday event windows. Therefore, return-target
    definitions must be carefully specified before
    making predictive or causal claims.
    """
)