from pydantic import BaseModel


class Sponsor(BaseModel):
    shortname: str
    title: str
    description: str
    link: str
