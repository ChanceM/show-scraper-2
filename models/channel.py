import os
from datetime import datetime
from pydantic import EmailStr, field_validator, ConfigDict
from pydantic_xml import attr, element
from typing import Tuple, Optional
from models.scraper import ScraperBaseXmlModel
from models.podcast import Funding, Location, Podping, Trailer, UpdateFrequency, Value, Podroll, Images, Medium, Locked, Guid, Person
from models.itunes import Category, Subtitle, Title, ItunesImage, Author, Owner, Explicit, Type
from models.item import Item

ns = {
    'atom': 'http://www.w3.org/2005/Atom'
}

class AtomLink(ScraperBaseXmlModel, tag='link', ns='atom', nsmap=ns):
    rel: Optional[str] = attr(default=None)
    href: str = attr()
    type: Optional[str] = attr(default=None)
    title: Optional[str] = attr(default=None)

class Image(ScraperBaseXmlModel, tag='image'):
    url: str = element(tag='url')
    title: str = element(tag='title')
    link: str = element(tag='link')
    description: Optional[str] = element(tag='description', default=None)
    height: Optional[int] = element(tag='height', default=None)
    width: Optional[int] = element(tag='width', default=None)

class Channel(ScraperBaseXmlModel, tag='channel'):
    atomLinks: Optional[Tuple[AtomLink, ...]] = element(tag='link', ns='atom', nsmap=ns, default=None)
    podcastPodping: Optional[Podping] = None
    podcastValue: Optional[Value] = None
    podcastPodroll: Optional[Podroll] = None
    image: Optional[Image] = None
    podcastImages: Optional[Images] = None
    podcastUpdateFrequency: Optional[UpdateFrequency] = None
    podcastMedium: Optional[str] = Medium
    title: str = element()
    description: str = element()
    link: str = element()
    language: str = element()
    copyright: str = element()
    podcastLocation: Optional[Location] = None
    podcastLocked: Optional[Locked] = None
    podcastGuid: Optional[str] = Guid
    podcastPersons: Optional[Tuple[Person,...]] = Person
    podcastTrailer: Optional[Tuple[Trailer,...]] = Trailer
    generator: Optional[str] = element(default=None)
    managingEditor: Optional[EmailStr] = element(default=None)
    lastBuildDate: Optional[str] = element(default=None)
    pubDate: Optional[str] = element(default=None)
    itunesTitle: Optional[str] = Title
    itunesImage: Optional[ItunesImage] = None
    itunesAuthor: Optional[str] = Author
    itunesOwner: Optional[Owner] = None
    itunesExplicit: Optional[Explicit] = None
    itunesCategories: Tuple[Category, ...] = Category
    itunesType: Optional[str] = Type
    itunesSubtitle: Optional[Subtitle] = None
    podcastFunding: Optional[Funding] = None
    items: Tuple[Item, ...] = element(tag='item')

    @field_validator('pubDate', mode='before')
    def pubDate_validator(cls, value: str) -> str:
        return datetime.strptime(value, '%a, %d %b %Y %H:%M:%S %z').isoformat()