"""Scrapy pipeline module
"""
import json
from pathlib import Path


class JsonFilePipeline:

    """Scrapy pipeline class that run after 
    
    Attributes:
        targ_basepath (pathlib.Path): Target folder for save the data
    """
    
    def __init__(self, output_path):
        """Pipeline initilize method
        
        Args:
            output_path (pathlib.Path): Target folder for save the data
        """
        self.targ_basepath = output_path
        self.targ_basepath.mkdir(parents=True, exist_ok=True)

    @classmethod
    def from_crawler(cls, crawler):
        """Pipeline factory method
        
        Args:
            crawler (scrapy.crawler.Crawler): Scrapy crawler object
        
        Returns:
            TYPE: Scrapy pipeline instance
        """
        return cls(output_path=crawler.settings.get("OUTPUT_PATH", Path("data")))

    def process_item(self, item, spider):
        """Append each parsed item into file
        
        Args:
            item (scrapy.item.Item): Scrapy item
            spider (scrapy.spiders.Spider): Scrapy spider
        
        Returns:
            scrapy.item.Item: Scrapy item
        """
        json_string = json.dumps(dict(item), ensure_ascii=False)
        filename = f"{type(item).__name__}.json"
        filepath = self.targ_basepath / filename
        with open(filepath, "a", encoding="utf-8") as f:  # /path/to/data/*.json
            f.write(json_string + "\n")

        return item
