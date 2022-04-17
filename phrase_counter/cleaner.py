"""Cleaning dirty input text."""
from typing import Iterable, Optional

import re

import requests
from bs4 import BeautifulSoup
from cleaning_utils import clear_stop_char, clear_stop_words, replace_arabic_char
from polyglot.detect import Detector


def fetch_page_text(url: str = "", webpage: str = "") -> str:
    """Getting html pages from urls & fetching needed elements of the page.

    Args:
        url: url of the target webpage.
        webpage: string version of the webpage.

    Returns:
        text of the webpage.
    """
    # If url is defined then make the request and fetch the page.
    if url != "":
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


def cleaner(
    dirty_text: str,
    replace_stop: bool = False,
    stop_list: Optional[Iterable[str]] = None,
) -> str:
    """Main function for cleaning.

    Args:
        dirty_text: Input dirty text
        replace_stop: Whether to replace stop words or not
        stop_list: list of stop words

    Returns:
        Final text ready for integration in NLP algorithms.
    """
    # ------------------- Langugae detection -------------------
    detector = Detector(dirty_text)
    lang = detector.language.code
    # ------------------- Linguistic phase -------------------
    if lang == "fa":
        processed_text = replace_arabic_char(dirty_text)
    elif lang == "ar":
        processed_text = replace_arabic_char(dirty_text, letter=False)
    else:
        processed_text = dirty_text

    processed_text = clear_stop_char(
        processed_text,
        replace_char=".",
    )

    if replace_stop:
        processed_text = clear_stop_words(
            text=processed_text, stop_list=stop_list, replace_char="."  # type: ignore
        )
    # ------------------- HTML Stripper -------------------
    processed_text = re.sub('<[^<]+?>', '', processed_text)
    processed_text = re.sub(
        '&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-fA-F]{1,6});', '', processed_text
    )

    # ------------------- Trimmer phase -------------------
    processed_text = processed_text.replace("\t", " ").replace("\n", " ").strip()
    processed_text = processed_text.replace("\u200c", " ")  # Nim-fasele
    processed_text = re.sub(" +", " ", processed_text)  # space cleaner
    processed_text = processed_text.strip()

    return str(processed_text)
