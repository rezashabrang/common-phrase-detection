"""Cleaning dirty input text."""
from io import StringIO

import re
from html.parser import HTMLParser

import requests
from bs4 import BeautifulSoup
from cleaning_utils import clear_stop_char, replace_arabic_char
from polyglot.detect import Detector
from polyglot.detect.base import UnknownLanguage


class MLStripper(HTMLParser):
    """Class for cleaning HTML"""

    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = StringIO()

    def handle_data(self, data):
        """Data Handling"""
        self.text.write(data)

    def get_data(self):
        """Getting stripped text."""
        return self.text.getvalue()


def strip_tags(html: str) -> str:
    """Strip HTML tags"""
    s = MLStripper()
    s.feed(html)
    return s.get_data()


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
    # stop_list: Optional[Iterable[str]] = None,
) -> str:
    """Main function for cleaning.

    Args:
        dirty_text: Input dirty text
        replace_stop: Whether to replace stop words or not
        stop_list: list of stop words

    Returns:
        Final text ready for integration in NLP algorithms.
    """
    # ------------------- HTML Stripper -------------------
    processed_text = strip_tags(dirty_text)
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

    # if replace_stop:
    #     processed_text = clear_stop_words(
    #         text=processed_text, stop_list=stop_list, replace_char="."  # type: ignore
    #     )

    # ------------------- Trimmer phase -------------------
    processed_text = processed_text.replace("\t", " ").replace("\n", " ").strip()
    processed_text = processed_text.replace("\u200c", " ")  # Nim-fasele
    processed_text = re.sub(" +", " ", processed_text)  # space cleaner
    processed_text = processed_text.strip()

    return str(processed_text)
