"""Spider module for StorySpider
"""
import re
from typing import List
from scrapy_redis.spiders import RedisSpider
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from fb_group.items import PostItem, CommentItem
from fb_group.utils import url_enqueue
from fb_group.spiders.comment import parse_data


class StorySpider(RedisSpider):

    """Scrapy spider class for download facebook group story (post) page

    Attributes:
        allowed_domains (list): Url domain for facebook
        content_xpath_base (str): Xpath address that contain story text body and image urls
        name (str): Spider name
    """

    name = "story"
    allowed_domains = ["mobile.facebook.com"]
    content_xpath_base = (
        "//div[@class='story_body_container']//header/following-sibling::div"
    )

    def get_request_path(self, response) -> str:
        """Return url without query string and trailing slash

        Args:
            response (scrapy.http.response.Response): HTTP response object

        Returns:
            str: Url without query string and trailing slash
        """
        path = urlparse(response.request.url).path
        return re.sub(r"(.*)\/$", "\\1", path)

    def parse_content(self, response) -> list:
        """Parse text body for current story

        Args:
            response (scrapy.http.response.Response): HTTP response object

        Returns:
            list: Story text body
        """
        xpath = self.content_xpath_base + "//text()"
        return "".join(response.xpath(xpath).getall())

    def parse_content_image(self, response) -> List[int]:
        """Parse image urls for current story

        Args:
            response (scrapy.http.response.Response): HTTP response object

        Returns:
            list: Story image urls
        """
        xpath = self.content_xpath_base + "//a[contains(@href, '/photo')]/@href"
        links = response.xpath(xpath).getall()
        if len(links) == 1:
            return [
                int(re.sub(r"^/photo\.php\?fbid=(\d+)&id=\d+&.*", "\\1", link))
                for link in links
            ]
        return [
            int(re.sub(r"/photos/viewer/.*&photo=(\d+)&profileid=.*", "\\1", link))
            for link in links
            if link.startswith("/photos/viewer/")
        ]

    def parse_comments(self, response) -> list:
        """Parse comment elements in current story page

        Args:
            response (scrapy.http.response.Response): HTTP response object

        Returns:
            list: List of comment elements

        Raises:
            ValueError: Description
        """
        xpath = "//div[@data-sigil='comment']"
        comments = response.xpath(xpath).getall()
        if comments:
            return comments
        # comment parent element
        if response.xpath("//div[@data-sigil='m-mentions-expand']").get():
            return []
        raise ValueError("Comment was not found in page")

    def parse_replies(self, response) -> list:
        """Parse all reply urls in current story page

        Args:
            response (scrapy.http.response.Response): HTTP response object

        Returns:
            list: List of story elements
        """
        xpath = "//div[@data-sigil='replies-see-more']//a/@href"
        replies = response.xpath(xpath).getall()
        return [x for x in replies if x.startswith("/comment/replies/")]

    def parse_next_page(self, response) -> str:
        """Parse pagination url

        Args:
            response (scrapy.http.response.Response): HTTP response object

        Returns:
            str: Url that paginate to following item page
        """
        xpath = "//div[contains(@id, 'see_prev_')]//a/@href"
        return response.xpath(xpath).get()

    def parse(self, response):
        """Default parsing main function, set as request callback

        Args:
            response (scrapy.http.response.Response): HTTP Response object

        Yields:
            scrapy.item.Item: CommentItem
        """
        items = []
        story_id = self.get_request_path(response).split("/")[-1]

        # Post content is only parse in first visited page, not following page
        if "?p=" not in response.request.url:
            items.append(
                PostItem(
                    {
                        "ID": story_id,
                        "CONTENT": self.parse_content(response),
                        "IMAGES": self.parse_content_image(response),
                    }
                )
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
