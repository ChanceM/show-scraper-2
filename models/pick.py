from typing import Optional
from pydantic import AnyHttpUrl, BaseModel

class PickShow(BaseModel):
    show: str
    episode: int|str
    slug: str

class Pick(BaseModel):
    title: str
    url: AnyHttpUrl
    description: str
    shows: list[PickShow]
    license: Optional[str] = None