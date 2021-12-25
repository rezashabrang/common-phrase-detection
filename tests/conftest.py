"""Fixtures."""
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def test_page():
    """Reading sample wikipedia html page."""
    html_path = f"{Path(__file__).parent}/data/wiki_test.html"
    with open(html_path, encoding="utf-8") as html_file:
        test_html = html_file.read()

    return test_html
