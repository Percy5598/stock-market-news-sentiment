import re
from difflib import SequenceMatcher

import pandas as pd


def normalize_title(
    title: str,
) -> str:
    """
    Normalize a headline for similarity comparison.
    """

    if pd.isna(title):
        return ""

    text = str(title).lower()

    text = re.sub(
        r"[^\w\s]",
        " ",
        text,
    )

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text.strip()


def title_similarity(
    title_a: str,
    title_b: str,
) -> float:
    """
    Calculate normalized title similarity.
    """

    return SequenceMatcher(
        None,
        normalize_title(title_a),
        normalize_title(title_b),
    ).ratio()


def add_duplicate_flags(
    df: pd.DataFrame,
) -> pd.DataFrame:

    data = df.copy()

    data["normalized_title"] = (
        data["title"]
        .apply(normalize_title)
    )

    data["exact_title_duplicate"] = (
        data["normalized_title"]
        .duplicated(
            keep=False
        )
    )

    if "url" in data.columns:

        data["url_duplicate"] = (
            data["url"]
            .duplicated(
                keep=False
            )
        )

    else:

        data["url_duplicate"] = False

    return data


def find_near_duplicate_titles(
    df: pd.DataFrame,
    threshold: float = 0.90,
) -> pd.DataFrame:
    """
    Find potentially syndicated or near-duplicate headlines.

    This is an audit tool rather than an automatic deletion rule.
    """

    data = df.reset_index(
        drop=True
    )

    titles = (
        data["title"]
        .fillna("")
        .astype(str)
        .tolist()
    )

    matches = []

    for i in range(
        len(titles)
    ):

        for j in range(
            i + 1,
            len(titles),
        ):

            similarity = title_similarity(
                titles[i],
                titles[j],
            )

            if similarity >= threshold:

                matches.append(
                    {
                        "index_a": i,
                        "index_b": j,
                        "similarity": similarity,
                        "title_a": titles[i],
                        "title_b": titles[j],
                    }
                )

    return pd.DataFrame(
        matches
    )