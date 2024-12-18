from pydantic import BaseModel, HttpUrl
from typing import Dict, Set


class ShowDetails(BaseModel):
    show_url: HttpUrl
    show_guid: str
    jb_url: HttpUrl
    acronym: str
    name: str

class ConfigData(BaseModel):
    shows: Dict[str,ShowDetails]
    usernames_map: Dict[str,Set[str]]