from datetime import time
import re
from pydantic_xml import BaseXmlModel, attr, element, wrapped,RootXmlModel
from pydantic import EmailStr, PositiveInt, AnyHttpUrl, constr, field_validator
from typing import Optional, Literal

NSMAP = {
    'itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd',
}

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

class ItunesImage(BaseXmlModel, tag='image', ns='itunes', nsmap=NSMAP):
    href: Optional[AnyHttpUrl] = attr(default=None)

Author: str = element(tag='author', default=None, ns='itunes', nsmap=NSMAP)

class Owner(BaseXmlModel, tag='owner', ns='itunes', nsmap=NSMAP):
    name: Optional[str] = wrapped('name', default=None)
    email: Optional[EmailStr] = wrapped('email', default=None)

class Explicit(BaseXmlModel, tag='explicit', ns='itunes', nsmap=NSMAP):
    root: Literal['yes','no'] = constr(strip_whitespace=True)

    @field_validator('root', mode='before')
    @classmethod
    def validate_explicit(cls, value):
        if str(value).lower() in {'false','no'} or value == 0:
            return 'no'
        return 'yes'
# Explicit: bool = element(tag='explicit', default=None, ns='itunes', nsmap=NSMAP)

class Category(BaseXmlModel, tag='category', ns='itunes', nsmap=NSMAP):
    text: str = attr()
    category: Optional[str] = wrapped('category',attr(name='text',default=None),default=None)

Type: Optional[TYPE_VALUES] = element(tag='type', default=None, ns='itunes', nsmap=NSMAP)

class Duration(BaseXmlModel, tag='duration', ns='itunes', nsmap=NSMAP):
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