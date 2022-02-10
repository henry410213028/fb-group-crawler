import os
import re
import json
from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.exceptions import CloseSpider
from bs4 import BeautifulSoup
from fb_group.items import StoryItem
from fb_group.utils import url_enqueue


class PageSpider(Spider):
    name = "page"
    allowed_domains = ["mobile.facebook.com"]
    start_urls = ["https://mobile.facebook.com/groups/"]

    def __init__(self, group_id: str, **kwargs):
        super().__init__(**kwargs)
        self.group_id = str(int(group_id or os.environ.get("GROUP_ID")))

    def start_requests(self):
        url = self.start_urls[0] + self.group_id
        yield Request(url, callback=self.parse, dont_filter=True)

    def parse_stories(self, response) -> list:
        xpath = "//*[@id='m_group_stories_container']//article"
        stories = response.xpath(xpath).getall()
        if stories:
            return stories
        raise ValueError("Story was not found in page")

    def parse_metadata(self, soup) -> dict:
        return json.loads(soup.find("article").get("data-ft"))

    def get_story_id(self, metadata) -> str:
        story_id = str(
            metadata["page_insights"][self.group_id]["post_context"]["story_fbid"][0]
        )
        url = (
            "https://"
            + self.allowed_domains[0]
            + f"/groups/{self.group_id}/permalink/{story_id}"
        )
        url_enqueue("story", url)
        return story_id

    def get_publish_time(self, metadata) -> int:
        publish_time = int(
            metadata["page_insights"][self.group_id]["post_context"]["publish_time"]
        )
        return publish_time

    def parse_data(self, soup) -> list:
        count_pattern = re.compile(r"([\d,]+)\s*Likes?\s*([\d,]+)\s*[C|c]omments?.*")
        count_text = (
            soup.find("div", class_="story_body_container")
            .find_next_sibling()
            .get_text()
        )
        n_like = count_pattern.sub("\\1", count_text).replace(",", "")
        n_comment = count_pattern.sub("\\2", count_text).replace(",", "")
        return [
            int(n_like) if n_like.isdigit() else None,
            int(n_comment) if n_comment.isdigit() else None,
        ]

    def parse_next_page(self, response):
        xpath = "//*[@id='m_more_item']//a/@href"
        return response.xpath(xpath).get()

    def parse(self, response):
        stories = self.parse_stories(response)
        for story in stories:
            soup = BeautifulSoup(story, "lxml")
            metadata = self.parse_metadata(soup)
            story_id = self.get_story_id(metadata)
            publish_time = self.get_publish_time(metadata)
            data = self.parse_data(soup)
            yield StoryItem(
                {
                    "ID": story_id,
                    "PUBLISH_TIME": publish_time,
                    "AUTHOR_ID": str(metadata["content_owner_id_new"]),
                    "AUTHOR_NAME": soup.find("h3").find("a").text,
                    "N_LIKE": data[0],
                    "N_COMMENT": data[1],
                }
            )

        next_page = self.parse_next_page(response)
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        settings = crawler.settings
        spider = cls(
            settings.get("group_id", ""),
            **kwargs,
        )
        spider._set_crawler(crawler)
        return spider
