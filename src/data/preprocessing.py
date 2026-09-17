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
]


def articles_to_dataframe(articles):
    """
    Convert article dictionaries into a cleaned DataFrame.
    """

    if not articles:
        return pd.DataFrame(columns=REQUIRED_COLUMNS)

    df = pd.DataFrame(articles)

    for column in REQUIRED_COLUMNS:
        if column not in df.columns:
            df[column] = None

    df = df[REQUIRED_COLUMNS].copy()

    # Remove articles without titles
    df = df.dropna(subset=["title"])

    # Remove duplicate URLs
    df = df.drop_duplicates(subset=["url"])

    # Clean whitespace
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
            .str.replace(r"\s+", " ", regex=True)
            .str.strip()
        )

    # Convert publication timestamp
    df["published_at"] = pd.to_datetime(
        df["published_at"],
        errors="coerce",
        utc=True,
    )

    # Convert fetch timestamp
    df["fetched_at"] = pd.to_datetime(
        df["fetched_at"],
        errors="coerce",
        utc=True,
    )

    return df.reset_index(drop=True)
