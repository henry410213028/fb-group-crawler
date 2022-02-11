"""Scrapy item module
"""
from scrapy.item import Item, Field


class StoryItem(Item):

    """Story (post) metadata that scrape from facebook group main page
    
    Attributes:
        AUTHOR_ID (str): Author unique ID
        AUTHOR_NAME (str): Author name
        ID (str): Story (post) unique ID
        N_COMMENT (int): Number of comment in story
        N_LIKE (int): Number of like in story
        PUBLISH_TIME (int): Story publish time
    """
    
    ID = Field()
    PUBLISH_TIME = Field()
    AUTHOR_ID = Field()
    AUTHOR_NAME = Field()
    N_LIKE = Field()
    N_COMMENT = Field()

    def __repr__(self):
        """Customize item message
        
        Returns:
            TYPE: Debugging string shown in scrapy execution log
        """
        return repr(f"{self['ID']}, {self['N_LIKE']}, {self['N_COMMENT']}")


class PostItem(Item):

    """Story main content
    
    Attributes:
        CONTENT (str): Story text body
        ID (str): Story ID
        IMAGES (list): Story images
    """
    
    ID = Field()
    CONTENT = Field()
    IMAGES = Field()

    def __repr__(self):
        """Customize item message
        
        Returns:
            TYPE: Debugging string shown in scrapy execution log
        """
        return repr(f"{self['ID']}, {self['CONTENT']}")


class CommentItem(Item):

    """Stroy comment and reply (comment of comment)
    
    Attributes:
        AUTHOR_NAME (str): Author name
        CONTENT (str): Comment body
        ID (str): Comment ID
        PARENT_ID (str): Comment related-post ID
    """
    
    ID = Field()
    PARENT_ID = Field()
    AUTHOR_NAME = Field()
    CONTENT = Field()

    def __repr__(self):
        """Customize item message
        
        Returns:
            TYPE: Debugging string shown in scrapy execution log
        """
        return repr(f"{self['ID']}, {self['CONTENT']}")
