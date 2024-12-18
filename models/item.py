from pydantic_xml import BaseXmlModel, attr, element
from typing import Tuple, Optional
from models.podcast import Chapters, Podping, Transcript, Value, Podroll, Images, Medium, Locked, Guid, Person, PodcastEpisode
from models.itunes import Category, Title, ItunesImage, Author, Owner, Explicit, Type, Duration, ItunesEpisode, EpisodeType
from pydantic import UUID5, EmailStr, constr, AnyHttpUrl

class Guid(BaseXmlModel, tag='guid'):
    isPermaLink: Optional[bool] = attr(default=None)
    guid: str = constr(strip_whitespace=True)

class Enclosure(BaseXmlModel, tag='enclosure'):
    length: int = attr(default=None)
    type: str = attr(default=None)
    url: AnyHttpUrl = attr(default=None)

class Item(BaseXmlModel, tag='item'):
    title: str = element()
    description: Optional[str] = element(default=None)
    guid: Optional[Guid] = element(tag='guid', default=None)
    link: Optional[str] = element(tag='link', default=None)
    pubDate: Optional[str] = element(default=None)
    podcastValue: Optional[Value] = None
    itunesImage: Optional[ItunesImage] = None
    podcastImages: Optional[Images] = None
    itunesDuration: Optional[str] = Duration
    itunesExplicit: Optional[bool] = Explicit
    itunesTitle: Optional[str] = Title
    itunesAuthor: Optional[str] = Author
    itunesEpisode: Optional[int] = ItunesEpisode
    podcastEpisode: Optional[int] = PodcastEpisode
    itunesEpisodeType: Optional[str] = EpisodeType
    enclosure: Optional[Enclosure] = None
    podcastChapters: Optional[Chapters] = Chapters
    podcastTranscripts: Tuple[Transcript, ...] = Transcript
    podcastPersons: Tuple[Person, ...] = Person