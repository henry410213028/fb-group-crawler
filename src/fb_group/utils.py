"""Utility functions module

Attributes:
    server (TYPE): Redis connection
"""
from scrapy_redis.connection import get_redis
from fb_group.settings import REDIS_URL


server = get_redis(url=REDIS_URL)


def url_enqueue(key_prefix: str, url: str):
    """Enqueue the target url into redis (list) key
    
    Args:
        key_prefix (str): Redis key prefix, according to the description in scrapy-redis document, default is spider name
        url (str): target url
    """
    if (key_prefix != "") & (url != ""):
        server.lpush(key_prefix + ":start_urls", url)


def parse_args(args: list) -> dict:
    """Convert list of command line string into key and value
    
    Args:
        args (list): List of string that came from sys.argv
    
    Returns:
        dict: As kwargs
    """
    return {i.split("=")[0]: i.split("=")[1] for i in args if "=" in i}
