import os
from datetime import datetime
from models.liveitem import LiveItem
from pydantic import EmailStr, field_validator
from pydantic_xml import attr, element
from typing import Tuple, Optional
from models.scraper import ScraperBaseXmlModel
from models.podcast import (
    Funding,
    License,
    Location,
    Podping,
    Trailer,
    UpdateFrequency,
    Value,
    Podroll,
    Images,
    Medium,
    Locked,
    Guid,
    Person,
)
from models.itunes import (
    Category,
    Subtitle,
    Title,
    ItunesImage,
    Author,
    Owner,
    Explicit,
    Type,
)
from models.item import Item

ns = {"atom": "http://www.w3.org/2005/Atom"}


class AtomLink(ScraperBaseXmlModel, tag="link", ns="atom", nsmap=ns):
    rel: Optional[str] = attr(default=None)
    href: str = attr()
    type: Optional[str] = attr(default=None)
    title: Optional[str] = attr(default=None)


class Image(ScraperBaseXmlModel, tag="image"):
    url: str = element(tag="url")
    title: str = element(tag="title")
    link: str = element(tag="link")
    description: Optional[str] = element(tag="description", default=None)
    height: Optional[int] = element(tag="height", default=None)
    width: Optional[int] = element(tag="width", default=None)


class Channel(ScraperBaseXmlModel, tag="channel"):
    atom_links: Optional[Tuple[AtomLink, ...]] = element(
        tag="link", ns="atom", nsmap=ns, default=None
    )
    image: Optional[Image] = None
    title: str = element()
    description: str = element()
    link: str = element()
    generator: Optional[str] = element(default=None)
    language: str = element()
    copyright: str = element()
    managingEditor: Optional[EmailStr] = element(default=None)
    lastBuildDate: Optional[str] = element(default=None)
    itunes_author: Optional[str] = Author
    itunes_categories: Tuple[Category, ...] = None
    itunes_explicit: Optional[Explicit] = None
    itunes_image: Optional[ItunesImage] = None
    itunes_owner: Optional[Owner] = None
    itunes_subtitle: Optional[Subtitle] = None
    itunes_title: Optional[str] = Title
    itunes_type: Optional[str] = Type
    pubDate: Optional[str] = element(default=None)
    podcast_funding: Optional[Funding] = None
    podcast_guid: Optional[Guid] = None
    podcast_images: Optional[Images] = None
    podcast_license: Optional[License] = None
    podcast_liveItem: Optional[Tuple[LiveItem,...]] = None
    podcast_location: Optional[Location] = None
    podcast_locked: Optional[Locked] = None
    podcast_medium: Optional[Medium] = None
    podcast_persons: Optional[Tuple[Person, ...]] = None
    podcast_podping: Optional[Podping] = None
    podcast_podroll: Optional[Podroll] = None
    podcast_trailer: Optional[Tuple[Trailer, ...]] = None
    podcast_updateFrequency: Optional[UpdateFrequency] = None
    podcast_value: Optional[Value] = None
    items: Tuple[Item, ...] = element(tag="item")

    @field_validator("pubDate", mode="before")
    def pubDate_validator(cls, value: str) -> str:
        return datetime.strptime(value, "%a, %d %b %Y %H:%M:%S %z").isoformat()
