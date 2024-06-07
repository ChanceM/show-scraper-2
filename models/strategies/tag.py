from abc import ABC, abstractmethod
from typing import List

from bs4 import BeautifulSoup, NavigableString

from models.config import ShowDetails

class TagParseStrategy(ABC):
    @abstractmethod
    def parse(self, page: BeautifulSoup, show_details: ShowDetails) -> List[str]:
        pass

class FiresideTagParse(TagParseStrategy):
    def parse(self, page: BeautifulSoup, show_details: ShowDetails) -> List[str]:
        tags = []

        for link in page.find_all("a", class_="tag"):
            _tag = link.get_text().strip()
            # escape inner quotes (occurs in coderradio 434)
            _tag = _tag.replace('"', r'\"')
            tags.append(_tag)

        return sorted(tags)

class PodhomeTagParse(TagParseStrategy):
    def parse(self, page: BeautifulSoup, show_details: ShowDetails) -> List[str]:
        return []

class TagParser:
    def __init__(self, page, show_details: ShowDetails, parse_strategy: TagParseStrategy):
        self.page = page
        self.parse_strategy = parse_strategy
        self.show_details = show_details

    def run(self):
        return self.parse_strategy.parse(self.page, self.show_details)