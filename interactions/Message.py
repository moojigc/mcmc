from dataclasses import dataclass, field
from enum import Enum
from typing import Any, List

from interactions.my_utils import DiscordObject


class ValueType(Enum):
    STR = 3
    NUMERIC = 4


@dataclass
class Option(DiscordObject):
    name: str
    type: int
    value: str


@dataclass
class Message(DiscordObject):
    id: str
    name: str
    type: int
    options: List[Option] = field(
        default_factory=list)
    value: str = None
    guild_id: str = None

    def __post_init__(self):
        self.options = [
            Option.from_dict(**option) for option in self.options
        ]
