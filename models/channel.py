from pydantic_xml import BaseXmlModel, attr, element
from typing import Tuple, Optional
from models.podcast import Podping, Value, Podroll, Images, Medium, Locked, Guid, Person
from models.itunes import Category, Title, ItunesImage, Author, Owner, Explicit, Type
from models.item import Item
from pydantic import UUID5, EmailStr

ns = {
    'atom': 'http://www.w3.org/2005/Atom/',
    'atom': 'http://www.w3.org/2005/Atom',
    'podcast': 'https://podcastindex.org/namespace/1.0'
}

class AtomLink(BaseXmlModel, tag='link', ns='atom', nsmap=ns):
    rel: Optional[str] = attr(default=None)
    href: str = attr()
    type: Optional[str] = attr(default=None)
    title: Optional[str] = attr(default=None)

class Image(BaseXmlModel, tag='image'):
    url: str = element(tag='url')
    title: str = element(tag='title')
    link: str = element(tag='link')
    description: Optional[str] = element(tag='description', default=None)
    height: Optional[int] = element(tag='height', default=None)
    width: Optional[int] = element(tag='width', default=None)

class Channel(BaseXmlModel, tag='channel'):
    atomLinks: Optional[Tuple[AtomLink, ...]] = element(tag='link', ns='atom', nsmap=ns, default=None)
    podcastPodping: Optional[Podping] = None
    podcastValue: Optional[Value] = None
    podcastPodroll: Optional[Podroll] = None
    image: Optional[Image] = None
    podcastImages: Optional[Images] = None
    podcastMedium: Optional[str] = Medium
    title: str = element(tag='title')
    description: str = element()
    link: str = element(tag='link')
    language: str = element()
    copyright: str = element()
    podcastLocked: Optional[Locked] = None
    podcastGuid: Optional[str] = Guid
    podcastPersons: Optional[Tuple[Person,...]] = Person
    generator: Optional[str] = element(default=None)
    managingEditor: Optional[EmailStr] = element(default=None)
    lastBuildDate: Optional[str] = element(default=None)
    pubDate: Optional[str] = element(default=None)
    itunesTitle: Optional[str] = Title
    itunesImage: Optional[ItunesImage] = None
    itunesAuthor: Optional[str] = Author
    itunesOwner: Optional[Owner] = None
    itunesExplicit: Optional[bool] = Explicit
    itunesCategories: Tuple[Category, ...] = Category
    itunesType: Optional[str] = Type
    items: Tuple[Item, ...] = element(tag='item')