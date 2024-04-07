import os
from pydantic_xml import attr, element
from typing import Tuple, Optional
from models .scraper import ScraperBaseXmlModel
from models.podcast import Chapters, Episode, Location, Season, Soundbite, Transcript, Value, Images, Guid, Person
from models.itunes import Subtitle, Title, ItunesImage, Author, Explicit,  Duration, ItunesEpisode, EpisodeType
from pydantic import constr, AnyHttpUrl, field_validator
from datetime import datetime

class Guid(ScraperBaseXmlModel, tag='guid'):
    isPermaLink: Optional[bool] = attr(default=None)
    guid: str = constr(strip_whitespace=True)

class Enclosure(ScraperBaseXmlModel, tag='enclosure'):
    length: int = attr(default=None)
    type: str = attr(default=None)
    url: AnyHttpUrl = attr(default=None)

class Item(ScraperBaseXmlModel, tag='item'):
    title: str = element()
    description: Optional[str] = element(default=None)
    enclosure: Optional[Enclosure] = None
    guid: Optional[Guid] = element(tag='guid', default=None)
    link: Optional[str] = element(tag='link', default=None)
    pubDate: Optional[str] = element(default=None)
    itunesImage: Optional[ItunesImage] = None
    itunesDuration: Optional[Duration] = None
    itunesExplicit: Optional[Explicit] = None
    itunesTitle: Optional[str] = Title
    itunesAuthor: Optional[str] = Author
    itunesEpisode: Optional[int] = ItunesEpisode
    itunesEpisodeType: Optional[str] = EpisodeType
    itunesSubtitle: Optional[Subtitle] = None
    podcastSoundbite: Optional[Tuple[Soundbite, ...]] = []
    podcastSeason: Optional[Season] = None
    podcastLocation: Optional[Location] = None
    podcastValue: Optional[Value] = None
    podcastImages: Optional[Images] = None
    podcastEpisode: Optional[Episode] = None
    podcastChapters: Optional[Chapters] = None
    podcastTranscripts: Optional[Tuple[Transcript, ...]] = []
    podcastPersons: Optional[Tuple[Person, ...]] = []

    @field_validator('pubDate', mode='before')
    def pubDate_validator(cls, value: str) -> str:
        return datetime.strptime(value, '%a, %d %b %Y %H:%M:%S %z').isoformat()