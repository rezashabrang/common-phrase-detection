"""Fixtures."""
import os
import random
import string
from pathlib import Path
from urllib import parse

import pytest
from pymongo import MongoClient

from phrase_counter.lib.db import mongo_connection


@pytest.fixture(scope="session", autouse=True)
def initializing_db():
    """Initializing mongo database."""
    # ---------------- Updating test environment ----------------
    current_path = str(Path(__file__).parent)
    test_env = {}
    with open(current_path + "/.env.test", encoding="utf-8") as test_env_file:
        for line in test_env_file:
            env_var, env_val = line.split("=")
            test_env[env_var] = env_val.strip()
    os.environ.update(test_env)

    # Initializing test client
    username = parse.quote_plus(str(os.getenv("MONGO_INITDB_ROOT_USERNAME")))
    password = parse.quote_plus(str(os.getenv("MONGO_INITDB_ROOT_PASSWORD")))
    host = os.getenv("MONGO_HOST")
    port = os.getenv("MONGO_PORT")

    test_client = MongoClient(f"mongodb://{username}:{password}@{host}:{port}/")

    test_db = test_client[os.getenv("MONGO_PHRASE_DB")]  # Creating test database
    test_col = test_db[os.getenv("MONGO_PHRASE_COL")]  # Creating test collection
    test_col.insert_one({"test": "TEST_SAMPLE"})  # Sample data insertion

    yield
    # Cleaning up
    test_client.drop_database(os.getenv("MONGO_PHRASE_DB"))
    test_client.close()


@pytest.fixture(scope="session")
def test_page():
    """Reading sample wikipedia html page."""
    html_path = f"{Path(__file__).parent}/data/wiki_test.html"
    with open(html_path, encoding="utf-8") as html_file:
        test_html = html_file.read()

    return test_html


@pytest.fixture(scope="function")
def clean_collection():
    """Cleaning test collection."""
    yield
    test_client = mongo_connection()
    test_db = test_client[os.getenv("MONGO_PHRASE_DB")]
    test_col = test_db[os.getenv("MONGO_PHRASE_COL")]
    test_col.delete_many({})


@pytest.fixture(scope="function")
def mock_data():
    """Creating mock data."""
    n_data = random.randint(200, 400)  # Number of random data to be created.
    status_list = [None, "stop", "highlight"]
    data = []
    for _ in range(n_data):
        sample = {
            "Bag": "".join(
                random.choices(string.ascii_lowercase + " ", k=random.randint(5, 20))
            ),
            "Count": random.randint(1, 4),
            "Status": random.choice(status_list),
            "Phrase_hash": "".join(
                random.choices(string.ascii_lowercase + string.digits, k=16)
            ),
        }
        data.append(sample)

    return data
