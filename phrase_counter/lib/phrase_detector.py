"""Main functions for counting phrases."""
import pandas as pd
from .cleaner import cleaner, fetch_page_text
from sklearn.feature_extraction.text import CountVectorizer
from hashlib import sha256
from typing import Any


def phrase_counter(doc: str, doc_type: str = "text") -> Any:
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
    # ----------------- Counter Section -----------------
    # Initializing vector
    count_vector = CountVectorizer(ngram_range=(1, 5), encoding="utf-8")

    # Fit on text
    count_data = count_vector.fit_transform([cleaned_text])

    # ----------------- Dataframe creation -----------------
    phrase_df = pd.DataFrame(columns=["Bag", "Count"])
    phrase_df["Bag"] = count_vector.get_feature_names_out().tolist()
    phrase_df["Count"] = count_data.toarray()[0].tolist()

    # ----------------- Additional Metadata -----------------
    phrase_df["Phrase_hash"] = phrase_df.apply(
        lambda row: sha256(row["Bag"].encode()).hexdigest(),
        axis=1
    )
    phrase_df["Status"] = None

    json_result = phrase_df.to_dict(orient='records')  # Converting result to JSON

    return json_result
