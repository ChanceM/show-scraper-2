from typing import Optional
from pydantic import AnyHttpUrl, BaseModel

class PickShow(BaseModel):
    show: str
    episode: int|str
    slug: str

class Pick(BaseModel):
    title: str
    url: AnyHttpUrl
    description: Optional[str] = None
    shows: list[PickShow]
    license: Optional[str] = None