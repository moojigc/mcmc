from interactions.User import User
from dataclasses import dataclass, field
from typing import List


@dataclass
class Member:
    deaf: bool
    is_pending: bool
    pending: bool
    joined_at: str
    mute: bool
    permissions: int
    roles: List[str]
    flags: int
    user: User
    premium_since: str = None
    nick: str = None
    avatar: str = None
    communication_disabled_until: int = None
    guild_id: str = None

    def __post_init__(self):
        self.user = User(**self.user)
