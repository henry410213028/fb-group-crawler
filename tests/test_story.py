import pytest
from tests import FILE_TESTCASE, create_response
from fb_group.spiders.story import StorySpider


class StoryParse:

    spider = StorySpider()

    def test_parse_content(self, test_args):
        response = create_response(test_args["html"])
        content = self.spider.parse_content(response)
        assert test_args["string"] in content

    def test_parse_content_image(self, test_args):
        response = create_response(test_args["html"])
        iamges = self.spider.parse_content_image(response)
        assert test_args["n_image"] == len(iamges)

    def test_parse_comments(self, test_args):
        response = create_response(test_args["html"])
        comment = self.spider.parse_comments(response)
        assert len(comment) == test_args["n_comment"]

    def test_parse_replies(self, test_args):
        response = create_response(test_args["html"])
        replies = self.spider.parse_replies(response)
        assert len(replies) == test_args["n_reply_page"]

    def test_parse_next_page(self, test_args):
        response = create_response(test_args["html"])
        next_page = self.spider.parse_next_page(response)
        if test_args["with_next_page"]:
            assert "m.facebook.com/groups" in next_page
        else:
            assert next_page is None


@pytest.mark.parametrize(
    "test_args",
    [
        (
            {
                "html": FILE_TESTCASE["story_comment_many_page.html"],
                "string": "大家上次黑五特價都有補到貨嗎？",
                "n_image": 2,
                "n_comment": 30,
                "n_reply_page": 11,
                "with_next_page": True,
            }
        ),
        (
            {
                "html": FILE_TESTCASE["story_comment_one_page.html"],
                "string": "不要以蘿蔔糕上的條紋來分切",
                "n_image": 1,
                "n_comment": 8,
                "n_reply_page": 4,
                "with_next_page": False,
            }
        ),
        (
            {
                "html": FILE_TESTCASE["story_comment_none.html"],
                "string": "",
                "n_image": 0,
                "n_comment": 0,
                "n_reply_page": 0,
                "with_next_page": False,
            }
        ),
        (
            {
                "html": FILE_TESTCASE["story_photo_only.html"],
                "string": "",
                "n_image": 1,
                "n_comment": 1,
                "n_reply_page": 1,
                "with_next_page": False,
            }
        ),
        (
            {
                "html": FILE_TESTCASE["story_text_only.html"],
                "string": "發現Epson除了較原稿顏色深些，其他畫質與原稿看起來幾乎無異。",
                "n_image": 0,
                "n_comment": 8,
                "n_reply_page": 6,
                "with_next_page": False,
            }
        ),
        (
            {
                "html": FILE_TESTCASE["story_text_with_many_photo.html"],
                "string": "#79元2入",
                "n_image": 5,
                "n_comment": 30,
                "n_reply_page": 9,
                "with_next_page": True,
            }
        ),
        (
            {
                "html": FILE_TESTCASE["story_text_with_one_photo.html"],
                "string": "PRIEURE SAINT COME法國白葡萄酒2019，透明淺金色蘋果和新鮮桃子香氣，酒體輕盈中等酸度，適合搭配海鮮等料理。",
                "n_image": 1,
                "n_comment": 24,
                "n_reply_page": 0,
                "with_next_page": False,
            }
        ),
        (
            {
                "html": FILE_TESTCASE["story_text_with_one_video.html"],
                "string": "過年買的好市多烤雞，旋風烤箱加熱處理，外皮烤的酥脆~轉阿轉~看起來蠻療癒的~~容量大就是有這個好處",
                "n_image": 0,
                "n_comment": 10,
                "n_reply_page": 7,
                "with_next_page": False,
            }
        ),
        (
            {
                "html": FILE_TESTCASE["story_text_with_presentation.html"],
                "string": "這間Costco已經不是從前的Costco 以前的CP值超高，東西多樣化且價格不貴，現在只是一間收會員費的家樂福，東西還比家樂福少，好幾次逛了一圈空手回家",
                "n_image": 0,
                "n_comment": 30,
                "n_reply_page": 4,
                "with_next_page": True,
            }
        ),
        (
            {
                "html": FILE_TESTCASE["story_video_only.html"],
                "string": "",
                "n_image": 0,
                "n_comment": 1,
                "n_reply_page": 0,
                "with_next_page": False,
            }
        ),
    ],
)
class TestStoryParse(StoryParse):
    pass
