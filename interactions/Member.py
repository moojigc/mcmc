from interactions.User import User
from dataclasses import dataclass, field
from typing import List


@dataclass
class Member:
    deaf: bool
    is_pending: bool
    joined_at: str
    mute: bool
    nick: str
    permissions: str
    premium_since: str
    roles: List[str]
    user: User = field(default_factory=User)
