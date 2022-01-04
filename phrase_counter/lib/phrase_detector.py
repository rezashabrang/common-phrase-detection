"""Main functions for counting phrases."""
import pandas as pd
from .cleaner import cleaner, fetch_page_text
from sklearn.feature_extraction.text import CountVectorizer
from hashlib import sha256


def phrase_counter(doc: str, doc_type: str = "text") -> pd.DataFrame:
    """Counting phrases in the document.

    Args:
        doc: Document to be processed.
        doc_type: Either a url or text.

    Returns:
        Dataframe with counts for each word.

    Raises:
        Exception: If unkown value is given for doc_type.
    """
    # ---------------- Fetching the page text ----------------
    if doc_type == "url":
        dirty_text = fetch_page_text(url=doc)
    elif doc_type == "text":
        dirty_text = fetch_page_text(webpage=doc)
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
