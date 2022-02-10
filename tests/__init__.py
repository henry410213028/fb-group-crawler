from typing import List
from pathlib import Path
from scrapy.http import HtmlResponse
from bs4 import BeautifulSoup


TESTCASE_FILENAMES = [
    "groups_main_page.html",
    "reply_many.html",
    "reply_many_page.html",
    "reply_one.html",
    "story_comment_many_page.html",
    "story_comment_one_page.html",
    "story_photo_only.html",
    "story_text_only.html",
    "story_text_with_many_photo.html",
    "story_text_with_one_photo.html",
    "story_text_with_one_video.html",
    "story_text_with_presentation.html",
    "story_video_only.html",
]


def create_file_testcase(filenames: List[str]) -> dict:
    testcase = {}
    for filename in filenames:
        with open(Path(r"tests/testcase") / filename, "r", encoding="utf-8") as f:
            content = f.read()
        testcase.update({filename: content})
    return testcase


def create_response(body: str):
    return HtmlResponse(body=body, url="www.example.com", encoding="utf-8")


def create_soup(body: str):
    return BeautifulSoup(body, "lxml")


FILE_TESTCASE = create_file_testcase(TESTCASE_FILENAMES)
