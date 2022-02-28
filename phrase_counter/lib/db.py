"""Mongo Database Configs."""
from typing import Collection, Dict, List, Union

import os
from hashlib import sha256
from urllib import parse

from fastapi.exceptions import HTTPException
from arango import ArangoClient
import pandas as pd
from pandas import DataFrame
from itertools import combinations


def arango_connection() -> ArangoClient:
    """Connecting to arango."""
    host = os.getenv("ARANGO_HOST")
    port = os.getenv("ARANGO_PORT")
    arango_client = ArangoClient(
        hosts=f"http://{host}:{port}"
    )

    return arango_client


def prepare_phrase_data(dataframe: DataFrame):
    """Converting phrase dataframe and creating edges for integration

        Args:
            dataframe: populated phrase dataframe

    """
    vertex_col_name = os.getenv("ARANGO_VERTEX_COLLECTION")

    phrase_hashes = dataframe["phrase_hash"]
    dataframe = dataframe.rename(columns={"phrase_hash": "_key"})

    # Finding all possible permutation of 2 for phrases
    phrase_relations = combinations(phrase_hashes, 2)

    # --------------- Creating edge dataframe ---------------
    # Inserting combinations
    edge_df = pd.DataFrame(phrase_relations, columns=["_from", "_to"])

    # Creating key value
    edge_df["_key"] = edge_df.apply(
        lambda row: row["_from"] + "_" + row["_to"], axis=1
    )

    edge_df["_from"] = vertex_col_name + "/" + edge_df["_from"].astype(str)
    edge_df["_to"] = vertex_col_name + "/" + edge_df["_to"].astype(str)
    edge_df["count"] = 1

    phrase_col = dataframe.to_dict(orient="records")
    edge_col = edge_df.to_dict(orient="records")

    return phrase_col, edge_col


def integrate_phrase_data(
    result: Dict[str, int],
    type_data="vertex"
) -> None:
    """Inserting or updating phrase data in arango collection.

    Args:
        phrase_res: JSON result of counted phrases.
        edge_res: JSON result of edges.
    """
    # ------------------ Initialization & Connecting to database ------------------
    vertex_col_name = os.getenv("ARANGO_VERTEX_COLLECTION")
    edge_col_name = os.getenv("ARANGO_EDGE_COLLECTION")
    username = os.getenv("ARANGO_USER")
    password = os.getenv("ARANGO_PASS")
    database = os.getenv("ARANGO_DATABASE")
    client = arango_connection()
    phrase_db = client.db(database, username=username, password=password)

    if type_data == "vertex":
        collection = phrase_db.collection(vertex_col_name)
    elif type_data == "edge":
        collection = phrase_db.collection(edge_col_name)

    bulk_insert = []  # initializing bulk insert list

    # If record exists then update it otherwise append to bulk insert list
    for item in result:
        find_query = {"_key": item["_key"]}
        find_res = list(collection.find(find_query))
        if find_res:
            old_count = find_res[0]["count"]
            collection.update_match(find_query, {"count": old_count + 1})
        else:
            bulk_insert.append(item)

    collection.import_bulk(bulk_insert)

    client.close()


# -------------------------------------------------------------------------------------

def update_status(phrase: str, status: str) -> None:
    """Updates the status of given phrase.

    Args:
        phrase: Given keyword for status update.
        status: stop or highlight.

    Raises:
        HTTPException: If no phrase is found in database.
    """
    pass


def fetch_data(
    status: Union[str, None], limit: int, offset: int
) -> List[Dict[str, str]]:
    """Fetching data from mongo."""
    # ----------------- Client Initialization ----------------
    pass
