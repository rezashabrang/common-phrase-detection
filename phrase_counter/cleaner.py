"""Cleaning dirty input text."""
from typing import Any, List, Optional

import re
from html.parser import HTMLParser
from io import StringIO

import requests
from bs4 import BeautifulSoup
from cleaning_utils import clear_stop_char, replace_arabic_char
from polyglot.detect import Detector
from polyglot.detect.base import UnknownLanguage


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
    remove_stop_regex: Optional[List[Any]] = None,
    remove_highlight_regex: Optional[List[Any]] = None
    # stop_list: Optional[Iterable[str]] = None,
) -> str:
    """Main function for cleaning.

    Args:
        dirty_text: Input dirty text
        remove_stop_regex: Regex for removing stop phrases
        remove_highlight_regex: Regex for removing highlight phrases

    Returns:
        Final text ready for integration in NLP algorithms.
    """
    # ------------------- HTML Stripper -------------------
    processed_text = BeautifulSoup(dirty_text, features="html.parser").get_text()
    # ------------------- Langugae detection -------------------
    try:
        detector = Detector(processed_text)
        lang = detector.language.code
    except UnknownLanguage:
        lang = ""
    # ------------------- Linguistic phase -------------------
    if lang == "fa":
        processed_text = replace_arabic_char(processed_text)
    elif lang == "ar":
        processed_text = replace_arabic_char(processed_text, letter=False)

    processed_text = clear_stop_char(
        processed_text,
        replace_char=".",
    )

    # ------------------- Trimmer phase -------------------
    trim_pattern = re.compile(
        "\t|\n|\u200c|\u200f|\u200e|\xa0|\xad|\r"
    )
    processed_text = re.sub(trim_pattern, " ", processed_text)
    processed_text = re.sub(" +", " ", processed_text)  # space cleaner
    processed_text = processed_text.strip()

    # --------------------- Remove frequents ---------------------
    if remove_stop_regex:
        for i in remove_stop_regex:
            processed_text = re.sub(remove_stop_regex[i], "", processed_text)

    if remove_highlight_regex:
        for i in remove_highlight_regex:
            processed_text = re.sub(remove_highlight_regex[i], "", processed_text)

    processed_text = re.sub(" +", " ", processed_text)  # space cleaner
    processed_text = processed_text.strip()

    return str(processed_text)
