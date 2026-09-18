import pandas as pd


REQUIRED_COLUMNS = [
    "title",
    "description",
    "content",
    "url",
    "published_at",
    "source_name",
    "source_url",
    "fetched_at",
    "collection_query",
]


def articles_to_dataframe(
    articles: list[dict],
    collection_query: str | None = None,
) -> pd.DataFrame:
    """
    Convert raw API articles into a normalized DataFrame.
    """

    if not articles:

        return pd.DataFrame(
            columns=REQUIRED_COLUMNS
        )

    df = pd.DataFrame(articles)

    for column in REQUIRED_COLUMNS:

        if column not in df.columns:
            df[column] = None

    if collection_query is not None:

        df["collection_query"] = (
            collection_query
        )

    df = df[
        REQUIRED_COLUMNS
    ].copy()

    # Remove articles without titles.
    df = df.dropna(
        subset=["title"]
    )

    df["title"] = (
        df["title"]
        .astype(str)
        .str.strip()
    )

    df = df[
        df["title"] != ""
    ]

    # Normalize text fields.
    text_columns = [
        "title",
        "description",
        "content",
        "source_name",
    ]

    for column in text_columns:

        df[column] = (
            df[column]
            .fillna("")
            .astype(str)
            .str.replace(
                r"\s+",
                " ",
                regex=True,
            )
            .str.strip()
        )

    # Normalize URLs.
    df["url"] = (
        df["url"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    # Normalize timestamps.
    df["published_at"] = pd.to_datetime(
        df["published_at"],
        errors="coerce",
        utc=True,
    )

    df["fetched_at"] = pd.to_datetime(
        df["fetched_at"],
        errors="coerce",
        utc=True,
    )

    # Remove exact URL duplicates.
    with_url = df[
        df["url"] != ""
    ].drop_duplicates(
        subset=["url"],
        keep="first",
    )

    without_url = df[
        df["url"] == ""
    ].drop_duplicates(
        subset=["title"],
        keep="first",
    )

    df = pd.concat(
        [
            with_url,
            without_url,
        ],
        ignore_index=True,
    )

    return df.reset_index(
        drop=True
    )