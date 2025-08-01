from pydantic_xml import attr, element
from pydantic import constr, EmailStr, UUID5, AnyHttpUrl, PositiveInt, field_validator, model_validator
from typing import Any, Optional, Tuple, Literal
from models.scraper import ScraperBaseXmlModel, ScraperRootXmlModel, NSMAP
from uuid import UUID

NSMAP = {'podcast':NSMAP['podcast']}

MEDIUM_VALUES = Literal[
    'podcast',
    'podcastL',
    'music',
    'musicL',
    'video',
    'videoL',
    'film',
    'filmL',
    'audiobook',
    'audiobookL',
    'newsletter',
    'newsletterL',
    'blog',
    'mixed',
    'publisher',
]

ROLE_VALUES = Literal[
    "Director",
    "Assistant Director",
    "Executive Producer",
    "Senior Producer",
    "Producer",
    "Associate Producer",
    "Development Producer",
    "Creative Director",
    "Host",
    "Co-Host",
    "Guest Host",
    "Guest",
    "Voice Actor",
    "Narrator",
    "Announcer",
    "Reporter",
    "Author",
    "Editorial Director",
    "Co-Writer",
    "Writer",
    "Songwriter",
    "Guest Writer",
    "Story Editor",
    "Managing Editor",
    "Script Editor",
    "Script Coordinator",
    "Researcher",
    "Editor",
    "Fact Checker",
    "Translator",
    "Transcriber",
    "Logger",
    "Studio Coordinator",
    "Technical Director",
    "Technical Manager",
    "Audio Engineer",
    "Remote Recording Engineer",
    "Post Production Engineer",
    "Audio Editor",
    "Sound Designer",
    "Foley Artist",
    "Composer",
    "Theme Music",
    "Music Production",
    "Music Contributor",
    "Production Coordinator",
    "Booking Coordinator",
    "Production Assistant",
    "Content Manager",
    "Marketing Manager",
    "Sales Representative",
    "Sales Manager",
    "Graphic Designer",
    "Cover Art Designer",
    "Social Media Manager",
    "Consultant",
    "Intern",
    "Camera Operator",
    "Lighting Designer",
    "Camera Grip",
    "Assistant Camera",
    "Editor",
    "Assistant Editor",
]

GROUP_VALUES = Literal[
    "Creative Direction",
    "Cast",
    "Writing",
    "Audio Production",
    "Audio Post-Production",
    "Administration",
    "Visuals",
    "Community",
    "Misc.",
    "Video Production",
    "Video Post-Production",
]

INTEGRITY_VALUES = Literal[
    "sri",
    "pgp-signature"
]

SOCIAL_INTERACT_PROTOCOL_VALUES = Literal[
    "disabled",
    "activitypub",
    "twitter",
    "lightning",
    "bluesky",
    "hive",
    "matrix",
    "nostr",
]

SERVICE_VALUES = Literal[
    'acast',
    'amazon',
    'anchor',
    'apple',
    'audible',
    'audioboom',
    'backtracks',
    'bitcoin',
    'blubrry',
    'buzzsprout',
    'captivate',
    'castos',
    'castopod',
    'facebook',
    'fireside',
    'fyyd',
    'google',
    'gpodder',
    'hypercatcher',
    'kasts',
    'libsyn',
    'mastodon',
    'megafono',
    'megaphone',
    'omnystudio',
    'overcast',
    'paypal',
    'pinecast',
    'podbean',
    'podcastaddict',
    'podcastguru',
    'podcastindex',
    'podcasts',
    'podchaser',
    'podcloud',
    'podfriend',
    'podiant',
    'podigee',
    'podnews',
    'podomatic',
    'podserve',
    'podverse',
    'redcircle',
    'relay',
    'resonaterecordings',
    'rss',
    'shoutengine',
    'simplecast',
    'slack',
    'soundcloud',
    'spotify',
    'spreaker',
    'tiktok',
    'transistor',
    'twitter',
    'whooshkaa',
    'youtube',
    'zencast',
]

class Podping(ScraperBaseXmlModel, tag='podping', ns='podcast', nsmap=NSMAP):
    usesPodping: bool = attr()

class Recipient(ScraperBaseXmlModel, tag='valueRecipient', ns='podcast', nsmap=NSMAP):
    name: str = attr()
    type: str = attr()
    address: str = attr()
    customKey: Optional[str] = attr(default=None)
    customValue: Optional[str] = attr(default=None)
    split: int = attr()
    fee: Optional[bool] = attr(default=None)

class RemoteItem(ScraperBaseXmlModel, tag='remoteItem', ns='podcast', nsmap=NSMAP):
    feedGuid: UUID5 | str = attr()
    feedUrl: Optional[str] = attr(default=None)
    itemGuid: Optional[str] = attr(default=None)
    medium: Optional[MEDIUM_VALUES] = attr(default='podcast')

class Timesplit(ScraperBaseXmlModel, tag='valueTimeSplit', ns='podcast', nsmap=NSMAP):
    startTime: PositiveInt = attr()
    duration: PositiveInt = attr()
    remotePercentage: Optional[int] = attr(default=None)
    remoteStartTime: Optional[PositiveInt] = attr(default=None)
    remoteItem: Optional[RemoteItem] = element(tag='remoteItem', ns='podcast', nsmap=NSMAP)
    recipients: Optional[Tuple[Recipient, ...]] = element(tag='valueRecipient', ns='podcast', nsmap=NSMAP, default=())

class Value(ScraperBaseXmlModel, tag='value', ns='podcast', nsmap=NSMAP):
    type: str = attr()
    method: str = attr()
    suggested: Optional[float] = attr(default=None)

    recipients: Tuple[Recipient, ...] = element(tag='valueRecipient', ns='podcast', nsmap=NSMAP)
    timesplits: Optional[Tuple[Timesplit, ...]] = element(tag='valueTimeSplit', ns='podcast', nsmap=NSMAP, default=())

class Images(ScraperBaseXmlModel, tag='images', ns='podcast', nsmap=NSMAP):
    srcset: str = attr(default=None)

class Medium(ScraperBaseXmlModel, tag='medium', ns='podcast', nsmap=NSMAP):
    medium: Literal[MEDIUM_VALUES] = 'podcast'

class Locked(ScraperBaseXmlModel, tag='locked', ns='podcast', nsmap=NSMAP):
    owner: Optional[EmailStr] = attr(default=None)
    locked: Literal['yes','no'] = constr(strip_whitespace=True)

class Guid(ScraperRootXmlModel, tag='guid', ns='podcast', nsmap=NSMAP):
    root: UUID

class Person(ScraperBaseXmlModel, tag='person', ns='podcast', nsmap=NSMAP):
    role: Optional[ROLE_VALUES] = attr(default='Host')
    group: Optional[GROUP_VALUES] = attr(default='Cast')
    href: Optional[AnyHttpUrl] = attr(default=None)
    img: Optional[AnyHttpUrl] = attr(default=None)
    name: str = constr(strip_whitespace=True)

    @field_validator('href', 'img', mode='before')
    @classmethod
    def validate_url(cls, value):
        if value == '':
            return None
        return value

    @field_validator('role', 'group', mode='before')
    @classmethod
    def validate_to_title(cls, value):
        return value.title()

class Podroll(ScraperBaseXmlModel, tag='podroll', ns='podcast', nsmap=NSMAP):
    remoteItems: Tuple[RemoteItem, ...] = element(tag='remoteItem', ns='podcast', nsmap=NSMAP)

class Chapters(ScraperBaseXmlModel, tag='chapters', ns='podcast', nsmap=NSMAP):
    url: AnyHttpUrl = attr()
    type: str = attr()

class Transcript(ScraperBaseXmlModel, tag='transcript', ns='podcast', nsmap=NSMAP):
    url: AnyHttpUrl = attr()
    type: str = attr()
    language: Optional[str] = attr(default=None)
    rel: Optional[str] = attr(default=None)

class UpdateFrequency(ScraperBaseXmlModel, tag='updateFrequency', ns='podcast', nsmap=NSMAP):
    complete: Optional[bool] = attr(default=None)
    dtstart: Optional[str] = attr(default=None)
    rrule: Optional[str] = attr(default=None)
    frequency: str = constr(strip_whitespace=True)


class Funding(ScraperBaseXmlModel, tag='funding', ns='podcast', nsmap=NSMAP):
    url: str = attr()
    funding: str = constr(strip_whitespace=True)

class Soundbite(ScraperBaseXmlModel, tag='soundbite', ns='podcast', nsmap=NSMAP):
    startTime: float = attr()
    duration: float = attr()
    soundbite: str = constr(strip_whitespace=True)

class Location(ScraperBaseXmlModel, tag='location', ns='podcast', nsmap=NSMAP):
    geo: Optional[str] = None
    osm: Optional[str] = None
    location: str = constr(strip_whitespace=True)

class Season(ScraperBaseXmlModel, tag='season', ns='podcast', nsmap=NSMAP):
    name: Optional[str] = None
    season: str = constr(strip_whitespace=True)

class Episode(ScraperBaseXmlModel, tag='episode', ns='podcast', nsmap=NSMAP):
    display: Optional[str] = attr(default=None)
    episode: str = constr(strip_whitespace=True)

class Trailer(ScraperBaseXmlModel, tag='trailer', ns='podcast', nsmap=NSMAP):
    url: AnyHttpUrl = attr()
    pubdate: str = attr()
    length: Optional[PositiveInt] = None
    type: Optional[str] = None
    season: Optional[str] = None
    trailer: str = constr(strip_whitespace=True)

class License(ScraperBaseXmlModel, tag='license', ns='podcast', nsmap=NSMAP):
    url: Optional[AnyHttpUrl] = attr(default=None)
    license: str

    @field_validator('url', mode='before')
    @classmethod
    def validate_url(cls, value):
        if value == '':
            return None
        return value

class Integrity(ScraperBaseXmlModel, tag='integrity', ns='podcast', nsmap=NSMAP):
    type: Literal[INTEGRITY_VALUES] = attr()
    value: str = attr()

class Source(ScraperBaseXmlModel, tag='source', ns='podcast', nsmap=NSMAP):
    uri: AnyHttpUrl = attr()
    contentType: Optional[str] = None

class AlternateEnclosure(ScraperBaseXmlModel, tag='alternateEnclosure', ns='podcast', nsmap=NSMAP):
    type: str = attr()
    length: Optional[PositiveInt] = attr(default=None)
    bitrate: Optional[float] = attr(default=None)
    height: Optional[PositiveInt] = attr(default=None)
    lang: Optional[str] = attr(default=None)
    title: Optional[str] = attr(default=None)
    rel: Optional[str] = attr(default=None)
    codecs: Optional[str] = attr(default=None)
    default: Optional[bool] = attr(default=None)
    integrity: Optional[Integrity] = None
    sources: Tuple[Source,...] = element(tag='source')

class SocialInteract(ScraperBaseXmlModel, tag='socialInteract', ns='podcast', nsmap=NSMAP):
    protocol: Literal[SOCIAL_INTERACT_PROTOCOL_VALUES] = attr()
    uri: Optional[AnyHttpUrl] = attr(default=None)
    accountId: Optional[str] = attr(default=None)
    accountUrl: Optional[AnyHttpUrl] = attr(default=None)
    priority: Optional[PositiveInt] = attr(default=None)

    @field_validator('uri',mode='before')
    @classmethod
    def validate_uri(cls, value, values):
        print(values.data['protocol'])
        if values.data['protocol'] != 'disabled' and value is None:
            raise ValueError('uri is required')
        return value


    @model_validator(mode='after')
    @classmethod
    def check_disabled(cls, data):
        if data.protocol == 'disabled':
            data.uri = None
            data.accountId = None
            data.accountUrl = None
            data.priority = None
        return data

class Block(ScraperBaseXmlModel, tag='block', ns='podcast', nsmap=NSMAP):
    id: Optional[Literal[SERVICE_VALUES]] = attr(default=None)
    block: Literal['yes','no']

class Txt(ScraperBaseXmlModel, tag='txt', ns='podcast', nsmap=NSMAP):
    purpose: Optional[str] = attr(default=None)
    txt: str

class Publisher(ScraperBaseXmlModel, tag='publisher', ns='podcast', nsmap=NSMAP):
    remoteItem: RemoteItem

    @field_validator('remoteItem', mode='after')
    @classmethod
    def check_remoteItem(cls, data: RemoteItem):
        if data.medium != 'publisher':
            raise ValueError('RemoteItem medium attribute must be "publisher".')
        return data

class Chat(ScraperBaseXmlModel, tag='chat', ns='podcast', nsmap=NSMAP):
    server: str = attr()
    protocol: str = attr()
    accountId: Optional[str] = attr(default=None)
    space: Optional[str] = attr(default=None)