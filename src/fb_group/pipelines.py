import logging
import json
from pathlib import Path

logger = logging.getLogger(__name__)


class JsonFilePipeline:
    def __init__(self, output_path):
        self.targ_basepath = output_path
        self.targ_basepath.mkdir(parents=True, exist_ok=True)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(output_path=crawler.settings.get("OUTPUT_PATH", Path("data")))

    def process_item(self, item, spider):
        json_string = json.dumps(dict(item), ensure_ascii=False)
        filename = f"{type(item).__name__}.json"
        filepath = self.targ_basepath / filename
        with open(filepath, "a", encoding="utf-8") as f:  # /path/to/data/*.json
            f.write(json_string + "\n")

        return item
