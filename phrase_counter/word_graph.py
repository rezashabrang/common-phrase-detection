"""Creating word to word graph"""
from typing import Any

from hashlib import sha256

import pandas as pd

from phrase_counter.cleaner import cleaner


def generate_word_graph(doc: str) -> Any:
    """Main function for creating word to word graph"""
    cleaned_text = cleaner(doc)  # Cleaning

    words_list = []
    hashed_list = []
    from_list = []
    to_list = []

    # -------------------- Generating Graphs --------------------
    for text_part in cleaned_text.split("."):
        # Generating words
        words = text_part.strip().split(" ")

        # Hashing words
        hashed_words = [
            sha256(word.encode()).hexdigest() for word in words if word != ""
        ]
        # Creating words relation
        from_rel = hashed_words[: len(hashed_words) - 1]
        to_rel = hashed_words[1:]

        # Extending results
        words_list.extend(words)
        hashed_list.extend(hashed_words)
        from_list.extend(from_rel)
        to_list.extend(to_rel)

    # -------------------- Concating Results --------------------
    words_df = pd.DataFrame(zip(words_list, hashed_list), columns=["word", "word_hash"])
    words_df["count"] = 1

    rel_df = pd.DataFrame(zip(from_list, to_list), columns=["_from", "_to"])
    rel_df["count"] = 1

    # -------------------- Aggregating --------------------
    words_df = (
        words_df.groupby(["word", "word_hash"]).agg({"count": "sum"}).reset_index()
    )

    rel_df = rel_df.groupby(["_from", "_to"]).agg({"count": "sum"}).reset_index()

    return words_df, rel_df
