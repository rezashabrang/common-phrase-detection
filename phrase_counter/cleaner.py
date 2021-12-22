"""Cleaning dirty input text."""
import re

import requests
from bitas_utils import clear_stop_char, replace_arabic_char
from bs4 import BeautifulSoup


def fetch_page_text(url: str = "", webpage: str = "") -> str:
    """Getting html pages from urls & fetching needed elements of the page.

    Args:
        url: url of the target webpage.
        webpage: string version of the webpage.

    Returns:
        text of the webpage.
    """
    # If url is defined then make the request and fetch the page.
    if not url:
        req = requests.get(url=url)
        soup = BeautifulSoup(req.content, "html.parser")

    # If not then make soup from given webpage.
    else:
        soup = BeautifulSoup(webpage, "html.parser")

    # Getting needed tags and stripped strings
    whole_page = ""
    for group in soup(["h1", "h2", "h3", "h4", "h5", "h6", "p"]):
        for text in group.stripped_strings:
            whole_page += text + " "

    whole_page = whole_page.strip()

    return whole_page


def cleaner(dirty_text: str) -> str:
    """Main function for cleaning.

    Args:
        dirty_text: Input dirty text

    Returns:
        Final text ready for integration in NLP algorithms.
    """
    # ------------------- Linguistic phase -------------------
    processed_text = replace_arabic_char(dirty_text)
    processed_text = clear_stop_char(processed_text)

    # ------------------- Trimmer phase -------------------
    processed_text = processed_text.replace("\t", " ").replace("\n", " ").strip()
    processed_text = processed_text.replace("\u200c", " ")  # Nim-fasele
    processed_text = re.sub(" +", " ", processed_text)  # space cleaner
    processed_text = processed_text.strip()

    return str(processed_text)
