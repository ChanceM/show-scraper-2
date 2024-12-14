from pydantic import BaseModel
from typing import Optional


class Sponsor(BaseModel):
    shortname: str
    title: str
    description: str
    link: str
    episode: Optional[int] = None