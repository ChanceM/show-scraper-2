from pydantic import BaseModel, HttpUrl
from typing import Dict, Set


class ShowDetails(BaseModel):
    show_rss: HttpUrl
    show_url: HttpUrl
    jb_url: HttpUrl
    acronym: str
    name: str
    host_platform: str

class ConfigData(BaseModel):
    shows: Dict[str,ShowDetails]
    usernames_map: Dict[str,Set[str]]