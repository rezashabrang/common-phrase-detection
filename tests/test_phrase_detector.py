"""Tests for phrase detector module."""
import pytest

from phrase_counter.phrase_detector import phrase_counter


def test_phrase_counter_return_true(test_page: str) -> None:
    """Testing that the phrase counter function returns something."""
    output = phrase_counter(doc=test_page, doc_type="text")

    # asserts that the returned dataframe is not empty
    assert not output.empty


def test_wrong_doc_type_arg(test_page: str) -> None:
    """Testing wrong input for doc_type arg in phrase_counter"""
    with pytest.raises(Exception):
        phrase_counter(doc=test_page, doc_type="Wrong Arg")
