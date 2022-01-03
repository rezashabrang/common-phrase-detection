from pymongo import MongoClient
from pymongo.results import InsertManyResult, UpdateResult
from urllib import parse
import os
from typing import Union

from phrase_counter.lib.phrase_detector import phrase_counter


def mongo_connection() -> MongoClient:
    """Connecting to mongo."""

    username = parse.quote_plus("root")
    password = parse.quote_plus("rootpass")
    host = os.getenv("MONGO_HOST")
    port = os.getenv("MONGO_PORT")

    mongo_client = MongoClient(
        f"mongodb://{username}:{password}@{host}:{port}"
    )

    return mongo_client


def integrate_phrase_data(
    phrase_res: list
) -> Union[InsertManyResult, UpdateResult]:
    """Inserting or updating phrase data in mongo collection.
    """

    # Switching to collection
    client = mongo_connection()
    phrasedb = client["phrasedb"]  # Phrase collection
    phrase_col = phrasedb["common_phrase"]  # Phrase collection

    # Initializing bulk insertion list
    values_to_be_inserted = []

    # Initializing res param for checking the update or insertion
    res = None

    for item in phrase_res:
        query = {"Phrase_hash": item["Phrase_hash"]}

        # If hash already exists update the count field.
        query_res = phrase_col.find(query)
        if list(query_res):
            update_query = {"$inc": {"Count": item["Count"]}}
            res = phrase_col.update_one(query, update_query)

        # If it is not already in database then save it for later bulk insertion
        else:
            values_to_be_inserted.append(item)

    # if value to be inserted list is not empty then bulk insert the results.
    if values_to_be_inserted:
        res = phrase_col.insert_many(values_to_be_inserted)

    return res
