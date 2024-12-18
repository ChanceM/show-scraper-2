from typing import Tuple, Optional, Any
from pydantic_xml import BaseXmlModel, RootXmlModel, attr, element, wrapped

from models.channel import Channel

class Rss(BaseXmlModel, tag='rss'):
    version: Optional[float] = attr(default=None)
    encoding: Optional[str] = attr(default=None)
    channel: Channel