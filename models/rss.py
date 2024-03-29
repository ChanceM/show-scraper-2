from typing import Optional
from pydantic_xml import BaseXmlModel, attr

from models.channel import Channel

class Rss(BaseXmlModel, tag='rss'):
    version: Optional[float] = attr(default=None)
    encoding: Optional[str] = attr(default=None)
    channel: Channel