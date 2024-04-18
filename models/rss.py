from typing import Optional
from pydantic_xml import attr
from models.scraper import ScraperBaseXmlModel, NSMAP
from models.channel import Channel


class Rss(ScraperBaseXmlModel, tag='rss', nsmap=NSMAP):
    version: float = attr(default=2.0)
    # encoding: Optional[str] = attr(default=None)
    channel: Channel