from pydantic_xml import element
from typing import Optional
from models.scraper import NSMAP

NSMAP = {'content':NSMAP['content']}

Encoded: Optional[str] = element(tag='encoded', default=None, ns='content', nsmap=NSMAP)