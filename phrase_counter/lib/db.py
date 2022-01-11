"""Mongo Database Configs."""
from fastapi.exceptions import HTTPException
from pymongo import MongoClient
from urllib import parse
import os
from typing import List, Dict, Union
from hashlib import sha256
from pymongo import DESCENDING


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


def update_status(
    phrase: str,
    status: str
) -> None:
    """Updates the status of given phrase.

        Args:
            phrase: Given keyword for status update.
            status: stop or highlight.

        Raises:
            HTTPException: If no phrase is found in database.
    """
    # Switching to collection
    client = mongo_connection()
    phrasedb = client[os.getenv("MONGO_PHRASE_DB")]  # Phrase database
    phrase_col = phrasedb[os.getenv("MONGO_PHRASE_COL")]  # Phrase collection
    phrase_hash = sha256(phrase.encode()).hexdigest()  # Hashing the phrase

    # Finding the phrase in db
    query = {"Phrase_hash": phrase_hash}
    query_res = phrase_col.find(query)
    if list(query_res):
        # Updating status
        update_query = {"$set": {"Status": status}}
        phrase_col.update_one(query, update_query)

    # If there is not any record then raise exception
    else:
        raise HTTPException(
            status_code=404,
            detail="no-phrase"
        )


def fetch_data(
    status: Union[str, None],
    limit: int,
    offset: int
) -> List[Dict[str, str]]:
    """Fetching data from mongo"""
    # ----------------- Client Initialization ----------------
    client = mongo_connection()
    phrasedb = client[os.getenv("MONGO_PHRASE_DB")]  # Phrase database
    phrase_col = phrasedb[os.getenv("MONGO_PHRASE_COL")]  # Phrase collection

    # If no status is given fetch all of available data.
    if status is None:  # Fetching all records
        result = list(phrase_col.find(
            {},
            limit=limit,
            skip=offset,
            projection={"_id": False, "Phrase_hash": False},
            sort=[("Count", DESCENDING)]
        ))
    elif status == "highlight":  # Fetching highlight phrases
        result = list(phrase_col.find(
            {"Status": "highlight"},
            limit=limit,
            skip=offset,
            projection={"_id": False, "Phrase_hash": False},
            sort=[("Count", DESCENDING)]
        ))
    elif status == "stop":  # Fetching stop phrases
        result = list(phrase_col.find(
            {"Status": "stop"},
            limit=limit,
            skip=offset,
            projection={"_id": False, "Phrase_hash": False},
            sort=[("Count", DESCENDING)]
        ))
    elif status == "with_status":  # Fetching records that status IS NOT NULL
        result = list(phrase_col.find(
            {"Status": {"$ne": None}},
            limit=limit,
            skip=offset,
            projection={"_id": False, "Phrase_hash": False},
            sort=[("Count", DESCENDING)]
        ))
    elif status == "no_status":  # Fetching records that status IS NULL
        result = list(phrase_col.find(
            {"Status": None},
            limit=limit,
            skip=offset,
            projection={"_id": False, "Phrase_hash": False},
            sort=[("Count", DESCENDING)]
        ))

    return result
