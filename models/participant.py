from typing import Literal, Optional
from pydantic import BaseModel, HttpUrl

ParticipantType = Literal["host", "guest"]

class Participant(BaseModel):

    type: ParticipantType
    username: str  # Unique ID
    title: str
    bio: Optional[str] = None
    avatar: Optional[str] = None
    avatar_small: Optional[str] = None
    homepage: Optional[str] = None
    twitter: Optional[HttpUrl] = None
    linkedin: Optional[HttpUrl] = None
    instagram: Optional[HttpUrl] = None
    youtube: Optional[HttpUrl] = None