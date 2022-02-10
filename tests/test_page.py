import pytest
from tests import FILE_TESTCASE, create_response, create_soup
from fb_group.spiders.page import PageSpider


class PageParse:

    spider = PageSpider(group_id="0")

    def test_parse_stories(self, test_args):
        response = create_response(test_args["html"])
        stories = self.spider.parse_stories(response)
        assert len(stories) == test_args["n_story"]

    def test_parse_metadata(self, test_args):
        soup = create_soup(test_args["html"])
        metadata = self.spider.parse_metadata(soup)
        assert len(metadata.keys()) > 0

    def test_parse_data(self, test_args):
        response = create_response(test_args["html"])
        pages = self.spider.parse_stories(response)
        for i, page in enumerate(pages):
            soup = create_soup(page)
            data = self.spider.parse_data(soup)
            assert data[0] == test_args["n_likes"][i]
            assert data[1] == test_args["n_comments"][i]

    def test_parse_next_page(self, test_args):
        response = create_response(test_args["html"])
        next_page = self.spider.parse_next_page(response)
        assert next_page.startswith("/groups/")


@pytest.mark.parametrize(
    "test_args",
    [
        (
            {
                "html": FILE_TESTCASE["groups_main_page.html"],
                "n_story": 20,
                "n_likes": [
                    356,
                    611,
                    1011,
                    187,
                    1314,
                    397,
                    456,
                    285,
                    1084,
                    508,
                    176,
                    16,
                    244,
                    335,
                    262,
                    77,
                    768,
                    163,
                    1001,
                    898,
                ],
                "n_comments": [
                    109,
                    102,
                    286,
                    10,
                    47,
                    310,
                    172,
                    23,
                    473,
                    107,
                    35,
                    7,
                    118,
                    28,
                    55,
                    5,
                    695,
                    34,
                    135,
                    64,
                ],
            }
        ),
    ],
)
class TestPageParse(PageParse):
    pass
