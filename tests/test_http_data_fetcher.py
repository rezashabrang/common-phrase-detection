"""Data fetcher endpoint tests."""
import pytest
from fastapi.exceptions import HTTPException
from fastapi.testclient import TestClient

from phrase_counter.routers.http_data_fetcher import router

client = TestClient(router)


def test_simple_data_fetcher() -> None:
    """Simple test for checking router functionality."""
    response = client.get("http://127.0.0.1:8000/api/data-fetcher/?limit=10&page=1")
    assert response.status_code == 200


def test_bad_status() -> None:
    """Testing with non registered status."""
    with pytest.raises(HTTPException):
        response = client.get("http://127.0.0.1:8000/api/data-fetcher/?status=wrong")
        assert response.status_code == 400
