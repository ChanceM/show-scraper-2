from typing import Literal, Optional, Tuple
from models.episode import Chapters, Episode, Location
from models.itunes import Author, Duration, EpisodeType, Explicit, ItunesEpisode, ItunesImage, Subtitle, Title
from models.podcast import AlternateEnclosure, Images, License, Person, Season, Soundbite, Transcript, Value
from pydantic import AwareDatetime
from pydantic_xml import attr, element
from models.item import Enclosure, Guid, Item
from models.scraper import NSMAP, ScraperBaseXmlModel

NSMAP = {'podcast':NSMAP['podcast']}

STATUS_VALUES = Literal[
    "pending",
    "live",
    "ended",
]

class LiveItem(Item, tag='liveitem', ns='podcast', nsmap=NSMAP):
    status: Literal[STATUS_VALUES] = attr()
    start: AwareDatetime = attr()
    end: Optional[AwareDatetime] = attr(default=None)