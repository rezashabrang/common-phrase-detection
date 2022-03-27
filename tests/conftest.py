"""Fixtures."""
import random
import string

import pytest


@pytest.fixture(scope="session")
def test_page():
    """Reading sample wikipedia html page."""
    test_html = """<p> sample html paragraph </p>
    <p> another sample html paragraph </p>
    """
    return test_html


@pytest.fixture(scope="function")
def mock_data():
    """Creating mock data."""
    n_data = random.randint(200, 400)  # Number of random data to be created.
    status_list = [None, "stop", "highlight"]
    data = []
    for _ in range(n_data):
        sample = {
            "bag": "".join(
                random.choices(string.ascii_lowercase + " ", k=random.randint(5, 20))
            ),
            "count": random.randint(1, 4),
            "status": random.choice(status_list),
            "phrase_hash": "".join(
                random.choices(string.ascii_lowercase + string.digits, k=16)
            ),
        }
        data.append(sample)

    return data
