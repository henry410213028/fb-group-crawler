from scrapy.item import Item, Field


class StoryItem(Item):
    ID = Field()
    PUBLISH_TIME = Field()
    AUTHOR_ID = Field()
    AUTHOR_NAME = Field()
    N_LIKE = Field()
    N_COMMENT = Field()

    def __repr__(self):
        return repr(f"{self['ID']}, {self['N_LIKE']}, {self['N_COMMENT']}")


class PostItem(Item):
    ID = Field()
    CONTENT = Field()

    def __repr__(self):
        return repr(f"{self['ID']}, {self['CONTENT']}")


class CommentItem(Item):
    ID = Field()
    PARENT_ID = Field()
    AUTHOR_NAME = Field()
    CONTENT = Field()

    def __repr__(self):
        return repr(f"{self['ID']}, {self['CONTENT']}")
