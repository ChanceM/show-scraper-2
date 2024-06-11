from datetime import time
from pydantic_xml import attr, element, wrapped
from pydantic import EmailStr, PositiveInt, AnyHttpUrl, constr, field_validator
from typing import List, Optional, Literal
from models.scraper import ScraperBaseXmlModel, ScraperRootXmlModel, NSMAP

NSMAP = {'itunes':NSMAP['itunes']}

TYPE_VALUES = Literal[
    'episodic',
    'serial',
    'Episodic',
    'Serial'
]

EPISODE_TYPES = Literal[
    'Full',
    'Trailer',
    'Bonus',
]

Title: str = element(tag='title', default=None, ns='itunes', nsmap=NSMAP)

class ItunesImage(ScraperBaseXmlModel, tag='image', ns='itunes', nsmap=NSMAP):
    href: Optional[AnyHttpUrl] = attr(default=None)

Author: str = element(tag='author', default=None, ns='itunes', nsmap=NSMAP)

class Owner(ScraperBaseXmlModel, tag='owner', ns='itunes', nsmap=NSMAP):
    name: Optional[str] = wrapped('name', default=None)
    email: Optional[EmailStr] = wrapped('email', default=None)

class Explicit(ScraperBaseXmlModel, tag='explicit', ns='itunes', nsmap=NSMAP):
    root: Literal['yes','no'] = constr(strip_whitespace=True)

    @field_validator('root', mode='before')
    @classmethod
    def validate_explicit(cls, value):
        if str(value).lower() in {'false','no'} or not bool(value):
            return 'no'
        return 'yes'

class Category(ScraperBaseXmlModel, tag='category', ns='itunes', nsmap=NSMAP):
    text: str = attr()
    category: Optional[str] = wrapped('category',attr(name='text',default=None),default=None)

Type: Optional[TYPE_VALUES] = element(tag='type', default=None, ns='itunes', nsmap=NSMAP)

class Duration(ScraperBaseXmlModel, tag='duration', ns='itunes', nsmap=NSMAP):
    root: time = constr(strip_whitespace=True)
    @field_validator('root', mode='before')
    @classmethod
    def validate_duration(cls, value: time|PositiveInt|str) -> time:
        if type(value) == int or value.isnumeric():
            seconds = int(value)
            minutes, seconds = divmod(seconds, 60)
            hours, minutes = divmod(minutes, 60)
            return time(hours, minutes, seconds)
        match value.count(':'):
            case 1:
                minutes, seconds = value.split(':')
                value = f"00:{int(minutes):02}:{int(seconds):02}"
            case 2:
                hours, minutes, seconds = value.split(':')
                value = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
        return time.fromisoformat(value)

ItunesEpisode: Optional[PositiveInt] = element(tag='episode', default=None, ns='itunes', nsmap=NSMAP)

EpisodeType: Optional[EPISODE_TYPES] = element(tag='episodeType', default='Full', ns='itunes', nsmap=NSMAP)

class Subtitle(ScraperRootXmlModel, tag='subtitle', ns='itunes', nsmap=NSMAP):
    root: str = constr(strip_whitespace=True)

class Keywords(ScraperBaseXmlModel, tag='keywords', ns='itunes', nsmap=NSMAP):
    keywords: str = constr(strip_whitespace=True)

    @field_validator('keywords', mode='after')
    @classmethod
    def validate_keywords(cls, value: str) -> List[str]:
       return [keyword.lower().strip() for keyword in value.split(',')]