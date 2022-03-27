"""Tests for cleaner module."""
from phrase_counter.cleaner import cleaner, fetch_page_text


def test_fetch_html_returns_true():
    """Testing that fetch_page_text returns something."""
    webpage = "<p>hello there</p>"
    page = fetch_page_text(webpage=webpage)
    assert page


def test_extra_space_cleaner():
    """Testing that cleaner removes extra spaces."""
    dirty_text = "    there is     lots  of     spaces       here      "
    cleaned_text = cleaner(dirty_text)
    assert cleaned_text == "there is lots of spaces here"


def test_new_line_and_tab_cleaner():
    """Testing that the trimmer removes newlines and tabs."""
    dirty_text = "There is \t lots of \n newlines \n and \t tabs \n here"
    cleaned_text = cleaner(dirty_text)
    assert cleaned_text == "There is lots of newlines and tabs here"
