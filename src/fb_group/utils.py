from scrapy_redis.connection import get_redis
from fb_group.settings import REDIS_URL


server = get_redis(url=REDIS_URL)


def url_enqueue(key_prefix: str, url: str):
    if (key_prefix != "") & (url != ""):
        server.lpush(key_prefix + ":start_urls", url)


def parse_args(args: list) -> dict:
    return {i.split("=")[0]: i.split("=")[1] for i in args if "=" in i}
