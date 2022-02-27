"""Tests for phrase detector module."""
import pytest

from phrase_counter.lib.phrase_detector import phrase_counter


def test_phrase_counter_return_true(test_page: str) -> None:
    """Testing that the phrase counter function returns something."""
    output = phrase_counter(doc=test_page, doc_type="HTML")

    # asserts that the returned dataframe is not empty
    assert output


def test_wrong_doc_type_arg(test_page: str) -> None:
    """Testing wrong input for doc_type arg in phrase_counter."""
    with pytest.raises(Exception):
        phrase_counter(doc=test_page, doc_type="Wrong Arg")


def test_check_keys_output(test_page: str) -> None:
    """Testing that relevent keys are in the output."""
    output = phrase_counter(doc=test_page, doc_type="HTML")
    sample_element = output[0]
    assert all(
        key in sample_element for key in ["bag", "phrase_hash", "count", "status"]
    )
