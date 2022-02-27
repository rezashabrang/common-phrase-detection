"""Testing database functionality."""
from typing import Callable

import os
from hashlib import sha256

import pytest
from fastapi.exceptions import HTTPException

from phrase_counter.lib.db import (
    fetch_data,
    integrate_phrase_data,
    mongo_connection,
    update_status,
)


def test_insert_true(clean_collection: Callable[[], None]) -> None:
    """Testing that insertion is happening."""
    sample_res = [
        {
            "bag": "test_bag",
            "count": 5,
            "status": None,
            "phrase_hash": "Some random hash",
        }
    ]
    integrate_phrase_data(sample_res)
    test_client = mongo_connection()
    test_db = test_client[os.getenv("MONGO_PHRASE_DB")]
    test_col = test_db[os.getenv("MONGO_PHRASE_COL")]
    mongo_rows = test_col.find({"phrase_hash": "Some random hash"})

    assert list(mongo_rows)


def test_update_true(clean_collection: Callable[[], None]) -> None:
    """Testing the update is happening in mongo."""
    sample_res = [
        {
            "bag": "test_bag",
            "count": 5,
            "status": None,
            "phrase_hash": "Some random hash",
        }
    ]
    integrate_phrase_data(sample_res)
    integrate_phrase_data(sample_res)  # Integrating again for update to happen
    test_client = mongo_connection()
    test_db = test_client[os.getenv("MONGO_PHRASE_DB")]
    test_col = test_db[os.getenv("MONGO_PHRASE_COL")]
    mongo_rows = test_col.find({"phrase_hash": "Some random hash"})
    assert list(mongo_rows)[0]["count"] == 10


def test_update_status_true(clean_collection: Callable[[], None]) -> None:
    """Testing that status update is working."""
    sample_res = [
        {
            "bag": "test_bag",
            "count": 5,
            "status": None,
            "phrase_hash": sha256(b"test_bag").hexdigest(),
        }
    ]
    integrate_phrase_data(sample_res)
    update_status("test_bag", "highlight")
    test_client = mongo_connection()
    test_db = test_client[os.getenv("MONGO_PHRASE_DB")]
    test_col = test_db[os.getenv("MONGO_PHRASE_COL")]
    mongo_rows = test_col.find({"phrase_hash": sample_res[0]["phrase_hash"]})
    status = list(mongo_rows)[0]["status"]
    assert status == "highlight"


def test_update_status_new_phrase():
    """Testing that for a new phrase function return not found exception."""
    with pytest.raises(HTTPException):
        update_status("sample", "stop")


def test_fetch_data_true(clean_collection, mock_data):
    """Simple test that checks if data is being fetched."""
    integrate_phrase_data(mock_data)
    res = fetch_data(status=None, limit=100, offset=0)
    assert res


def test_check_sort(clean_collection, mock_data):
    """Checking that returned data is sorted base on count."""
    integrate_phrase_data(mock_data)
    res = fetch_data(status=None, limit=10, offset=0)

    for i in range(len(res) - 1):
        assert res[i]["count"] >= res[i + 1]["count"]


def test_check_keys(clean_collection, mock_data):
    """Checking the keys in records."""
    integrate_phrase_data(mock_data)
    res = fetch_data(status=None, limit=10, offset=0)
    keys_list = res[0].keys()
    assert "bag" in keys_list
    assert "status" in keys_list
    assert "count" in keys_list


def test_check_len(clean_collection, mock_data):
    """Checking that the length of the returned data is equal to limit arg."""
    integrate_phrase_data(mock_data)
    res = fetch_data(status=None, limit=10, offset=0)
    assert len(res) == 10


def test_check_statuses(clean_collection, mock_data):
    """Checking statuses."""
    integrate_phrase_data(mock_data)
    statuses = [None, "highlight", "stop", "with_status", "no_status"]
    for status in statuses:
        res = fetch_data(status=status, limit=10, offset=0)
        assert res
        assert len(res) == 10
        for i in range(len(res) - 1):
            assert res[i]["count"] >= res[i + 1]["count"]
