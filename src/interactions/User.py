
from dataclasses import dataclass


@dataclass
class User:
    avatar: str
    discriminator: str
    id: str
    public_flags: int
    username: str
