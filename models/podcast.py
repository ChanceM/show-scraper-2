from pydantic_xml import BaseXmlModel, attr, element
from pydantic import constr, EmailStr, UUID5, AnyHttpUrl
from typing import Optional, Tuple, Literal

NSMAP = {
    'podcast': 'https://podcastindex.org/namespace/1.0',
}

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
    'mixed'
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
    "director",
    "assistant director",
    "executive producer",
    "senior producer",
    "producer",
    "associate producer",
    "development producer",
    "creative director",
    "host",
    "co-host",
    "guest host",
    "guest",
    "voice actor",
    "narrator",
    "announcer",
    "reporter",
    "author",
    "editorial director",
    "co-writer",
    "writer",
    "songwriter",
    "guest writer",
    "story editor",
    "managing editor",
    "script editor",
    "script coordinator",
    "researcher",
    "editor",
    "fact checker",
    "translator",
    "transcriber",
    "logger",
    "studio coordinator",
    "technical director",
    "technical manager",
    "audio engineer",
    "remote recording engineer",
    "post production engineer",
    "audio editor",
    "sound designer",
    "foley artist",
    "composer",
    "theme music",
    "music production",
    "music contributor",
    "production coordinator",
    "booking coordinator",
    "production assistant",
    "content manager",
    "marketing manager",
    "sales representative",
    "sales manager",
    "graphic designer",
    "cover art designer",
    "social media manager",
    "consultant",
    "intern",
    "camera operator",
    "lighting designer",
    "camera grip",
    "assistant camera",
    "editor",
    "assistant editor",
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
    "creative direction",
    "cast",
    "writing",
    "audio production",
    "audio post-production",
    "administration",
    "visuals",
    "community",
    "misc.",
    "video production",
    "video post-production",
]

class Podping(BaseXmlModel, tag='podping', ns='podcast', nsmap=NSMAP):
    usesPodping: bool = attr()

class Recipient(BaseXmlModel, tag='valueRecipient', ns='podcast', nsmap=NSMAP):
    name: str = attr()
    type: str = attr()
    address: str = attr()
    customKey: Optional[str] = attr(default=None)
    customValue: Optional[str] = attr(default=None)
    split: int = attr()
    fee: Optional[bool] = attr(default=None)

class Value(BaseXmlModel, tag='value', ns='podcast', nsmap=NSMAP):
    type: str = attr()
    method: str = attr()
    suggested: Optional[float] = attr(default=None)

    recipients: Tuple[Recipient, ...] = element(tag='valueRecipient', ns='podcast', nsmap=NSMAP)

class RemoteItem(BaseXmlModel, tag='remoteITem', ns='podcast', nsmap=NSMAP):
    feedGuid: str = attr()
    feedUrl: Optional[str] = attr(default=None)
    itemGuid: Optional[str] = attr(default=None)
    medium: Optional[MEDIUM_VALUES] = attr(default='podcast')

class Images(BaseXmlModel, tag='images', ns='podcast', nsmap=NSMAP):
    srcset: str = attr(default=None)

Medium: Literal[MEDIUM_VALUES] = element(tag='medium', ns='podcast', nsmap=NSMAP, default='podcast')

class Locked(BaseXmlModel, tag='locked', ns='podcast', nsmap=NSMAP):
    owner: Optional[EmailStr] = attr(default=None)
    locked: Literal['yes','no'] = constr(strip_whitespace=True)

Guid: UUID5 = element(tag='guid', ns='podcast', nsmap=NSMAP, default=None )

class Person(BaseXmlModel, tag='person', ns='podcast', nsmap=NSMAP):
    role: Optional[ROLE_VALUES] = attr(default='host')
    group: Optional[GROUP_VALUES] = attr(default='cast')
    href: Optional[AnyHttpUrl] = attr(default=None)
    image: Optional[AnyHttpUrl] = attr(default=None)
    name: str = constr(strip_whitespace=True)

class Podroll(BaseXmlModel, tag='podroll', ns='podcast', nsmap=NSMAP):
    remoteItems: Tuple[RemoteItem, ...] = element(tag='remoteItem')

PodcastEpisode: int = element(tag='episode', ns='podcast', nsmap=NSMAP, default=None )

class Chapters(BaseXmlModel, tag='chapters', ns='podcast', nsmap=NSMAP):
    url: AnyHttpUrl = attr()
    type: str = attr()

class Transcript(BaseXmlModel, tag='transcript', ns='podcast', nsmap=NSMAP):
    url: AnyHttpUrl = attr()
    type: str = attr()
    language: Optional[str] = attr(default=None)
    rel: Optional[str] = attr(default=None)

class UpdateFrequency(BaseXmlModel, tag='updateFrequency', ns='podcast', nsmap=NSMAP):
    complete: Optional[bool] = attr(default=None)
    dtstart: Optional[str] = attr(default=None)
    rrule: Optional[str] = attr(default=None)
    frequency: str = constr(strip_whitespace=True)