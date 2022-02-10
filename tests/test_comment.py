import pytest
from tests import FILE_TESTCASE, create_response, create_soup
from fb_group.spiders.comment import CommentSpider, parse_data


class CommentParse:

    spider = CommentSpider()

    def test_parse_replies(self, test_args):
        response = create_response(test_args["html"])
        replies = self.spider.parse_replies(response)
        assert len(replies) == test_args["n_reply"]

    def test_parse_data(self, test_args):
        response = create_response(test_args["html"])
        replies = self.spider.parse_replies(response)
        for reply in replies:
            soup = create_soup(reply)
            data = parse_data(soup)
            assert len(data[0]) > 0
            assert len(data[1]) > 0

    def test_parse_next_page(self, test_args):
        response = create_response(test_args["html"])
        next_page = self.spider.parse_next_page(response)
        if test_args["with_next_page"]:
            assert next_page.startswith("/comment/replies/")
        else:
            assert next_page is None


@pytest.mark.parametrize(
    "test_args",
    [
        (
            {
                "html": FILE_TESTCASE["reply_many_page.html"],
                "n_reply": 31,
                "with_next_page": True,
            }
        ),
        (
            {
                "html": FILE_TESTCASE["reply_many.html"],
                "n_reply": 8,
                "with_next_page": False,
            }
        ),
        (
            {
                "html": FILE_TESTCASE["reply_one.html"],
                "n_reply": 2,
                "with_next_page": False,
            }
        ),
    ],
)
class TestCommentParse(CommentParse):
    pass
