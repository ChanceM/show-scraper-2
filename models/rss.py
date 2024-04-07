from typing import Optional
from pydantic_xml import attr
from models.scraper import ScraperBaseXmlModel
from models.channel import Channel

class Rss(ScraperBaseXmlModel, tag='rss'):
    version: Optional[float] = attr(default=None)
    encoding: Optional[str] = attr(default=None)
    channel: Channel