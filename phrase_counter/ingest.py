"""Main functions for counting phrases."""
from typing import Any

from hashlib import sha256

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

from phrase_counter.cleaner import cleaner, fetch_page_text

# STOP_PATH = f"{Path(__file__).parent}/static/stop-words.txt"
# with open(STOP_PATH, "r", encoding="utf-8") as stop_file:
#     STOP_LIST = stop_file.readlines()

# # Removing newlines
# STOP_LIST = list(map(str.strip, STOP_LIST))


def ingest_doc(
    doc: str,
    doc_type: str = "TEXT",
    ngram_range=(1, 5),
    remove_stop_regex=None,
    remove_highlight_regex=None
) -> Any:
    """Counting phrases in the document.

    Args:
        doc: Document to be processed.
        doc_type: URL, TEXT, or HTML.
        tag_stop: Whether to change status of stop words or not

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

    cleaned_text = cleaner(
        dirty_text,
        remove_stop_regex=remove_stop_regex,
        remove_highlight_regex=remove_highlight_regex
    )

    bags_list = []
    counts_list = []
    # ----------------- Splitting -----------------
    for text_part in cleaned_text.split("."):
        # ----------------- Counter Section -----------------
        # Initializing vector
        count_vector = CountVectorizer(
            ngram_range=(ngram_range[0], ngram_range[1]), encoding="utf-8"
        )
        try:
            # Fit on text
            count_data = count_vector.fit_transform([text_part])
        except ValueError:
            continue
        # ----------------- Extending data -----------------
        bags_list.extend(count_vector.get_feature_names_out().tolist())
        counts_list.extend(count_data.toarray()[0].tolist())

    # Concating results
    phrase_df = pd.DataFrame(zip(bags_list, counts_list), columns=["bag", "count"])

    # Aggregating for removing duplicate values (rows with same hash or phrase)
    phrase_df = phrase_df.groupby(["bag"]).agg({"count": "sum"}).reset_index()

    # Creating phrase hash
    phrase_df["_key"] = [sha256(bag.encode()).hexdigest() for bag in phrase_df["bag"]]

    # Counting number of words in each bag
    phrase_df["length"] = [len(str(bag).split()) for bag in phrase_df["bag"]]

    return phrase_df
