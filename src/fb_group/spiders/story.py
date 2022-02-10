import re
from scrapy_redis.spiders import RedisSpider
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from fb_group.items import PostItem, CommentItem
from fb_group.utils import url_enqueue
from fb_group.spiders.comment import parse_data


class StorySpider(RedisSpider):
    name = "story"
    allowed_domains = ["mobile.facebook.com"]

    def get_request_path(self, response) -> str:
        path = urlparse(response.request.url).path
        return re.sub(r"(.*)\/$", "\\1", path)

    def parse_content(self, response) -> str:
        xpath = "//div[@class='story_body_container']//header/following-sibling::div"
        content = "".join(response.xpath(xpath + "//text()").getall())
        return content

    def parse_comments(self, response) -> list:
        xpath = "//div[@data-sigil='comment']"
        comments = response.xpath(xpath).getall()
        if comments:
            return comments
        # comment parent element
        if response.xpath("//div[@data-sigil='m-mentions-expand']").get():
            return []
        raise ValueError("Comment was not found in page")

    def parse_replies(self, response) -> list:
        xpath = "//div[@data-sigil='replies-see-more']//a/@href"
        replies = response.xpath(xpath).getall()
        return [x for x in replies if x.startswith("/comment/replies/")]

    def parse_next_page(self, response) -> str:
        xpath = "//div[contains(@id, 'see_prev_')]//a/@href"
        return response.xpath(xpath).get()

    def parse(self, response):
        items = []
        story_id = self.get_request_path(response).split("/")[-1]

        # Post content is only parse in first visited page, not following page
        if "?p=" not in response.request.url:
            items.append(
                PostItem({"ID": story_id, "CONTENT": self.parse_content(response),})
            )

        comments = self.parse_comments(response)
        for comment in comments:
            soup = BeautifulSoup(comment, "lxml")
            comment_id = soup.find("div").get("id")
            if comment_id.isdigit():
                data = parse_data(soup)
                items.append(
                    CommentItem(
                        {
                            "PARENT_ID": story_id,
                            "ID": comment_id,
                            "AUTHOR_NAME": data[1],
                            "CONTENT": data[0],
                        }
                    )
                )
            else:
                self.logger.warning(f"Unexpected Comment ID: {comment_id}")

        replies = self.parse_replies(response)
        for reply in replies:
            url = "https://" + self.allowed_domains[0] + reply
            url_enqueue("comment", url)

        next_page = self.parse_next_page(response)
        if next_page:
            url_enqueue(self.name, next_page)

        for item in items:
            yield item
