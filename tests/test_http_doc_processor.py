from typing import Callable

import pytest
from fastapi.exceptions import HTTPException
from fastapi.testclient import TestClient

from phrase_counter.routers.http_doc_processor import router

client = TestClient(router)


def test_simple_router(clean_collection: Callable[[], None]) -> None:
    """Simple test for checking router functionality."""
    sample_payload = {"file": "<p>sample</p>"}
    response = client.post(
        "http://127.0.0.1:8000/api/doc-process/", json=sample_payload
    )
    assert response.status_code == 201


def test_wrong_html_format() -> None:
    """Testing for wrong payload format."""
    with pytest.raises(HTTPException):
        sample_payload = {"file": "Should not give a plain string. Only HTML format."}
        client.post("http://127.0.0.1:8000/api/doc-process/", json=sample_payload)


def test_with_sample_page(test_page) -> None:
    """Testing with sample HTML page"""
    sample_payload = {"file": test_page}
    response = client.post(
        "http://127.0.0.1:8000/api/doc-process/", json=sample_payload
    )
    
    assert response.status_code == 201
