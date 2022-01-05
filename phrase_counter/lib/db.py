"""Mongo Database Configs."""
from pymongo import MongoClient
from urllib import parse
import os
from typing import List, Dict


def mongo_connection() -> MongoClient:
    """Connecting to mongo."""
    username = parse.quote_plus(str(os.getenv("MONGO_USERNAME")))
    password = parse.quote_plus(str(os.getenv("MONGO_PASSWORD")))
    host = os.getenv("MONGO_HOST")
    port = os.getenv("MONGO_PORT")
    database = os.getenv("MONGO_PHRASE_DB")
    mongo_client = MongoClient(
        f"mongodb://{username}:{password}@{host}:{port}/?authsource={database}"
    )

    return mongo_client


def integrate_phrase_data(
    phrase_res: List[Dict[str, object]]
) -> None:
    """Inserting or updating phrase data in mongo collection.

    Args:
        phrase_res: JSON result of counted phrases.
    """
    # Switching to collection
    client = mongo_connection()
    phrasedb = client[os.getenv("MONGO_PHRASE_DB")]  # Phrase database
    phrase_col = phrasedb[os.getenv("MONGO_PHRASE_COL")]  # Phrase collection
    # Initializing bulk insertion list
    values_to_be_inserted = []

    for item in phrase_res:
        query = {"Phrase_hash": item["Phrase_hash"]}

        # If hash already exists update the count field.
        query_res = phrase_col.find(query)
        if list(query_res):
            update_query = {"$inc": {"Count": item["Count"]}}
            phrase_col.update_one(query, update_query)

        # If it is not already in database then save it for later bulk insertion
        else:
            values_to_be_inserted.append(item)

    # if value to be inserted list is not empty then bulk insert the results.
    if values_to_be_inserted:
        phrase_col.insert_many(values_to_be_inserted)

    client.close()
