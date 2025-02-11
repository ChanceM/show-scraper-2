from pydantic import BaseModel, HttpUrl
from typing import Dict, List, Optional, Set


class ShowDetails(BaseModel):
    show_rss: HttpUrl
    show_url: HttpUrl
    jb_url: HttpUrl
    acronym: str
    name: str
    host_platform: str
    dont_override: Optional[List[str]] = []

class ConfigData(BaseModel):
    shows: Dict[str,ShowDetails]
    usernames_map: Dict[str,Set[str]]
    data_dont_override: Set[str]