from typing import Callable

import os
from hashlib import sha256

import pytest
from fastapi.exceptions import HTTPException

from phrase_counter.lib.db import integrate_phrase_data, mongo_connection, update_status


def test_insert_true(clean_collection: Callable[[], None]) -> None:
    """Testing that insertion is happening."""
    sample_res = [
        {
            "Bag": "test_bag",
            "Count": 5,
            "Status": None,
            "Phrase_hash": "Some random hash",
        }
    ]
    integrate_phrase_data(sample_res)
    test_client = mongo_connection()
    test_db = test_client[os.getenv("MONGO_PHRASE_DB")]
    test_col = test_db[os.getenv("MONGO_PHRASE_COL")]
    mongo_rows = test_col.find({"Phrase_hash": "Some random hash"})

    assert list(mongo_rows)


def test_update_true(clean_collection: Callable[[], None]) -> None:
    """Testing the update is happening in mongo."""
    sample_res = [
        {
            "Bag": "test_bag",
            "Count": 5,
            "Status": None,
            "Phrase_hash": "Some random hash",
        }
    ]
    integrate_phrase_data(sample_res)
    integrate_phrase_data(sample_res)  # Integrating again for update to happen
    test_client = mongo_connection()
    test_db = test_client[os.getenv("MONGO_PHRASE_DB")]
    test_col = test_db[os.getenv("MONGO_PHRASE_COL")]
    mongo_rows = test_col.find({"Phrase_hash": "Some random hash"})
    assert list(mongo_rows)[0]["Count"] == 10


def test_update_status_true(clean_collection: Callable[[], None]) -> None:
    """Testing that status update is working."""
    sample_res = [
        {
            "Bag": "test_bag",
            "Count": 5,
            "Status": None,
            "Phrase_hash": sha256("test_bag".encode()).hexdigest(),
        }
    ]
    integrate_phrase_data(sample_res)
    update_status("test_bag", "highlight")
    test_client = mongo_connection()
    test_db = test_client[os.getenv("MONGO_PHRASE_DB")]
    test_col = test_db[os.getenv("MONGO_PHRASE_COL")]
    mongo_rows = test_col.find({"Phrase_hash": sample_res[0]["Phrase_hash"]})
    status = list(mongo_rows)[0]["Status"]
    assert status == "highlight"


def test_update_status_new_phrase():
    """Testing that for a new phrase function return not found exception."""
    with pytest.raises(HTTPException):
        update_status("sample", "stop")
