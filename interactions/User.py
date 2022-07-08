
from dataclasses import dataclass

from interactions.my_utils import DiscordObject


@dataclass
class User(DiscordObject):
    avatar: str
    discriminator: str
    id: str
    public_flags: int
    username: str
    avatar_decoration: str = None
