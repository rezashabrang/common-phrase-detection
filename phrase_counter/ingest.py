"""Main functions for counting phrases."""
from typing import Any, Optional

from hashlib import sha256
from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

from phrase_counter.cleaner import cleaner, fetch_page_text

# ---------------------- Getting stop words list ----------------------
STOP_PATH = f"{Path(__file__).parent}/static/stop-words.txt"
with open(STOP_PATH, "r", encoding="utf-8") as stop_file:
    STOP_LIST = stop_file.readlines()

# Removing newlines
STOP_LIST = list(map(str.strip, STOP_LIST))


def ingest_doc(doc: str, doc_type: str = "text") -> Any:
    """Counting phrases in the document.

    Args:
        doc: Document to be processed.
        doc_type: URL, TEXT, or HTML.

    Returns:
        Dataframe with counts for each word.

    Raises:
        Exception: If unkown value is given for doc_type.
    """
    # ---------------- Fetching the page text ----------------
    # Fetching a page from URL
    if doc_type == "URL":
        dirty_text = fetch_page_text(url=doc)

    # Processing HTML
    elif doc_type == "HTML":
        dirty_text = fetch_page_text(webpage=doc)

    # Raw text
    elif doc_type == "TEXT":
        dirty_text = doc

    else:
        raise Exception("Unknown value for doc_type argument.")

    cleaned_text = cleaner(dirty_text)

    # ----------------- Initialization -----------------
    phrase_df = pd.DataFrame(columns=["bag", "count"])

    # ----------------- Splitting -----------------
    for text_part in cleaned_text.split("."):

        # ----------------- Counter Section -----------------
        # Initializing vector
        count_vector = CountVectorizer(ngram_range=(1, 5), encoding="utf-8")
        try:
            # Fit on text
            count_data = count_vector.fit_transform([text_part])
        except ValueError:
            continue

        # ----------------- Dataframe creation -----------------
        temp_df = pd.DataFrame(columns=["bag", "count"])
        temp_df["bag"] = count_vector.get_feature_names_out().tolist()
        temp_df["count"] = count_data.toarray()[0].tolist()

        # Concating results
        phrase_df = pd.concat([phrase_df, temp_df])

    # Creating phrase hash
    phrase_df["_key"] = phrase_df.apply(
        lambda row: sha256(row["bag"].encode()).hexdigest(), axis=1
    )

    # Aggregating for removing duplicate values (rows with same hash or phrase)
    phrase_df = phrase_df.groupby(["bag", "_key"]).agg({"count": "sum"}).reset_index()

    # Changing status to suggested stop for phrases that conatin stop words
    phrase_df["status"] = phrase_df.apply(
        lambda row: stop_word_detector(row["bag"]), axis=1
    )
    # Counting number of words in each bag
    phrase_df["length"] = phrase_df.apply(
        lambda row: len(str(row["bag"]).split()), axis=1
    )
    return phrase_df


def stop_word_detector(phrase: str) -> Optional[str]:
    """Find stop phrases based on existing list of stop words.

    Args:
        phrase: text of the phrase.

    Returns:
        status if stop words are in phrase.
    """
    # If there is any stop word in the phrase then it maybe a stop phrase
    if any(stop_word in phrase.split() for stop_word in STOP_LIST):
        return "suggested-stop"

    return None
