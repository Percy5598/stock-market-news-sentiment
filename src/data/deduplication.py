import re

import pandas as pd
from difflib import SequenceMatcher


def normalize_title(title):
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
    ).strip()

    return text


def title_similarity(title_a, title_b):
    return SequenceMatcher(
        None,
        normalize_title(title_a),
        normalize_title(title_b),
    ).ratio()


def add_duplicate_flags(df):
    data = df.copy()

    data["normalized_title"] = (
        data["title"].apply(normalize_title)
    )

    data["exact_title_duplicate"] = (
        data["normalized_title"]
        .duplicated(keep=False)
    )

    data["url_duplicate"] = (
        data["url"].duplicated(keep=False)
    )

    return data


def find_near_duplicate_titles(
    df,
    threshold=0.90,
):
    data = df.copy()

    titles = (
        data["title"]
        .fillna("")
        .astype(str)
        .tolist()
    )

    matches = []

    for i in range(len(titles)):
        for j in range(i + 1, len(titles)):
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

    return pd.DataFrame(matches)