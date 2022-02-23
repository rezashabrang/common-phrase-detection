"""Testing doc-process endpoint."""
from typing import Callable

from fastapi.testclient import TestClient

from phrase_counter.routers.http_doc_processor import router

client = TestClient(router)


def test_simple_router(clean_collection: Callable[[], None]) -> None:
    """Simple test for checking router functionality."""
    sample_payload = {"document": "<p>sample</p>"}
    response = client.post(
        "http://127.0.0.1:8000/api/doc-process/?doc_type=HTML", json=sample_payload
    )
    assert response.status_code == 201


def test_with_sample_page(test_page: str) -> None:
    """Testing with sample HTML page."""
    sample_payload = {"document": test_page}
    response = client.post(
        "http://127.0.0.1:8000/api/doc-process/?doc_type=HTML", json=sample_payload
    )

    assert response.status_code == 201
