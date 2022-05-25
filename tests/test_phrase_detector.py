"""Tests for phrase detector module."""
import pytest

from phrase_counter.ingest import ingest_doc


def test_ingest_doc_return_true(test_page: str) -> None:
    """Testing that the phrase counter function returns something."""
    output = ingest_doc(doc=test_page, doc_type="HTML")

    # asserts that the returned dataframe is not empty
    assert any(output)


def test_wrong_doc_type_arg(test_page: str) -> None:
    """Testing wrong input for doc_type arg in ingest_doc."""
    with pytest.raises(Exception):
        ingest_doc(doc=test_page, doc_type="Wrong Arg")


def test_check_keys_output(test_page: str) -> None:
    """Testing that relevent keys are in the output."""
    output = ingest_doc(doc=test_page, doc_type="HTML")
    sample_element = list(output.columns)
    print(sample_element)
    assert all(key in sample_element for key in ["bag", "_key", "count"])
