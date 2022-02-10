"""Spider module for CommentSpider
"""
import re
from scrapy_redis.spiders import RedisSpider
from bs4 import BeautifulSoup
from fb_group.items import CommentItem
from fb_group.utils import url_enqueue


class CommentSpider(RedisSpider):

    """Scrapy spider class for download facebook group story comment page
    
    Attributes:
        allowed_domains (list): Url domain for facebook
        name (str): Spider name
    """
    
    name = "comment"
    allowed_domains = ["mobile.facebook.com"]

    def get_comment_id(self, response) -> str:
        """Get comment id from current reply page
        
        Args:
            response (scrapy.http.response.Response): HTTP response object
        
        Returns:
            str: Comment id
        """
        ctoken = re.sub(
            r".*replies\/\?ctoken=(\d+_\d+)\&.*", "\\1", response.request.url
        )
        return ctoken.split("_")[-1]

    def parse_replies(self, response) -> list:
        """Parse comment elements in current reply page
        
        Args:
            response (scrapy.http.response.Response): HTTP response object
        
        Returns:
            list: List of reply elements
        
        Raises:
            ValueError: Description
        """
        xpath = "//div[@data-sigil='comment']"
        replies = response.xpath(xpath).getall()
        if replies:
            return replies
        raise ValueError("Reply was not found in page")

    def parse_next_page(self, response):
        """Parse pagination url
        
        Args:
            response (scrapy.http.response.Response): HTTP response object
        
        Returns:
            str: Url that paginate to following item page
        """
        xpath = "//div[contains(@id, 'comment_replies_more')]//a/@href"
        return response.xpath(xpath).get()

    def parse(self, response):
        """Default parsing main function, set as request callback
        
        Args:
            response (scrapy.http.response.Response): HTTP Response object
        
        Yields:
            scrapy.item.Item: CommentItem
        """
        replies = self.parse_replies(response)
        for reply in replies[1:]:  # replies[0] is parent comment, do not save again
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

        next_page = self.parse_next_page(response)
        if next_page:  # startswith("/comment/replies/")
            url = "https://" + self.allowed_domains[0] + next_page
            url_enqueue(self.name, url)


def parse_data(soup) -> list:
    """Parse comment infornation
    
    Args:
        soup (bs4.BeautifulSoup): Current reply element
    
    Returns:
        list: Comment body and author name for current comment
    """
    content = soup.find("div", {"data-sigil": "comment-body"})
    if content:
        author_name = content.find_previous_sibling()
        if author_name:
            return [content.get_text(), author_name.get_text()]
        return [content.get_text(), ""]
    else:
        return ["", ""]
