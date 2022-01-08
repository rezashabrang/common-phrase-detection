from typing import Callable

from hashlib import sha256

import pytest
from fastapi.exceptions import HTTPException
from fastapi.testclient import TestClient

from phrase_counter.lib.db import integrate_phrase_data
from phrase_counter.routers.http_status_updater import router

client = TestClient(router)


def test_simple_router(clean_collection: Callable[[], None]) -> None:
    """Simple test for checking router functionality."""
    sample_res = [
        {
            "Bag": "sample",
            "Count": 1,
            "Status": None,
            "Phrase_hash": sha256("sample".encode()).hexdigest(),
        }
    ]
    integrate_phrase_data(sample_res)

    response = client.get("http://127.0.0.1:8000/api/status-updater/sample/0")
    assert response.status_code == 201


def test_simple_router_2(clean_collection: Callable[[], None]) -> None:
    """Simple test for checking router functionality."""
    sample_res = [
        {
            "Bag": "sample",
            "Count": 1,
            "Status": None,
            "Phrase_hash": sha256("sample".encode()).hexdigest(),
        }
    ]
    integrate_phrase_data(sample_res)

    response = client.get("http://127.0.0.1:8000/api/status-updater/sample/1")
    assert response.status_code == 201


def test_wrong_code(clean_collection: Callable[[], None]) -> None:
    """Testing when a wrong status code is given."""
    sample_res = [
        {
            "Bag": "sample",
            "Count": 1,
            "Status": None,
            "Phrase_hash": "Some random hash",
        }
    ]
    integrate_phrase_data(sample_res)
    with pytest.raises(HTTPException):
        response = client.get("http://127.0.0.1:8000/api/status-updater/sample/5")
        assert response.status_code == 400


def test_new_phrase() -> None:
    """Testing when a new phrase is given."""
    with pytest.raises(HTTPException):
        response = client.get("http://127.0.0.1:8000/api/status-updater/sample/1")
        assert response.status_code == 404
