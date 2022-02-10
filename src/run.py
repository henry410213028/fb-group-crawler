"""Crawler main entry point

python run.py group_id=1260448967306807
"""
import sys
from scrapy.settings import Settings
from scrapy.crawler import CrawlerProcess
from fb_group.utils import parse_args
from fb_group.spiders.page import PageSpider
from fb_group.spiders.story import StorySpider
from fb_group.spiders.comment import CommentSpider


def main(kwargs):
    settings = Settings()
    settings.setmodule('fb_group.settings', priority='project')
    settings.setdict(kwargs, priority='project')
    process = CrawlerProcess(settings)
    process.crawl(PageSpider)
    process.crawl(StorySpider)
    process.crawl(CommentSpider)
    process.start()


if __name__ == "__main__":
    print(sys.argv)
    main(parse_args(sys.argv[1:]))
