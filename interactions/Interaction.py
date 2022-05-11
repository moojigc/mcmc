from dataclasses import dataclass
from Message import Message
from Member import Member


@dataclass
class Interaction:
    id: str
    application_id: str
    channel_id: str
    data: Message
    guild_id: str
    member: Member
    token: str
    type: int
    version: int
