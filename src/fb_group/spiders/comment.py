import re
from scrapy_redis.spiders import RedisSpider
from bs4 import BeautifulSoup
from fb_group.items import CommentItem
from fb_group.utils import url_enqueue


class CommentSpider(RedisSpider):
    name = "comment"
    allowed_domains = ["mobile.facebook.com"]

    def get_comment_id(self, response) -> str:
        ctoken = re.sub(
            r".*replies\/\?ctoken=(\d+_\d+)\&.*", "\\1", response.request.url
        )
        return ctoken.split("_")[-1]

    def parse_replies(self, response) -> list:
        xpath = "//div[@data-sigil='comment']"
        replies = response.xpath(xpath).getall()
        if replies:
            return replies
        raise ValueError("Reply was not found in page")

    def parse_next_page(self, response):
        xpath = "//div[contains(@id, 'comment_replies_more')]//a/@href"
        next_page = response.xpath(xpath).get()
        if next_page:  # startswith("/comment/replies/")
            url = "https://" + self.allowed_domains[0] + next_page
            url_enqueue(self.name, url)

    def parse(self, response):
        replies = self.parse_replies(response)
        for reply in replies[1:]:  # replies[0] is parent comment
            soup = BeautifulSoup(reply, "lxml")
            reply_id = soup.find("div").get("id")
            data = parse_data(soup)
            if reply_id.isdigit():
                yield CommentItem(
                    {
                        "PARENT_ID": self.get_comment_id(response),
                        "ID": reply_id,
                        "AUTHOR_NAME": data[0],
                        "CONTENT": data[1],
                    }
                )

        self.parse_next_page(response)


def parse_data(soup) -> list:
    content = soup.find("div", {"data-sigil": "comment-body"})
    if content:
        author_name = content.find_previous_sibling()
        if author_name:
            return [content.get_text(), author_name.get_text()]
        return [content.get_text(), ""]
    else:
        return ["", ""]
