import os
from pydantic_xml import attr, element
from typing import Tuple, Optional
from models .scraper import ScraperBaseXmlModel
from models.podcast import AlternateEnclosure, Chapters, Episode, License, Location, Season, Soundbite, Transcript, Value, Images, Person
from models.itunes import Subtitle, Title, ItunesImage, Author, Explicit,  Duration, ItunesEpisode, EpisodeType
from pydantic import constr, AnyHttpUrl, field_validator
from datetime import datetime

class Guid(ScraperBaseXmlModel, tag='guid', ns=''):
    isPermaLink: Optional[bool] = attr(default=None)
    guid: str = constr(strip_whitespace=True)

class Enclosure(ScraperBaseXmlModel, tag='enclosure', ns=''):
    length: int = attr(default=None)
    type: str = attr(default=None)
    url: AnyHttpUrl = attr(default=None)

class Item(ScraperBaseXmlModel, tag='item'):
    title: str = element(ns='')
    description: Optional[str] = element(default=None, ns='')
    enclosure: Optional[Enclosure] = None
    guid: Optional[Guid] = None
    link: Optional[str] = element(tag='link', default=None, ns='')
    pubDate: Optional[str] = element(default=None, ns='')
    itunes_author: Optional[str] = Author
    itunes_duration: Optional[Duration] = None
    itunes_episode: Optional[int] = ItunesEpisode
    itunes_episodeType: Optional[str] = EpisodeType
    itunes_explicit: Optional[Explicit] = None
    itunes_image: Optional[ItunesImage] = None
    itunes_subtitle: Optional[Subtitle] = None
    itunes_title: Optional[str] = Title
    podcast_alternateEnclosure: Optional[AlternateEnclosure] = None
    podcast_chapters: Optional[Chapters] = None
    podcast_episode: Optional[Episode] = None
    podcast_images: Optional[Images] = None
    podcast_license: Optional[License] = None
    podcast_location: Optional[Location] = None
    podcast_persons: Optional[Tuple[Person, ...]] = []
    podcast_season: Optional[Season] = None
    podcast_soundbite: Optional[Tuple[Soundbite, ...]] = []
    podcast_transcripts: Optional[Tuple[Transcript, ...]] = []
    podcast_value: Optional[Value] = None

    @field_validator('pubDate', mode='before')
    def pubDate_validator(cls, value: str) -> str:
        return datetime.strptime(value, '%a, %d %b %Y %H:%M:%S %z').isoformat()