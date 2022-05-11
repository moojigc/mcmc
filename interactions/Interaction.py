from dataclasses import dataclass, field, make_dataclass
from interactions.Message import Message
from interactions.Member import Member


@dataclass
class Interaction:
    id: str
    application_id: str
    channel_id: str
    guild_id: str
    guild_locale: str
    locale: str
    token: str
    type: int
    version: int
    member: Member = field(default_factory=Member)
    data: Message = field(default_factory=Message)
